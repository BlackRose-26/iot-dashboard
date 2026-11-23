"""Actual local service development probes. Not unseen or general accuracy."""
import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
import argparse
import asyncio
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time

from app.assistant import Question
from app.database import execute
from app.security import DUMMY_HASH
from evaluate_holdout import ObservedAssistant,score
from holdout_audit import ROOT,runtime_fingerprint,sha
from holdout_metrics import summarize


async def check(output):
    sys.path.insert(0,str(ROOT/'backend/tests'))
    from test_assistant_public_language import DEVELOPMENT
    from test_player_flow import environment,join,post
    if output.exists(): raise ValueError('Keep earlier development measurements; choose a new output.')
    generator=environment.__wrapped__()
    app,admin,token,engine,settings=next(generator)
    service=ObservedAssistant(settings,engine)
    cases=[]
    try:
        players=[join(app,token,i) for i in range(4)]
        for outcome in ('win','loss'):
            for path in ('/api/admin/simulator/ready','/api/admin/queue/call-next','/api/admin/simulator/start','/api/admin/simulator/'+outcome):
                assert post(admin,path).status_code==200
        with engine.begin() as c:
            for i in range(1,1+(len(DEVELOPMENT)-1)//8):
                execute(c,"INSERT INTO staff_users(id,username,password_hash,role) VALUES(:id,:name,:hash,'admin')",
                        id=i+1,name=f'language-development-{i}',hash=DUMMY_HASH)
        state=await service.prepare();began=time.monotonic()
        while state['reason']=='warming' and time.monotonic()-began<125:
            await asyncio.sleep(1);state=await service.status()
        if not state['available']: raise RuntimeError('Local model preparation failed.')
        for i,(label,question,language) in enumerate(DEVELOPMENT):
            topic,*subtype=label.split(':')
            row={'id':f'public-language-dev-{i+1:02d}','family':'development','language':language,
                 'question':question,'target':{'topic':topic}}
            if subtype: row['target'][topic]=subtype[0]
            if label=='social:help': row['acceptable_labels']=[label,'knowledge:assistant']
            service.last_target=None
            try:
                reply=await service.ask(Question(question=question,use_memory=False),1+i//8)
                result=score(row,reply,service.last_target)
            except Exception as error:
                result=score(row,{'status':'error','reason':type(error).__name__},None)
            cases.append(result)
            print(json.dumps({k:result[k] for k in ('id','expected_label','predicted_label','accepted','reason')}),flush=True)
        topics=sorted({c['expected_topic'] for c in cases})
        report={'kind':'visible-development-probes','measured_at':datetime.now(timezone.utc).isoformat(),
                'limits':'Developer-authored development checks. Not held-out, independently human-adjudicated or general factual accuracy.',
                'runtime':runtime_fingerprint(),'model':settings.ollama_model,
                'development_sha256':sha(ROOT/'backend/tests/test_assistant_public_language.py'),
                'metrics':summarize(cases,topics),'cases':cases}
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as stream: json.dump(report,stream,indent=2)
        print(json.dumps({'accepted':report['metrics']['accepted'],'n':len(cases)}),flush=True)
    finally:
        await service.close()
        for player in locals().get('players',[]): player.close()
        try: next(generator)
        except StopIteration: pass


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    asyncio.run(check(parser.parse_args().output.resolve()))
