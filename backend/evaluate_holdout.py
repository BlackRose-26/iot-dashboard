"""One-shot service-level holdout. Never repairs the predictor or learns from these cases."""
import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
import argparse
import asyncio
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time

import httpx

from app.assistant import Assistant, Question
from app.database import execute
from app.security import DUMMY_HASH
from evaluate_routing import route_label
from holdout_audit import DATASET, ROOT, TOPICS, sha, verify_frozen
from holdout_metrics import summarize


class ObservedAssistant(Assistant):
    """Observe the existing returned label; do not change inference or results."""
    last_target=None
    async def _ask(self,*args,**kwargs):
        result=await super()._ask(*args,**kwargs)
        self.last_target=result.get('_training_target')
        return result


def score(row,result,target):
    expected=route_label(row['target'])
    status=result['status']
    if status in ('refused','needs_clarification'):
        predicted='unsupported'
    elif target:
        predicted=route_label(target)
    elif row.get('previous') and status=='conversation' and result.get('reason')=='preference':
        predicted='follow_up'
    else:
        predicted='unclassified'
    acceptable=row.get('acceptable_labels',[expected])
    context=result.get('context',{})
    continuity=all(context.get(key)==value for key,value in row.get('expected_context',{}).items())
    # Knowledge follow-ups may be rendered with their resolved knowledge label.
    if row['target']['topic']=='follow_up' and row.get('previous',{}).get('knowledge'):
        acceptable=[*acceptable,'knowledge:'+row['previous']['knowledge']]
    accepted=predicted in acceptable and continuity and status in ('ok','no_data','conversation','refused','needs_clarification')
    if row['target']['topic']!='unsupported' and status in ('refused','needs_clarification'):
        accepted=False
    return {'id':row['id'],'family':row['family'],'language':row['language'],'expected_label':expected,
            'predicted_label':predicted,'expected_topic':row['target']['topic'],'predicted_topic':predicted.split(':')[0],
            'exact_label':expected==predicted,'accepted':accepted,'continuity_correct':continuity,
            'status':status,'reason':result.get('reason'),'tools':context.get('tools',[])}


async def evaluate(output):
    manifest,rows=verify_frozen()
    ledger=DATASET.with_suffix('.consumed.json')
    if output.exists() or ledger.exists():
        raise ValueError('This holdout version was already consumed or output exists. Never silently rerun it as unseen data.')
    sys.path.insert(0,str(ROOT/'backend/tests'))
    from test_player_flow import environment,join,post
    generator=environment.__wrapped__()
    app,admin,token,engine,settings=next(generator)
    assistant=ObservedAssistant(settings,engine)
    cases=[]
    try:
        players=[join(app,token,index) for index in range(4)]
        for outcome in ('win','loss'):
            for path in ('/api/admin/simulator/ready','/api/admin/queue/call-next','/api/admin/simulator/start','/api/admin/simulator/'+outcome):
                assert post(admin,path).status_code==200
        with engine.begin() as c:
            for index in range(1,1+(len(rows)-1)//8):
                execute(c,"INSERT INTO staff_users(id,username,password_hash,role) VALUES(:id,:name,:hash,'admin')",
                        id=index+1,name=f'synthetic-holdout-{index}',hash=DUMMY_HASH)
        state=await assistant.prepare();began=time.monotonic()
        while state['reason']=='warming' and time.monotonic()-began<125:
            await asyncio.sleep(1);state=await assistant.status()
        if not state['available']: raise RuntimeError('Prepare the local model before consuming the holdout.')
        async with httpx.AsyncClient(base_url=settings.ollama_url,trust_env=False,timeout=5) as client:
            tags=(await client.get('/api/tags')).json()['models']
            model=next({'name':m['name'],'digest':m['digest']} for m in tags if m['name']==settings.ollama_model)
        evaluator_hash=sha(Path(__file__).resolve())
        stamp={'started_at':datetime.now(timezone.utc).isoformat(),'dataset_sha256':manifest['dataset_sha256'],
               'model':model,'evaluator_sha256':evaluator_hash,'status':'running'}
        with ledger.open('x',encoding='utf-8') as stream: json.dump(stamp,stream,indent=2)
        for index,row in enumerate(rows):
            began=time.monotonic();assistant.last_target=None
            try:
                reply=await assistant.ask(Question(question=row['question'],previous=row.get('previous'),use_memory=False),1+index//8)
                result=score(row,reply,assistant.last_target)
            except Exception as error:
                result=score(row,{'status':'error','reason':type(error).__name__},None)
            result['seconds']=round(time.monotonic()-began,4)
            cases.append(result)
            # Persist progress without storing answers, IDs, question text or examples.
            output.parent.mkdir(parents=True,exist_ok=True)
            partial=output.with_suffix('.partial.json')
            partial.write_text(json.dumps({'status':'running','cases':cases},indent=2),encoding='utf-8')
            if (index+1)%25==0:
                print(json.dumps({'evaluated':index+1,'total':len(rows),'intent':row['target']['topic'],
                                  'accepted_so_far':sum(r['accepted'] for r in cases)}),flush=True)
        verify_frozen()
        if sha(Path(__file__).resolve())!=evaluator_hash: raise RuntimeError('Evaluator changed during inference.')
        report={'measured_at':datetime.now(timezone.utc).isoformat(),'dataset_sha256':manifest['dataset_sha256'],
                'model':model,'component':'Core Assistant.ask service with synthetic XAMPP data and private memory disabled',
                'limits':'First-use project holdout, synthetic developer-authored; not independently human-labelled or real-user factual-answer accuracy.',
                'metrics':summarize(cases,TOPICS),'cases':cases}
        with output.open('x',encoding='utf-8') as stream: json.dump(report,stream,indent=2)
        stamp.update(status='complete',completed_at=report['measured_at'],result_sha256=sha(output))
        ledger.write_text(json.dumps(stamp,indent=2),encoding='utf-8')
        print(json.dumps(report['metrics'],indent=2),flush=True)
    finally:
        await assistant.close()
        for player in locals().get('players',[]): player.close()
        try: next(generator)
        except StopIteration: pass


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    asyncio.run(evaluate(args.output.resolve()))
