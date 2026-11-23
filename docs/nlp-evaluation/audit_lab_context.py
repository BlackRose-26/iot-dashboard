"""Post-hoc context invariance diagnostic. Same public questions, not new test cases."""
import argparse
import asyncio
from collections import Counter
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
from nlp_lab.run import sha,write,MODEL,code_hashes,protected
from nlp_lab.data import text
from app.assistant import Context


def open_run(directory):
    protocol=json.loads((directory/'protocol.json').read_text(encoding='utf-8'))
    def canonical(mapping):
        result={(ROOT/k).resolve().relative_to(ROOT).as_posix():value for k,value in mapping.items()}
        if len(result)!=len(mapping): raise ValueError('Duplicate canonical source paths.')
        return result
    # The Windows CMD entrypoint records scripts/../backend paths; importing the
    # same unchanged module records backend paths. Compare canonical paths AND
    # every byte hash, without modifying the original protocol or source code.
    if canonical(code_hashes())!=canonical(protocol['source_code']) or protected()!=protocol['protected'] or sha(directory/'data.json')!=protocol['prepared_data_sha256']:
        raise ValueError('Frozen source/data/runtime changed.')
    data=json.loads((directory/'data.json').read_text(encoding='utf-8'))
    return protocol,data['rows'],data['balanced']


def audit(directory):
    protocol,rows,external=open_run(directory)
    subset=[r for r in external if r['label']!='follow_up']
    contexts=[Context(tools=['get_queue_summary']).model_dump(),Context(knowledge='privacy').model_dump(),
              Context(tools=['get_player_scores'],source='simulator',period='yesterday').model_dump()]
    stressed=[{**r,'previous':contexts[i%len(contexts)]} for i,r in enumerate(subset)]
    names=['ollama-v11','tfidf-original','tfidf-normalized','e5-frozen-linear','setfit-multilingual']
    manifest={'kind':'post-hoc paired context diagnostic, not independent new cases',
              'original_protocol_sha256':sha(directory/'protocol.json'),'diagnostic_code_sha256':sha(Path(__file__)),
              'ids':[r['id'] for r in subset],'contexts':contexts,
              'models':{name:sha(directory/(name+'.json')) for name in names}}
    write(directory/'context-stress.protocol.json',manifest)
    from nlp_lab.baseline import predict
    changed={'ollama-v11':asyncio.run(predict(stressed,[rows[i] for i in protocol['splits']['train']]))}
    import torch
    torch.set_num_threads(4)
    import joblib
    from nlp_lab.models import SparseModel,DenseModel
    from sentence_transformers import SentenceTransformer
    for name in names[1:]:
        if name.startswith('tfidf'):
            model=SparseModel();model.encoder=joblib.load(directory/(name+'-vectorizer.joblib'))
            view=name.split('-')[1]
        else:
            path=directory/'setfit-encoder' if name=='setfit-multilingual' else MODEL
            model=DenseModel(SentenceTransformer(str(path),device='cpu',local_files_only=True,trust_remote_code=False));view='original'
        model.heads=joblib.load(directory/(name+'-heads.joblib'))
        predictions=[]
        for row in stressed:
            actual='unsupported' if row['blocked'] else str(model.predict([text(row,view)])[0][0])
            predictions.append({'id':row['id'],'expected':row['label'],'predicted':actual})
        changed[name]=predictions
        del model
    result={'limits':manifest['kind'],'n_questions':len(subset),'candidates':{}}
    for name in names:
        before=json.loads((directory/(name+'.json')).read_text())['reports']['balanced_new_development']['cases']
        before={r['id']:r for r in before}
        cases=changed[name]
        result['candidates'][name]={'n':len(cases),
            'primary_correct_before':sum(before[c['id']]['predicted'].split(':')[0]==c['expected'].split(':')[0] for c in cases),
            'primary_correct_after':sum(c['predicted'].split(':')[0]==c['expected'].split(':')[0] for c in cases),
            'originally_correct_became_wrong':sum(before[c['id']]['predicted'].split(':')[0]==c['expected'].split(':')[0] and c['predicted'].split(':')[0]!=c['expected'].split(':')[0] for c in cases),
            'predicted_follow_up_after':sum(c['predicted'].split(':')[0]=='follow_up' for c in cases),
            'cases':cases}
    open_run(directory)
    write(directory/'context-stress.json',result)
    print(json.dumps({k:{field:value for field,value in v.items() if field!='cases'} for k,v in result['candidates'].items()},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',required=True)
    args=parser.parse_args()
    if any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run): raise ValueError('Invalid run ID')
    audit(ROOT/'.tools/nlp-lab'/args.run)
