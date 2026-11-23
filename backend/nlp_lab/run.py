"""Reproducible local DEVELOPMENT comparison. Never modifies or activates runtime AI."""
import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'
os.environ['TOKENIZERS_PARALLELISM']='false'
import argparse
import asyncio
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nlp_lab.data import ROOT,TOPICS,balanced_cases,partitions,prepare,sha,text

REVISION='614241f622f53c4eeff9890bdc4f31cfecc418b3'
MODEL=ROOT/'.tools/hf-public/models--intfloat--multilingual-e5-small/snapshots'/REVISION
ARTIFACTS=ROOT/'.tools/nlp-lab'


def write(path,value):
    payload=json.dumps(value,indent=2,ensure_ascii=False)
    with path.open('x',encoding='utf-8') as stream: stream.write(payload)


def protected():
    paths=list((ROOT/'backend/app').glob('assistant*.py'))
    paths+=list((ROOT/'backend/evaluation').glob('*'))
    paths+=[ROOT/'backend/data'/n for n in ('assistant-routing.json','assistant-interactions.json','assistant-behavioral.json','assistant-routing-contrasts.json','assistant-language-lexicon.json')]
    paths+=[ROOT/'docs/nlp-evaluation/results'/n for n in ('holdout-v1.json','holdout-v1-regression-v10.json','holdout-v1-regression-v11.json')]
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths if p.is_file()}


def code_hashes():
    paths=list(Path(__file__).parent.glob('*.py'))+list((Path(__file__).parent/'data').glob('*.json'))
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}


def freeze(directory):
    directory.mkdir(parents=True,exist_ok=False)
    rows,audit=prepare();splits,grouping=partitions(rows)
    external=balanced_cases()
    # No silently duplicated question may be called the external development set.
    from difflib import SequenceMatcher
    import re
    exact=[];near=[]
    for case in external:
        value=re.sub(r'\W+',' ',case['question'].casefold()).strip()
        words=set(value.split())
        for row in rows:
            other=row['key'].split('|')[0]
            if value==other and case['previous']==row['previous']: exact.append([case['id'],row['id']])
            other_words=set(other.split())
            if words|other_words and len(words&other_words)/len(words|other_words)>=.75 and SequenceMatcher(None,value,other).ratio()>=.88:
                near.append([case['id'],row['id']])
    audit['balanced_development_overlap']={'exact':exact,'high_lexical_near':near}
    if exact: raise ValueError('Exact overlap in new development questions; resolve before predictions.')
    protocol={'status':'frozen-development-only','created_at':datetime.now(timezone.utc).isoformat(),
              'not_unseen':'Existing project synthetic training inputs; family-grouped train/calibration/comparison plus new synthetic balanced development probes. Independent human review is pending.',
              'audit':audit,'grouping':grouping,'splits':splits,
              'source_code':code_hashes(),'protected':protected(),'model':'intfloat/multilingual-e5-small',
              'model_revision':REVISION,'setfit':{'steps':40,'batch_size':8,'iterations':3,'seed':20261120,'body_max_length':256},
              'operating_policy':'Choose on calibration only: >=90% accepted PRIMARY precision and zero calibration OOS false accepts; else abstain. This is an experimental target, not a proven safety guarantee.',
              'limits':'Classifier label metrics only. No factual answers/database/browser/hardware evaluation. Baseline retains static social/prompt priors; source-comparison rows were previously present in its public corpora.'}
    write(directory/'data.json',{'rows':rows,'balanced':external})
    protocol['prepared_data_sha256']=sha(directory/'data.json')
    write(directory/'protocol.json',protocol)
    print(json.dumps({'directory':str(directory),'audit':audit,'grouping':grouping},indent=2),flush=True)


def load(directory):
    protocol=json.loads((directory/'protocol.json').read_text(encoding='utf-8'))
    if protocol['source_code']!=code_hashes() or protocol['protected']!=protected() or protocol['prepared_data_sha256']!=sha(directory/'data.json'):
        raise ValueError('Frozen code/data/runtime changed; preserve this run and create another run ID.')
    data=json.loads((directory/'data.json').read_text(encoding='utf-8'))
    return protocol,data['rows'],data['balanced']


