"""Public-source development preparation; never opens a frozen holdout or database."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from app.assistant import Context, normalize
from app.assistant_learning import RUNTIME_CORPORA
from evaluate_routing import route_label
from app.assistant_training import TrainingTarget

ROOT=Path(__file__).resolve().parents[2]
SUPPLEMENT=Path(__file__).parent/'data/ood-development.json'
TOPICS=('overview','players','queue','machine','scores','levels','trend','top','definition','knowledge','social','follow_up','unsupported')


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    # Explicit paths only: no directory glob, private export or evaluation import.
    result=[]
    for path in RUNTIME_CORPORA:
        payload=json.loads(path.read_text(encoding='utf-8'))
        for row in payload['examples']:
            if row['split']!='train': continue
            previous=Context.model_validate(row['previous']).model_dump() if row.get('previous') else None
            family=row.get('family') or 'undocumented-'+re.sub(r'[-_]\d+$','',row['id'])
            result.append({**row,'id':path.stem+':'+row['id'],'source':path.name,
                           'family':family,'previous':previous,'label':route_label(row['target'])})
    supplement=json.loads(SUPPLEMENT.read_text(encoding='utf-8'))
    for family,questions in supplement['families'].items():
        for i,question in enumerate(questions):
            result.append({'id':f'lab-negative:{family}:{i}','source':SUPPLEMENT.name,
                           'family':'negative-'+family,'previous':None,'label':'unsupported',
                           'target':{'topic':'unsupported'},'question':question,'split':'train'})
    return result


def prepare():
    rows=sources()
    audit={'sources':{p.relative_to(ROOT).as_posix():sha(p) for p in (*RUNTIME_CORPORA,SUPPLEMENT)},
           'provenance':'Project-authored synthetic DEVELOPMENT data, not independent human gold or an unseen benchmark.',
           'original_training_n':sum(r['source']!=SUPPLEMENT.name for r in rows),
           'original_topics':dict(Counter(r['target']['topic'] for r in rows if r['source']!=SUPPLEMENT.name)),
           'original_labels':dict(Counter(r['label'] for r in rows if r['source']!=SUPPLEMENT.name)),
           'supplement_n':sum(r['source']==SUPPLEMENT.name for r in rows)}
    seen={};conflicts=[];duplicates=0
    for row in rows:
        TrainingTarget.model_validate(row['target'])
        safe,blocked=normalize(row['question'])
        row['safe']=safe
        row['blocked']=blocked or ('unrecognized_context' if safe and safe['has_unrecognized_words'] else None)
        row['language']=row.get('language') or (safe['language_hint'] if safe else 'unknown')
        previous=json.dumps(row['previous'],sort_keys=True)
        row['key']=re.sub(r'\W+',' ',row['question'].casefold()).strip()+'|'+previous
        # Both raw and normalized equality participate in grouping. No duplicated
        # copy may land across partitions, even if its author supplied another ID.
        row['normalized_key']=json.dumps({'tokens':safe['safe_tokens'] if safe else None,
                                          'raw_when_blocked':row['key'] if row['blocked'] else None,
                                          'previous':row['previous']},sort_keys=True)
        if row['key'] in seen:
            duplicates+=1
            if seen[row['key']]['label']!=row['label']:
                conflicts.append([seen[row['key']]['id'],row['id']])
        else: seen[row['key']]=row
    normalized_seen={};normalized_conflicts=[]
    for row in rows:
        key=row['normalized_key']
        if key in normalized_seen and normalized_seen[key]['label']!=row['label']:
            normalized_conflicts.append([normalized_seen[key]['id'],row['id']])
        else: normalized_seen[key]=row
    audit['normalized_conflicting_id_pairs']=normalized_conflicts
    conflicts+=normalized_conflicts
    # Quarantine all contradictory exact inputs rather than silently relabel them.
    bad={i for pair in conflicts for i in pair}
    rows=[r for r in rows if r['id'] not in bad]
    unique={}
    for row in rows: unique.setdefault(row['key'],row)
    rows=list(unique.values())
    audit.update(exact_duplicate_copies=duplicates,conflicting_id_pairs=conflicts,
                 usable_rows=len(rows),guard_outcomes=dict(Counter(r['blocked'] or 'admitted' for r in rows)))
    return rows,audit


def partitions(rows):
    from difflib import SequenceMatcher
    import numpy as np
    from sklearn.model_selection import StratifiedGroupKFold
    parent=list(range(len(rows)))
    def find(i):
        while parent[i]!=i: parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j): parent[find(j)]=find(i)
    seen={}
    for i,row in enumerate(rows):
        for key in ('family:'+row['source']+':'+row['family'],'exact:'+row['key'],'normalized:'+row['normalized_key']):
            if key in seen: union(i,seen[key])
            else: seen[key]=i
    # Conservative lexical near-duplicate components. Connected chains stay
    # together; the threshold is fixed before predictions, never adjusted to fit.
    for i,a in enumerate(rows):
        a_words=set(a['key'].split('|')[0].split())
        for j in range(i):
            b=rows[j]
            if a['previous']!=b['previous']: continue
            b_words=set(b['key'].split('|')[0].split())
            if len(a_words|b_words) and len(a_words&b_words)/len(a_words|b_words)>=.75 and SequenceMatcher(None,a['key'],b['key']).ratio()>=.88:
                union(i,j)
    groups=np.array([find(i) for i in range(len(rows))])
    labels=np.array([r['target']['topic'] for r in rows])
    splitter=StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=20261120)
    folds=list(splitter.split(np.zeros(len(rows)),labels,groups))
    # Partition choice uses class support only, never a model's predictions.
    for validation in range(5):
        for calibration in range(5):
            if validation==calibration: continue
            val=set(folds[validation][1]);cal=set(folds[calibration][1])
            train=set(range(len(rows)))-val-cal
            admitted=[i for i in train if not rows[i]['blocked']]
            support=Counter(rows[i]['target']['topic'] for i in admitted)
            if all(support[t]>=2 for t in TOPICS):
                result={'train':[int(i) for i in sorted(train)],'calibration':[int(i) for i in sorted(cal)],'comparison':[int(i) for i in sorted(val)]}
                group_sets={part:{groups[i] for i in indices} for part,indices in result.items()}
                assert not group_sets['train']&group_sets['calibration'] and not group_sets['train']&group_sets['comparison'] and not group_sets['calibration']&group_sets['comparison']
                for part,indices in result.items():
                    for i in indices: rows[i]['partition']=part;rows[i]['group']=int(groups[i])
                return result,{'groups':len(set(groups)), 'largest_group':max(Counter(groups).values()),
                               'seed':20261120,'near_rule':'Jaccard>=0.75 and character similarity>=0.88; same typed previous context',
                               'support':{p:dict(Counter(rows[i]['target']['topic'] for i in ids)) for p,ids in result.items()}}
    raise ValueError('No leakage-safe split supports every topic in training. Collect genuinely distinct reviewed families; do not weaken the split.')


def text(row,view='original'):
    if row['blocked']: raise ValueError('Guarded/private/unresolved input cannot reach a classifier.')
    value=row['question'] if view=='original' else ' '.join(row['safe']['safe_tokens'])
    context=row['previous']
    if context:
        value+=' [validated previous context: '+json.dumps(context,sort_keys=True)+']'
    return 'query: '+value


def balanced_cases():
    path=Path(__file__).parent/'data/balanced-development.json'
    payload=json.loads(path.read_text(encoding='utf-8'))
    result=[]
    for i,line in enumerate(payload['cases']):
        family,label,language,question=line.split('|',3)
        previous=None
        if label=='follow_up':
            previous=Context(knowledge='privacy').model_dump() if family=='knowledge-elaboration' else Context(tools=['get_player_scores'],period='today',source='simulator',score_page=1).model_dump()
        safe,blocked=normalize(question)
        result.append({'id':f'balanced-dev-{i+1:03d}','family':family,'label':label,
                       'target':{'topic':label.split(':')[0]},'language':language,
                       'source':path.name,'question':question,'previous':previous,'safe':safe,
                       'blocked':blocked or ('unrecognized_context' if safe and safe['has_unrecognized_words'] else None)})
    assert len(result)==130 and Counter(r['target']['topic'] for r in result)=={t:10 for t in TOPICS}
    return result
