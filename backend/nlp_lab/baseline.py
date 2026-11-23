"""Actual v11 routing with synthetic no-data renderers; no database or identity access."""
import asyncio
from types import SimpleNamespace
from unittest.mock import patch

from app.assistant import Assistant, Question, basic_response
from app.assistant_training import TrainingInput,TrainingTarget


class Observer(Assistant):
    last_target=None
    async def _ask(self,*args,**kwargs):
        result=await super()._ask(*args,**kwargs)
        self.last_target=result.get('_training_target')
        return result
    def enqueue_audit(self,*args,**kwargs): pass


async def predict(rows,training,model='qwen3:4b-instruct'):
    from evaluate_routing import route_label
    examples=[]
    for row in training:
        if row['blocked']: continue
        sample=TrainingInput(**row['safe'],previous=row['previous']).model_dump()
        label=TrainingTarget(**row['target']).model_dump()
        examples.append((sample,label,'project'))
    service=Observer(SimpleNamespace(ai_enabled=True,ollama_url='http://127.0.0.1:11434',ollama_model=model,simulator_enabled=False),None)
    def no_data(*args,**kwargs): return None
    def render(data,context):
        result=basic_response(Question(question='Offline evaluation.'),'no_data','Offline routing only; no database was queried.')
        result['context']=context.model_dump()
        return result
    result=[]
    try:
        state=await service.prepare()
        started=asyncio.get_running_loop().time()
        while state['reason']=='warming' and asyncio.get_running_loop().time()-started<125:
            await asyncio.sleep(1);state=await service.status()
        if not state['available']: raise RuntimeError('Ollama is unavailable; do not substitute another baseline.')
        # Scoped process-local patches never change application files or running
        # servers. Only train partition examples may enter few-shot retrieval.
        with patch('app.assistant_learning.seed_examples',lambda:tuple(examples)),patch('app.assistant.collect',no_data),patch('app.assistant.collect_all',no_data),patch('app.assistant.compose',render),patch('app.assistant.compose_all',render):
            for i,row in enumerate(rows):
                service.last_target=None
                began=asyncio.get_running_loop().time()
                try:
                    reply=await service.ask(Question(question=row['question'],previous=row['previous'],use_memory=False),1+i//8)
                    actual='unsupported' if reply['status'] in ('refused','needs_clarification') else route_label(service.last_target) if service.last_target else 'error'
                    error=reply.get('reason') if reply['status']=='unavailable' else None
                except Exception as failure:
                    actual='error';error=type(failure).__name__
                result.append({'id':row['id'],'expected':row['label'],'predicted':actual,'error':error,
                               'seconds':asyncio.get_running_loop().time()-began})
                if (i+1)%25==0: print(f'Ollama component: {i+1}/{len(rows)}',flush=True)
    finally: await service.close()
    return result
