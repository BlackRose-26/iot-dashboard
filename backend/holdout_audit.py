"""Freeze-only evaluation support. Application modules must never import the holdout."""
import ast
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re

from app.assistant import Context, PROMPT, RoutingPlan, normalize
from app.assistant_learning import RUNTIME_CORPORA, corpus_digest, seed_examples
from evaluate_routing import route_label

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT/'backend/evaluation'
DATASET = DIRECTORY/'holdout-v1.json'
MANIFEST = DIRECTORY/'holdout-v1.manifest.json'
TOPICS = tuple(RoutingPlan.model_json_schema()['properties']['topic']['enum'])
TAGLISH_INDICES = {
    'overview':{1,3,7,9,11,13,17,19,23},
    'scores':set(range(1,22,2)), 'definition':{1,4,7,10,13,16,19,22},
    'knowledge':set(range(1,22,2)), 'social':{1,3,5,8,11,14,17,20,23},
    'unsupported':set(range(1,22,2)),
}
STOP = set('a an the is are was were what how which why who me my our this that it its they their them of in on at to for from and or please paki po ang ng sa ba mga naman'.split())


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_key(text):
    return ' '.join(re.findall(r'\w+',text.casefold()))


def feature_key(text):
    safe,blocked = normalize(text)
    if blocked or safe['has_unrecognized_words']:
        return None
    return tuple(safe['safe_tokens'])


def inventory():
    tree = ast.parse((DIRECTORY/'cases_v1.py').read_text(encoding='utf-8'))
    return ast.literal_eval(next(node.value for node in tree.body if isinstance(node,ast.Assign)
                                and any(isinstance(t,ast.Name) and t.id=='INVENTORY' for t in node.targets)))


def previous_context(index):
    contexts = [
        {'tools':['get_player_scores'],'period':'today'},
        {'tools':['get_player_scores'],'period':'today'},
        {'tools':['get_event_summary'],'metrics':['wins']},
        {'tools':['get_event_summary'],'metrics':['wins']},
        {'tools':['get_play_trend'],'period':'today'},
        {'tools':['get_play_trend'],'period':'today'},
        {'tools':['get_player_scores']}, {'tools':['get_player_scores']},
        {'tools':['get_top_scores'],'source':'device'}, {'tools':['get_top_scores'],'source':'device'},
        {'tools':['get_event_summary'],'source':'device'}, {'tools':['get_event_summary'],'source':'device'},
        {'knowledge':'architecture'}, {'knowledge':'architecture'},
        {'tools':['get_event_summary'],'detailed':True}, {'tools':['get_event_summary'],'detailed':True},
        {'tools':['get_level_statistics'],'level':7}, {'tools':['get_level_statistics'],'level':7},
        {'tools':['get_event_summary'],'metrics':['average_score']},
        {'tools':['get_event_summary'],'metrics':['average_score']},
        {'tools':['get_player_scores'],'score_page':1}, {'tools':['get_player_scores'],'score_page':1},
        {'tools':['get_score_distribution'],'period':'today'},
        {'tools':['get_score_distribution'],'period':'today'}, {'knowledge':'queue_flow'},
    ]
    expectation = {}
    if index in (0,1): expectation['period']='yesterday'
    if index in (2,3,19): expectation['period']='today'
    if index in (4,5): expectation['period']='last_7_days'
    if index in (6,7,18): expectation['source']='device'
    if index in (8,9,19): expectation['source']='simulator'
    if index in (10,11): expectation['source']='all'
    if index in (12,13,24): expectation['detailed']=True
    if index in (14,15): expectation['detailed']=False
    if index in (20,21): expectation['score_page']=2
    if index in (22,23): expectation['period']='event_to_date'
    if index==18: expectation['period']='yesterday'
    prior = Context.model_validate(contexts[index]).model_dump()
    expectation.update({key:prior[key] for key in ('tools','definition','knowledge')})
    return prior,expectation


