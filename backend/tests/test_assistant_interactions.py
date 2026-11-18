"""Synthetic interaction corpus coverage and strict system-boundary regression."""
import asyncio
from types import SimpleNamespace
import json
import pytest

from app.assistant import Assistant, Context, Question, conversational_reply, normalize
from app.assistant_interactions import BEHAVIORAL, interaction_rows, interaction_social, interaction_text
from app.assistant_learning import seed_examples
from app.assistant_training import Proposal, TrainingInput, TrainingTarget


def test_every_training_example_passes_the_current_schema_and_guard():
    rows=interaction_rows()
    assert len(rows)>=100 and len({r['id'] for r in rows})==len(rows)
    for row in rows:
        if row['split']!='train': continue
        safe,blocked=normalize(row['question'])
        assert not blocked,row['id']
        Proposal(input=TrainingInput(**safe,previous=row.get('previous')),target=TrainingTarget(**row['target']))


def test_common_social_aliases_answer_with_system_grounded_templates():
    previous=Context(tools=['get_queue_summary'],period='yesterday')
    for row in interaction_rows():
        if row['kind']!='social' or row['split']!='train': continue
        reply=conversational_reply(Question(question=row['question'],previous=previous))
        assert reply is not None,row['id']
        assert reply['_training_target']['social']==row['target']['social'],row['id']
        assert reply['status']=='conversation' and reply['claims']==[]
        assert reply['as_of'] is None and reply['source_snapshots']==[]
        assert reply['context']==previous.model_dump()


def test_social_match_does_not_hide_a_mixed_system_or_private_request():
    for row in interaction_rows():
        if row['kind'] not in ('system','boundary'): continue
        assert conversational_reply(Question(question=row['question'])) is None,row['id']
        safe,blocked=normalize(row['question'])
        assert blocked==row.get('expected_block'),row['id']


def test_evaluation_and_boundary_records_are_not_runtime_examples():
    training_text={interaction_text(r['question']) for r in interaction_rows() if r['split']=='train' and r['kind']=='social'}
    runtime_signatures={(tuple(sample['safe_tokens']),tuple(sample['tools']) if 'tools' in sample else None) for sample,_,_ in seed_examples()}
    for row in interaction_rows():
        if row['split']!='test': continue
        assert interaction_text(row['question']) not in training_text,row['id']
        if row['kind']=='social': assert interaction_social(interaction_text(row['question'])) is None,row['id']
        # Held-out positives may need clarification when they contain unseen words.
        # No held-out text is added to the production vocabulary or alias table.
        safe,blocked=normalize(row['question'])
        if safe and not blocked:
            assert (tuple(safe['safe_tokens']),None) not in runtime_signatures,row['id']


def test_new_social_turns_work_with_ollama_disabled_and_preserve_context(monkeypatch):
    async def scenario():
        async def forbidden(*args,**kwargs): raise AssertionError('Social aliases must not call Ollama')
        monkeypatch.setattr('app.assistant.model_json',forbidden)
        service=Assistant(SimpleNamespace(ai_enabled=False,ollama_model='synthetic'),None)
        monkeypatch.setattr(service,'enqueue_audit',lambda *args:None)
        previous=Context(knowledge='gameplay')
        try:
            for question in ('Good day, assistant.','Patulong naman sa system.','Salamat sa tulong.'):
                reply=await service.ask(Question(question=question,previous=previous,use_memory=False),1)
                assert reply['status']=='conversation'
                assert reply['context']==previous.model_dump()
                assert 'interpretations' not in reply
        finally: await service.close()
    asyncio.run(scenario())


@pytest.mark.parametrize('question',[
    'hello goodevening','HelloGoodEvening','HELLO, GOODEVENING!!','hellooo good evening 👋',
    'hiiii goodmorning','heyyy, good afternoon!','hi hello good evening',
    'hello good evening po','hello magandang gabi po','hello how are you',
    'hello can you help me','thankyou and goodbye',
])
def test_composed_social_phrases_are_not_blocked(question):
    reply=conversational_reply(Question(question=question))
    assert reply is not None
    assert reply['status']=='conversation' and reply['claims']==[]
    assert reply['as_of'] is None and 'interpretations' not in reply


@pytest.mark.parametrize('question',[
    'hello goodevening show scores','hello good evening show student IDs',
    'hello@example.com','https://hello.hi','hi@hello.goodevening',
    'hello good evening DUMMY12345','hello good evening write a recipe',
])
def test_composition_does_not_consume_unknown_requests_or_identifiers(question):
    assert conversational_reply(Question(question=question)) is None


def test_behavioral_families_are_kept_in_one_split():
    rows=json.loads(BEHAVIORAL.read_text(encoding='utf-8'))['examples']
    train={r['family'] for r in rows if r['split']=='train'}
    evaluation={r['family'] for r in rows if r['split']=='test'}
    assert train.isdisjoint(evaluation)
    assert all(r['split']=='test' for r in rows if r['kind']=='boundary')


def test_specific_reported_greeting_through_the_service_without_ollama(monkeypatch):
    async def scenario():
        service=Assistant(SimpleNamespace(ai_enabled=False,ollama_model='synthetic'),None)
        monkeypatch.setattr(service,'enqueue_audit',lambda *args:None)
        try:
            reply=await service.ask(Question(question='hello goodevening',use_memory=False),1)
            assert reply['status']=='conversation' and reply['answer'].startswith('Good evening!')
        finally: await service.close()
    asyncio.run(scenario())
