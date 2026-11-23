"""Retrieve owner-reviewed corrections and clarify only supported ambiguities."""
import json
from pathlib import Path

import pytest

from app.assistant import Assistant, Question, RoutingPlan, normalize
from app.assistant_learning import CORPUS, CONTRASTS, interpretation_choices, retrieve, seed_examples
from app.assistant_interactions import interaction_rows
from app.assistant_training import Proposal, TrainingInput, TrainingTarget
from app.database import execute
from test_player_flow import environment
from test_assistant_training import candidate, approve, BASE


def test_corpus_is_valid_and_evaluation_is_not_retrieved():
    rows=json.loads(CORPUS.read_text())['examples']
    assert len(rows)>=60
    for row in rows:
        normalized,blocked=normalize(row['question'])
        assert not blocked,row['id']
        Proposal(input=TrainingInput(**normalized),target=TrainingTarget(**row['target']))
    train={tuple(sample['safe_tokens']) for sample,_,_ in seed_examples()}
    contrast_rows=json.loads(CONTRASTS.read_text())['examples']
    assert len(seed_examples())==sum(row['split']=='train' for row in rows+contrast_rows+list(interaction_rows()))
    for row in rows:
        if row['split']=='test': assert tuple(normalize(row['question'])[0]['safe_tokens']) not in train


@pytest.mark.parametrize('question', ['hello','Explain accuracy.','Show overall overlap accuracy.',
    'How many players registered?','What is the cabinet connection status?','Show average score and win rate.'])
def test_clear_questions_do_not_get_two_options(question):
    normalized,blocked=normalize(question)
    assert not blocked
    assert interpretation_choices(normalized,RoutingPlan(topic='players'))==[]


def test_ambiguous_question_gets_exactly_two_safe_scoped_interpretations():
    normalized,_=normalize('Show accuracy today for physical device results.')
    choices=interpretation_choices(normalized,RoutingPlan(topic='players'))
    assert len(choices)==2 and choices[0]['question']!=choices[1]['question']
    for choice in choices:
        safe,blocked=normalize(choice['question'])
        assert not blocked
        assert safe['requested_period']=='today' and safe['requested_source']=='device'
    assert len(interpretation_choices(normalize('How are the players doing?')[0],RoutingPlan(topic='players')))==2


def test_learning_is_owner_scoped_approved_current_and_disableable(environment):
    app,admin,_,engine,settings=environment
    body=candidate('What is the overall win rate?','players')
    # candidate helper's social default only applies to social inputs.
    row=admin.post(BASE,json=body).json()
    safe,_=normalize('What is the overall win rate?')
    assert retrieve(engine,1,safe)['exact'] is None  # pending is not learned
    assert approve(admin,row).status_code==200
    learned=retrieve(engine,1,safe)
    assert learned['exact']['topic']=='players' and learned['reviewed_matches']==1
    assert retrieve(engine,2,safe)['exact'] is None
    assert retrieve(engine,1,safe,use_memory=False)['exact'] is None
    assert all(item['input']['prior_contexts']==[] for item in learned['examples'])
    with engine.begin() as c:
        execute(c,"UPDATE ai_training_examples SET context_version=:version",version='0'*64)
    assert retrieve(engine,1,safe)['exact'] is None


def test_ambiguous_query_does_not_query_live_data_until_choice(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    async def ready(self): return {'available':True}
    async def classify(*args,**kwargs): return {'message':{'content':'{"topic":"players"}'}}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',classify)
    monkeypatch.setattr('app.assistant.collect_all',lambda *args:pytest.fail('No analytics before clarification'))
    reply=admin.post('/api/admin/assistant/query',json={'question':'What is our accuracy?','use_memory':False}).json()
    assert reply['status']=='needs_clarification' and len(reply['interpretations'])==2
    assert reply['claims']==[] and reply['as_of'] is None


def test_exact_correction_routes_without_model_but_reads_fresh_data(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    body=candidate('Check event figures.','players')
    row=admin.post(BASE,json=body).json()
    assert approve(admin,row).status_code==200
    async def ready(self): return {'available':True}
    async def forbidden(*args,**kwargs): pytest.fail('Exact reviewed correction should route locally')
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',forbidden)
    reply=admin.post('/api/admin/assistant/query',json={'question':'Check event figures.'}).json()
    assert reply['status']=='ok' or reply['status']=='no_data'
    assert reply['learning']['method']=='reviewed_example'
    assert reply['as_of'] is not None and reply['learning']['model_weights_changed'] is False
    assert reply['evidence']['global_counts']['registrations']==0