def build_rows():
    groups = inventory()
    assert set(groups)==set(TOPICS)
    rows = []
    for topic,body in groups.items():
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        assert len(lines)==25,(topic,len(lines))
        for index,line in enumerate(lines):
            parts = line.split('|')
            family,question = parts[:2]
            target = {'topic':topic}
            if topic in ('definition','knowledge','social'):
                assert len(parts)==3
                target[topic]=parts[2]
            RoutingPlan.model_validate(target)
            taglish=TAGLISH_INDICES.get(topic,set(range(1,24,2)))
            row = {'id':f'{topic}-{index+1:02d}','family':topic+'/'+family,'language':'taglish' if index in taglish else 'en',
                   'question':question,'target':target}
            if topic=='follow_up':
                row['previous'],row['expected_context'] = previous_context(index)
            # Capabilities/help can legitimately use the reviewed assistant card.
            if topic=='social' and target['social']=='help':
                row['acceptable_labels']=['social:help','knowledge:assistant']
            rows.append(row)
    return rows


def reference_questions():
    references = []
    for path in (*RUNTIME_CORPORA,ROOT/'backend/data/assistant-routing-validation.json'):
        references.extend((path.name+'/'+row['id'],row['question']) for row in json.loads(path.read_text(encoding='utf-8'))['examples'])
    # Include the older manually-authored local integration probes as seen data.
    tree = ast.parse((ROOT/'backend/check_assistant_quality.py').read_text(encoding='utf-8'))
    for node in ast.walk(tree):
        if isinstance(node,ast.Tuple) and len(node.elts)==4 and all(isinstance(t,ast.Constant) and isinstance(t.value,str) for t in node.elts[:2]):
            references.append(('previous-probe/'+node.elts[0].value,node.elts[1].value))
    for path in sorted((ROOT/'backend/tests').glob('test_assistant*.py')):
        tree=ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and len(node.value.split())>=4:
                references.append((f'{path.name}/L{node.lineno}',node.value))
    path=ROOT/'backend/tests/test_routing_quality.py'
    for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
        if isinstance(node,ast.Constant) and isinstance(node.value,str) and len(node.value.split())>=4:
            references.append((f'{path.name}/L{node.lineno}',node.value))
    for index,match in enumerate(re.findall(r'\[[^\n\]]+\]',PROMPT)):
        try:
            values = ast.literal_eval(match)
            if isinstance(values,list) and all(isinstance(v,str) for v in values):
                references.append((f'prompt-array/{index}',' '.join(values)))
        except (SyntaxError,ValueError): pass
    for index,value in enumerate(re.findall(r'"([^"\n]+)"',PROMPT)):
        if len(value.split())>=4:
            references.append((f'prompt-text/{index}',value))
    return references


def overlap_audit(rows):
    refs = reference_questions()
    exact_raw = {text_key(question):identity for identity,question in refs}
    exact_safe = {key:identity for identity,question in refs if (key:=feature_key(question))}
    prepared = [(identity,text_key(question),set(text_key(question).split())-STOP) for identity,question in refs]
    duplicates,near = [],[]
    seen = {}
    within,within_near = [],[]
    for row in rows:
        raw = text_key(row['question']); words=set(raw.split())-STOP
        safe = feature_key(row['question'])
        reference = exact_raw.get(raw) or (exact_safe.get(safe) if safe else None)
        if reference: duplicates.append({'id':row['id'],'reference':reference})
        if raw in seen: within.append([seen[raw],row['id']])
        seen[raw]=row['id']
        for identity,old,old_words in prepared:
            overlap = len(words & old_words)/len(words | old_words) if words|old_words else 0
            if len(raw)>=24 and overlap>=.7 and SequenceMatcher(None,raw,old,autojunk=False).ratio()>=.84:
                near.append({'id':row['id'],'reference':identity,'content_jaccard':round(overlap,3)})
    for index,row in enumerate(rows):
        raw=text_key(row['question']);words=set(raw.split())-STOP
        for other in rows[index+1:]:
            old=text_key(other['question']);old_words=set(old.split())-STOP
            overlap=len(words&old_words)/len(words|old_words) if words|old_words else 0
            if len(raw)>=24 and overlap>=.7 and SequenceMatcher(None,raw,old,autojunk=False).ratio()>=.84:
                within_near.append([row['id'],other['id']])
    return {'reference_count':len(refs),'exact_collisions':duplicates,'near_duplicates':near,
            'within_set_exact':within,'within_set_near':within_near,
            'policy':'Reject exact raw/usable-normalized overlaps and near pairs with content Jaccard>=0.70 plus character similarity>=0.84; thresholds fixed before predictions.'}


