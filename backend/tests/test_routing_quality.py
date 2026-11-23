"""Intent-family regression and evaluation contamination checks, not accuracy estimates."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.assistant import Assistant, RoutingPlan, constrained_route, intent_payload, normalize, resolve_routing
from app.assistant_semantics import constraints
from app.assistant_learning import CONTRASTS, CORPUS, retrieve, seed_examples
from app.assistant_training import Proposal, TrainingInput, TrainingTarget
from evaluate_routing import route_label
from test_player_flow import environment


@pytest.mark.parametrize('question,tools,knowledge',[
    ('Summarize all event activity.',['get_event_summary','get_queue_summary','get_machine_summary'],None),
    ('Explain who assigns the next player.',[],'queue_flow'),
    ('Can simulator activity verify the ESP32 connection?',[],'offline'),
    ('Do physical scores and simulator results stay separate?',[],'results'),
    ('When are most games played?',['get_play_trend'],None),
    ('Kailan ang pinakamaraming laro?',['get_play_trend'],None),
    ('Explain why the queue is stuck.',['get_queue_summary','get_machine_summary'],None),
])
def test_current_intent_family_overrides_an_incorrect_model_label(question,tools,knowledge):
    normalized,blocked = normalize(question)
    assert blocked is None and normalized['has_unrecognized_words'] is False
    for wrong in (RoutingPlan(topic='definition',definition='accuracy'),RoutingPlan(topic='knowledge',knowledge='registration')):
        actual = resolve_routing(wrong,normalized)
        assert actual.tools == tools and actual.knowledge == knowledge and actual.definition is None


def test_new_data_is_safe_consistent_and_never_retrieves_evaluation_rows():
    training = {tuple(sample['safe_tokens']) for sample,_,_ in seed_examples()}
    contrasts = json.loads(CONTRASTS.read_text())['examples']
    assert len({row['id'] for row in contrasts}) == len(contrasts)
    for row in contrasts:
        safe,blocked = normalize(row['question'])
        assert not blocked and not safe['has_unrecognized_words'],row['id']
        Proposal(input=TrainingInput(**safe),target=TrainingTarget(**row['target']))
    eval_rows = [row for row in json.loads(CORPUS.read_text())['examples'] if row['split']=='test']
    validation = json.loads(CORPUS.with_name('assistant-routing-validation.json').read_text())['examples']
    assert {row['family'] for row in validation}.isdisjoint(row['family'] for row in contrasts)
    for row in eval_rows+validation:
        safe,blocked = normalize(row['question'])
        assert not safe or tuple(safe['safe_tokens']) not in training,row['id']


def test_role_separated_demonstrations_leave_current_request_last():
    safe,_ = normalize('Show average points for the event.')
    examples = retrieve(None,1,safe,use_memory=False)['examples']
    assert examples
    payload = intent_payload(SimpleNamespace(ollama_model='synthetic-model'),safe,examples=examples)
    messages = payload['messages']
    assert messages[0]['role'] == 'system' and messages[-1]['role'] == 'user'
    assert json.loads(messages[-1]['content'])['safe_tokens'] == safe['safe_tokens']
    assert any(message['role']=='assistant' for message in messages)
    for index in range(1,len(messages)-1,2):
        assert messages[index]['role']=='user' and messages[index+1]['role']=='assistant'
        TrainingTarget.model_validate_json(messages[index+1]['content'])
    assert payload['options']['temperature'] == 0


def test_public_explanations_do_not_enable_assignments_identifiers_or_unknown_subjects():
    assert normalize('Please assign the next player.')[1] == 'refused'
    assert normalize('List student IDs.')[1] == 'refused'
    safe,blocked = normalize('Who won the basketball game?')
    assert blocked or safe['has_unrecognized_words'] or safe['requires_scope_check']
    assert route_label({'topic':'definition','definition':'average_score'}) == 'definition:average_score'


@pytest.mark.parametrize('question',[
    'How many players are waiting for the operator?',
    'Show separate simulator and physical scores.',
])
def test_measurement_requests_are_not_replaced_by_workflow_explanations(question):
    safe,blocked = normalize(question)
    assert not blocked and not safe['has_unrecognized_words']
    payload = intent_payload(SimpleNamespace(ollama_model='synthetic'),safe)
    assert json.loads(payload['messages'][-1]['content'])['request_kind'] == 'analytics'
    assert 'definition' not in payload['format']['properties']['topic']['enum']


@pytest.mark.parametrize('question',[
    'Explain remembered context.',
    'Summarize the event including activity.',
])
def test_reviewed_function_and_memory_words_survive_the_runtime_guard(question):
    safe,blocked = normalize(question)
    assert not blocked and not safe['has_unrecognized_words']


@pytest.mark.parametrize('question,topic',[
    ('Summarize the whole carnival activity.','overview'),
    ('Report the average score.','scores'),
])
def test_generated_learning_labels_match_the_requested_measure(question,topic):
    safe,_ = normalize(question)
    assert constrained_route(safe,constraints(safe)).topic == topic


def test_api_keeps_real_summary_and_design_explanations_despite_wrong_model(environment,monkeypatch):
    app,admin,token,engine,settings = environment
    async def ready(self):
        return {'available':True}
    async def wrong_model(*args,**kwargs):
        return {'message':{'content':'{"topic":"definition","definition":"accuracy"}'}}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',wrong_model)
    cases = [('Summarize the event including activity.',None),
             ('Who assigns the next player?','queue_flow'),
             ('Can simulated results verify a real cabinet connection?','offline'),
             ('Do physical scores and simulator results stay separate?','results')]
    for question,knowledge in cases:
        response = admin.post('/api/admin/assistant/query',json={'question':question,'use_memory':False})
        assert response.status_code == 200
        body = response.json()
        if knowledge:
            assert body['status'] == 'conversation' and body['context']['knowledge'] == knowledge
        else:
            assert set(body['context']['tools']) == {'get_event_summary','get_queue_summary','get_machine_summary'}