def summarize(cases):
    from sklearn.metrics import f1_score
    n=len(cases);supported=[c for c in cases if c['expected'].split(':')[0]!='unsupported']
    oos=[c for c in cases if c['expected']=='unsupported']
    answered=[c for c in supported if c.get('decision','answer')=='answer' and c['predicted'] not in ('unsupported','error')]
    return {'n':n,'exact_label_correct':sum(c['expected']==c['predicted'] for c in cases),
            'primary_correct':sum(c['expected'].split(':')[0]==c['predicted'].split(':')[0] for c in cases),
            'primary_macro_f1':float(f1_score([c['expected'].split(':')[0] for c in cases],[c['predicted'].split(':')[0] for c in cases],labels=list(TOPICS),average='macro',zero_division=0)),
            'valid_answer_coverage':len(answered)/len(supported) if supported else None,
            'answered_valid_primary_precision':sum(c['expected'].split(':')[0]==c['predicted'].split(':')[0] for c in answered)/len(answered) if answered else None,
            'oos_n':len(oos),'oos_false_classifications':sum(c['predicted'] not in ('unsupported','error','clarify') for c in oos),
            'oos_false_answers':sum(c.get('decision','answer')=='answer' and c['predicted'] not in ('unsupported','error','clarify') for c in oos),
            'errors':sum(c['predicted']=='error' for c in cases),
            'per_primary':{topic:{'n':sum(c['expected'].split(':')[0]==topic for c in cases),
                                  'primary_correct':sum(c['expected'].split(':')[0]==topic==c['predicted'].split(':')[0] for c in cases)} for topic in TOPICS}}


def evaluate_model(model,rows,view,operating,temperature=1):
    import numpy as np
    result=[]
    for row in rows:
        began=time.perf_counter()
        if row['blocked']:
            label='unsupported';decision='reject';probability=None
        else:
            labels,probabilities=model.predict([text(row,view)])
            from nlp_lab.models import scaled
            probabilities=scaled(probabilities,temperature)
            label=str(labels[0]);ordered=np.sort(probabilities[0]);probability=float(ordered[-1])
            decision='reject' if label=='unsupported' else 'answer' if probability>=operating['confidence'] and float(ordered[-1]-ordered[-2])>=operating['margin'] else 'clarify'
        result.append({'id':row['id'],'expected':row['label'],'predicted':label,'decision':decision,
                       'confidence':probability,'guard':row['blocked'],'language':row['language'],
                       'seconds':time.perf_counter()-began})
    return result


def finish_model(directory,name,model,rows,external,view,training_seconds):
    from nlp_lab.models import policy,fit_temperature,scaled
    protocol,_,_=load(directory)
    calibration=[rows[i] for i in protocol['splits']['calibration'] if not rows[i]['blocked']]
    _,probabilities=model.predict([text(row,view) for row in calibration])
    truth=[r['target']['topic'] for r in calibration]
    calibration_fit=fit_temperature(probabilities,truth,model.heads.primary.classes_)
    operating=policy(scaled(probabilities,calibration_fit['temperature']),truth,model.heads.primary.classes_)
    partitions_to_test={'grouped_source_development':[rows[i] for i in protocol['splits']['comparison']],
                        'balanced_new_development':external}
    reports={}
    for key,subset in partitions_to_test.items():
        cases=evaluate_model(model,subset,view,operating,calibration_fit['temperature'])
        reports[key]={'argmax':summarize(cases),'selective':summarize([{**c,'predicted':c['predicted'] if c['decision'] in ('answer','reject') else 'clarify'} for c in cases]),'cases':cases}
    # Public, developer-reviewed wording probes form an offline counterfactual,
    # never a runtime privacy bypass or additional training/calibration data.
    from app.assistant import normalize,Context
    public=json.loads((Path(__file__).parent/'data/public-diagnostics.json').read_text(encoding='utf-8'))
    diagnostics=[]
    for case in public['examples']:
        safe,blocked=normalize(case['question'])
        if blocked=='refused': raise ValueError('Privacy/control refusal cannot be bypassed by a wording probe.')
        diagnostics.append({**case,'previous':Context.model_validate(case['previous']).model_dump() if case.get('previous') else None,
                            'safe':safe,'blocked':blocked or ('unrecognized_context' if safe and safe['has_unrecognized_words'] else None),
                            'language':safe['language_hint'] if safe else 'unknown'})
    guarded=evaluate_model(model,diagnostics,view,operating,calibration_fit['temperature'])
    reports['public_wording_gated']={'argmax':summarize(guarded),'cases':guarded}
    if view=='original':
        approved=[{**case,'blocked':None} for case in diagnostics]
        counterfactual=evaluate_model(model,approved,view,operating,calibration_fit['temperature'])
        reports['public_wording_reviewed_text_counterfactual']={'warning':'Only these fixed synthetic public probes. Not raw runtime permission, privacy validation, training data or unseen accuracy.',
                                                              'argmax':summarize(counterfactual),'cases':counterfactual}
    result={'candidate':name,'training_seconds':training_seconds,'view':view,'policy':operating,'calibration':calibration_fit,
            'scope':'Offline synthetic DEVELOPMENT classification; no activation or independent accuracy claim.',
            'protocol_sha256':sha(directory/'protocol.json'),'reports':reports}
    write(directory/(name+'.json'),result)
    import joblib
    joblib.dump(model.heads,directory/(name+'-heads.joblib'))
    if name.startswith('tfidf'): joblib.dump(model.encoder,directory/(name+'-vectorizer.joblib'))
    print(json.dumps({'candidate':name,'balanced':reports['balanced_new_development']['argmax'],'policy':operating},indent=2),flush=True)