def runtime_fingerprint():
    paths = sorted((ROOT/'backend/app').glob('assistant*.py'))+[ROOT/'backend/app/analytics.py']
    return {'code':{path.relative_to(ROOT).as_posix():sha(path) for path in paths},
            'corpora':{path.relative_to(ROOT).as_posix():sha(path) for path in RUNTIME_CORPORA},
            'runtime_corpus_sha256':corpus_digest(),'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest()}


def evaluator_fingerprint():
    paths=[ROOT/'backend'/name for name in ('holdout_audit.py','holdout_metrics.py','evaluate_holdout.py')]
    paths.append(DIRECTORY/'cases_v1.py')
    return {path.relative_to(ROOT).as_posix():sha(path) for path in paths}


def freeze():
    if MANIFEST.exists() or DATASET.exists():
        raise ValueError('This holdout version is already frozen; do not rewrite it.')
    rows = build_rows()
    audit = overlap_audit(rows)
    if any(audit[key] for key in ('exact_collisions','near_duplicates','within_set_exact','within_set_near')):
        print(json.dumps(audit,indent=2))
        raise ValueError('Resolve overlaps before freezing, without running model predictions.')
    payload = {'version':'holdout-v1','provenance':'New synthetic developer-authored evaluation only; not independently human-labelled or guaranteed absent from foundation-model pretraining.',
               'policy':'Never load into runtime training, aliases, vocabulary or few-shot retrieval. First results are a one-shot held-out measurement; later reuse is regression only.',
               'examples':rows}
    DATASET.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest = {'dataset_sha256':sha(DATASET),'n':len(rows),'counts':dict(Counter(r['target']['topic'] for r in rows)),
                'language_counts':dict(Counter(r['language'] for r in rows)),
                'subtype_counts':dict(Counter(route_label(r['target']) for r in rows)),
                'families_per_intent':{topic:len({r['family'] for r in rows if r['target']['topic']==topic}) for topic in TOPICS},
                'audit':audit,'runtime':runtime_fingerprint(),'evaluation_code':evaluator_fingerprint(),
                'authoring':'Manual literal inventory; no prediction-based selection or application changes.'}
    assert min(manifest['families_per_intent'].values())>=10
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return manifest


def verify_frozen():
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    if sha(DATASET)!=manifest['dataset_sha256'] or runtime_fingerprint()!=manifest['runtime']:
        raise ValueError('Frozen dataset or runtime fingerprint changed. This run is invalid.')
    if evaluator_fingerprint()!=manifest['evaluation_code']:
        raise ValueError('Frozen evaluation code changed. This run is invalid.')
    rows=json.loads(DATASET.read_text(encoding='utf-8'))['examples']
    if overlap_audit(rows)!=manifest['audit']:
        raise ValueError('The evaluation separation audit changed.')
    return manifest,rows


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['audit','freeze','verify'])
    operation=parser.parse_args().operation
    if operation=='audit': print(json.dumps(overlap_audit(build_rows()),indent=2))
    elif operation=='freeze': print(json.dumps(freeze(),indent=2))
    else: print(json.dumps({'verified':True,'n':verify_frozen()[0]['n']}))
