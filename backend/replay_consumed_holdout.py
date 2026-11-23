"""Regression replay ONLY. Never creates a new unseen-test claim or rewrites v1.

The original data, labels, scorer, consumption ledger and first result must remain
unchanged. Current predictor hashes are frozen before the first replay request.
"""
import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

import httpx

from app.assistant import Question
from app.assistant_language import LEXICON, lexical_resource  # LEXICON = the file the app loads (v2 since 24 Nov)
from app.database import execute
from app.security import DUMMY_HASH
from evaluate_holdout import ObservedAssistant, score
from holdout_audit import DATASET, MANIFEST, ROOT, TOPICS, evaluator_fingerprint, runtime_fingerprint, sha
from holdout_metrics import summarize


def protected_inputs():
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    ledger=DATASET.with_suffix('.consumed.json')
    consumed=json.loads(ledger.read_text(encoding='utf-8'))
    if consumed['status']!='complete' or sha(DATASET)!=manifest['dataset_sha256']:
        raise ValueError('Only an unchanged, already-consumed holdout can be replayed.')
    if evaluator_fingerprint()!=manifest['evaluation_code']:
        raise ValueError('The original frozen scorer/inventory was changed.')
    baseline=ROOT/'docs/nlp-evaluation/results/holdout-v1.json'
    if sha(baseline)!=consumed['result_sha256']:
        raise ValueError('The first-use result must remain unchanged.')
    protected={str(p.relative_to(ROOT)):sha(p) for p in (DATASET,MANIFEST,ledger,baseline)}
    return manifest,protected


async def replay(output):
    manifest,protected=protected_inputs()
    if output.exists() or output.with_suffix('.freeze.json').exists():
        raise ValueError('Choose a new regression artifact; existing runs are immutable.')
    frozen={'kind':'consumed-holdout-regression','runtime':runtime_fingerprint(),
            'public_lexicon_sha256':lexical_resource()[1],
            'scorer':evaluator_fingerprint(),'runner_sha256':sha(Path(__file__)),
            'protected_inputs':protected,'started_at':datetime.now(timezone.utc).isoformat()}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.with_suffix('.freeze.json').open('x',encoding='utf-8') as stream:
        json.dump(frozen,stream,indent=2)
    # Read prompts only inside this regression process; never print or import
    # them into runtime data, aliases, retrieval, vocabulary or Graphify inputs.
    rows=json.loads(DATASET.read_text(encoding='utf-8'))['examples']
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
                        id=index+1,name=f'synthetic-regression-{index}',hash=DUMMY_HASH)
        state=await assistant.prepare();began=time.monotonic()
        while state['reason']=='warming' and time.monotonic()-began<125:
            await asyncio.sleep(1);state=await assistant.status()
        if not state['available']: raise RuntimeError('Local model preparation failed; no replay predictions executed.')
        async with httpx.AsyncClient(base_url=settings.ollama_url,trust_env=False,timeout=5) as client:
            tags=(await client.get('/api/tags')).json()['models']
            model=next({'name':m['name'],'digest':m['digest']} for m in tags if m['name']==settings.ollama_model)
        for index,row in enumerate(rows):
            began=time.monotonic();assistant.last_target=None
            try:
                reply=await assistant.ask(Question(question=row['question'],previous=row.get('previous'),use_memory=False),1+index//8)
                result=score(row,reply,assistant.last_target)
            except Exception as error:
                result=score(row,{'status':'error','reason':type(error).__name__},None)
            result['seconds']=round(time.monotonic()-began,4)
            cases.append(result)
            output.with_suffix('.partial.json').write_text(json.dumps({'kind':frozen['kind'],'cases':cases},indent=2),encoding='utf-8')
            if (index+1)%25==0:
                print(json.dumps({'regression_evaluated':index+1,'total':len(rows),'accepted':sum(c['accepted'] for c in cases)}),flush=True)
        if protected_inputs()[1]!=protected or runtime_fingerprint()!=frozen['runtime'] or sha(Path(__file__))!=frozen['runner_sha256'] or sha(LEXICON)!=frozen['public_lexicon_sha256']:
            raise RuntimeError('Frozen predictor, scorer, runner or protected artifacts changed during replay.')
        report={'kind':frozen['kind'],'measured_at':datetime.now(timezone.utc).isoformat(),
                'dataset_sha256':manifest['dataset_sha256'],'model':model,
                'limits':'Consumed synthetic regression, not unseen accuracy or independently adjudicated factual answer accuracy. No changes allowed against this replay.',
                'metrics':summarize(cases,TOPICS),'cases':cases}
        with output.open('x',encoding='utf-8') as stream: json.dump(report,stream,indent=2)
        print(json.dumps({'kind':report['kind'],'metrics':report['metrics']},indent=2),flush=True)
    finally:
        await assistant.close()
        for player in locals().get('players',[]): player.close()
        try: next(generator)
        except StopIteration: pass


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    asyncio.run(replay(parser.parse_args().output.resolve()))