def run_sparse(directory):
    from nlp_lab.models import SparseModel
    protocol,rows,external=load(directory)
    training=[rows[i] for i in protocol['splits']['train'] if not rows[i]['blocked']]
    for view in ('original','normalized'):
        name='tfidf-'+view
        if (directory/(name+'.json')).exists(): raise ValueError('Existing candidate result is immutable.')
        began=time.perf_counter()
        model=SparseModel().fit([text(r,view) for r in training],training)
        finish_model(directory,name,model,rows,external,view,time.perf_counter()-began)


def run_dense(directory,finetune):
    import torch
    torch.set_num_threads(4)
    torch.manual_seed(20261120)
    from sentence_transformers import SentenceTransformer
    from nlp_lab.models import DenseModel
    protocol,rows,external=load(directory)
    training=[rows[i] for i in protocol['splits']['train'] if not rows[i]['blocked']]
    name='setfit-multilingual' if finetune else 'e5-frozen-linear'
    if (directory/(name+'.json')).exists(): raise ValueError('Existing candidate result is immutable.')
    began=time.perf_counter()
    if finetune:
        from datasets import Dataset
        from setfit import SetFitModel,Trainer,TrainingArguments
        model=SetFitModel.from_pretrained(str(MODEL),local_files_only=True,device='cpu',trust_remote_code=False)
        def parameter_digest():
            parameter=next(p for p in model.model_body.parameters() if p.ndim==2 and 10000<p.numel()<1000000)
            return hashlib.sha256(parameter.detach().cpu().numpy().tobytes()).hexdigest()
        before=parameter_digest()
        # Contrastive body sees a balanced capped subset; final hierarchical
        # heads use all training rows with balanced class weights.
        sample=[];counts=Counter()
        for row in training:
            topic=row['target']['topic']
            if counts[topic]<16: sample.append(row);counts[topic]+=1
        data=Dataset.from_dict({'text':[text(r) for r in sample],
                                'label':[list(TOPICS).index(r['target']['topic']) for r in sample]})
        args=TrainingArguments(output_dir=str(directory/'setfit-checkpoints'),batch_size=8,num_epochs=1,
                               max_steps=40,num_iterations=3,max_length=256,seed=20261120,
                               report_to='none',save_strategy='no',eval_strategy='no',show_progress_bar=False)
        trainer=Trainer(model=model,args=args,train_dataset=data)
        trainer.train()
        after=parameter_digest()
        write(directory/'setfit-training.json',{'steps':40,'body_parameter_before':before,'body_parameter_after':after,
                                              'body_weights_changed':before!=after,'subset_n':len(sample),'subset_counts':dict(counts)})
        encoder=model.model_body
        encoder.save(str(directory/'setfit-encoder'),safe_serialization=True)
    else:
        encoder=SentenceTransformer(str(MODEL),device='cpu',local_files_only=True,trust_remote_code=False)
        encoder.max_seq_length=256
    candidate=DenseModel(encoder).fit([text(r) for r in training],training)
    finish_model(directory,name,candidate,rows,external,'original',time.perf_counter()-began)


def run_baseline(directory):
    from nlp_lab.baseline import predict
    protocol,rows,external=load(directory)
    target=directory/'ollama-v11.json'
    if target.exists(): raise ValueError('Existing baseline is immutable.')
    training=[rows[i] for i in protocol['splits']['train']]
    combined=[rows[i] for i in protocol['splits']['comparison']]+external
    cases=asyncio.run(predict(combined,training))
    cut=len(protocol['splits']['comparison'])
    result={'candidate':'ollama-v11','limits':'Actual routing with no-data renderers; no database. Train-only retrieval. Static prompt/social priors predate this split; grouped-source cases are seen development for this baseline.',
            'reports':{key:{'argmax':summarize(part),'cases':part} for key,part in
                       (('grouped_source_development',cases[:cut]),('balanced_new_development',cases[cut:]))}}
    load(directory)
    write(target,result)
    print(json.dumps({'candidate':'ollama-v11','balanced':result['reports']['balanced_new_development']['argmax']},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','sparse','encoder','setfit','ollama'])
    parser.add_argument('--run',required=True)
    args=parser.parse_args()
    if not args.run or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run):
        raise ValueError('Run ID must be a short lowercase identifier, not a path.')
    directory=ARTIFACTS/args.run
    if args.stage=='prepare': freeze(directory)
    elif args.stage=='sparse': run_sparse(directory)
    elif args.stage=='encoder': run_dense(directory,False)
    elif args.stage=='setfit': run_dense(directory,True)
    else: run_baseline(directory)


if __name__=='__main__': main()
