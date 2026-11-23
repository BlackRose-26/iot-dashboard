"""Measure the local router without a database, private memory or report overwrites.

The existing test set is a reused development regression set, not an unseen test.
Dataset labels are fixed before inference; errors remain in the denominator.
"""
import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

from app.assistant import Assistant, Context, NORMALIZATION_VERSION, PROMPT, RoutingPlan, intent_payload, model_json, normalize, resolve_routing
from app.assistant_learning import corpus_digest, retrieve, seed_examples
from app.config import Settings

ROOT = Path(__file__).resolve().parents[1]


def route_label(route):
    topic = route['topic']
    field = {'knowledge':'knowledge','definition':'definition','social':'social'}.get(topic)
    return topic+(':'+str(route.get(field)) if field else '')


def intent_label(intent):
    return {'tools':sorted(intent.tools),'definition':intent.definition,'knowledge':intent.knowledge,
            'clarify':intent.clarify}


async def evaluate(dataset, split, output):
    if output.exists():
        raise ValueError('Choose a new output path; evaluation artifacts are immutable.')
    payload = json.loads(dataset.read_text(encoding='utf-8'))
    rows = [row for row in payload['examples'] if row['split'] == split]
    if not rows or len({row['id'] for row in rows}) != len(rows):
        raise ValueError('Evaluation requires nonempty unique case IDs.')
    training = {tuple(sample['safe_tokens']) for sample,_,_ in seed_examples()}
    for row in rows:
        safe,blocked = normalize(row['question'])
        if safe and tuple(safe['safe_tokens']) in training:
            raise ValueError('An exact normalized evaluation input occurs in runtime training examples: '+row['id'])
    settings = Settings.load()
    service = Assistant(settings,None)
    cases = []
    try:
        state = await service.prepare()
        started = time.monotonic()
        while state['reason'] == 'warming' and time.monotonic()-started < 125:
            await asyncio.sleep(1)
            state = await service.status()
        if not state['available']:
            raise RuntimeError('Local Ollama is unavailable: '+state['reason'])
        for row in rows:
            began = time.monotonic()
            safe,blocked = normalize(row['question'])
            if not blocked and safe['has_unrecognized_words']:
                blocked = 'unrecognized_context'
            expected = row.get('expected_block') or route_label(row['target'])
            actual = 'blocked:'+blocked if blocked else 'evaluation_error'
            if row.get('expected_block'):
                expected = 'blocked:'+row['expected_block']
            error = None
            diagnostics = {}
            try:
                if not blocked:
                    previous = Context.model_validate(row['previous']) if row.get('previous') else None
                    examples = retrieve(None,1,safe,previous.model_dump() if previous else None,use_memory=False)['examples']
                    async with asyncio.timeout(22):
                        response = await model_json(settings,intent_payload(settings,safe,
                            previous.model_dump() if previous else None,examples=examples))
                    route = RoutingPlan.model_validate_json(response['message']['content'])
                    actual = route_label(route.model_dump())
                    diagnostics = {key:response.get(key) for key in ('prompt_eval_count','eval_count','done_reason')}
                    diagnostics['retrieved_examples'] = len(examples)
                    diagnostics['resolved_intent'] = intent_label(resolve_routing(route,safe,previous))
            except Exception as failure:
                error = type(failure).__name__
            result = {'id':row['id'],'family':row.get('family'),'expected':expected,'predicted':actual,
                      'correct':expected==actual,'error':error,'seconds':round(time.monotonic()-began,4),**diagnostics}
            if row.get('expected_intent'):
                result['intent_correct'] = diagnostics.get('resolved_intent') == row['expected_intent']
            cases.append(result)
            print(json.dumps(result,ensure_ascii=False),flush=True)
    finally:
        await service.close()
    counts = Counter(row['expected'] for row in cases)
    correct = sum(row['correct'] for row in cases)
    report = {'measured_at':datetime.now(timezone.utc).isoformat(),'component':'application-guard-aware constraint-guided Ollama routing stage before final backend intent resolution',
        'model':settings.ollama_model,'dataset':dataset.relative_to(ROOT).as_posix(),
        'normalization_version':NORMALIZATION_VERSION,'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),
        'dataset_sha256':hashlib.sha256(dataset.read_bytes()).hexdigest(),'runtime_corpus_sha256':corpus_digest(),
        'split':split,'private_memory':False,'database_access':False,
        'n':len(cases),'correct':correct,'accuracy':correct/len(cases),
        'per_label':{label:{'n':count,'correct':sum(r['correct'] for r in cases if r['expected']==label)} for label,count in counts.items()},
        'confusion':[{'expected':a,'predicted':b,'count':count} for (a,b),count in Counter((r['expected'],r['predicted']) for r in cases).items()],
        'limits':payload.get('evaluation_note','Synthetic development regression, not blind real-user or end-to-end factual accuracy.'),
        'cases':cases}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as target:
        json.dump(report,target,indent=2,ensure_ascii=False)
    print(json.dumps({'output':str(output),'correct':correct,'n':len(cases),'accuracy':report['accuracy']}),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path,default=ROOT/'backend/data/assistant-routing.json')
    parser.add_argument('--split',default='test')
    parser.add_argument('--output',required=True,type=Path)
    args = parser.parse_args()
    asyncio.run(evaluate(args.dataset.resolve(),args.split,args.output.resolve()))
