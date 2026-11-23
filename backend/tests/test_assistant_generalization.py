"""Independent behavioral probes: subject changes, invariance, requested operations and real SQL."""
import json
import uuid
from datetime import timedelta

import pytest

from app.analytics import collect, collect_all
from app.assistant import Assistant, Context, RoutingPlan, compose_all, normalize, requested_metrics, resolve_routing
from app.assistant_semantics import constraints, resolve_subject
from app.database import execute
from app.game import simulated_result, replay, canonical
from app.security import now, digest
from test_player_flow import environment

SCORE_PARAPHRASES=['score','scores','ilan ang score nila?','ilan ang score ng lahat ng participants?',
    'Show each participant’s points.','List the game scores for every player.', 'Ano ang puntos ng bawat player?',
    'Please show all participants and their scores.']

@pytest.mark.parametrize('question',SCORE_PARAPHRASES)
@pytest.mark.parametrize('old',[Context(tools=['get_queue_summary']),Context(definition='accuracy'),
    Context(tools=['get_event_summary'],metrics=['registrations']),Context(knowledge='registration')])
def test_explicit_subject_is_invariant_to_old_history_and_wrong_model_label(question,old):
    normalized,blocked=normalize(question)
    assert not blocked
    for route in (RoutingPlan(topic='follow_up'),RoutingPlan(topic='players'),RoutingPlan(topic='definition',definition='accuracy')):
        intent=resolve_routing(route,normalized,old)
        assert intent.tools==['get_player_scores'] and intent.definition is None and intent.knowledge is None
    assert 'registrations' not in requested_metrics(normalized)

@pytest.mark.parametrize('question,tools,metrics',[
    ('Show average score and score distribution.',['get_event_summary','get_score_distribution'],['average_score']),
    ('What is the total score?',['get_event_summary'],['total_score']),
    ('Calculate the total score.',['get_event_summary'],['total_score']),
    ('What is the average score?',['get_event_summary'],['average_score']),
    ('What is the highest score?',['get_event_summary'],['highest_score']),
    ('Who has the highest score?',['get_top_scores'],['highest_score']),
    ('Show scores and the queue.',['get_player_scores','get_queue_summary'],[]),
    ('What is the win rate?',['get_event_summary'],['wins','win_rate']),
    ('How many players registered?',['get_event_summary'],['registrations']),
    ('What is the cabinet connection status?',['get_machine_summary'],[]),
])
def test_directional_changes_select_the_requested_operation(question,tools,metrics):
    normalized,blocked=normalize(question)
    assert not blocked
    assert constraints(normalized)['tools']==tools
    assert requested_metrics(normalized)==metrics


def test_definition_and_ellipsis_are_distinct_from_a_new_data_subject():
    definition=resolve_routing(RoutingPlan(topic='scores'),normalize('What does score mean?')[0])
    assert definition.definition=='scoring' and definition.tools==[]
    previous=Context(tools=['get_player_scores'],score_page=1)
    intent=resolve_routing(RoutingPlan(topic='follow_up'),normalize('What about yesterday?')[0],previous)
    assert intent.tools==previous.tools
    for question,definition in [('Define average score.','average_score'),('Define total score.','total_score'),('Ano ang ibig sabihin ng score?','scoring')]:
        normalized,blocked=normalize(question)
        assert not blocked
        assert resolve_routing(RoutingPlan(topic='players'),normalized).definition==definition
    normalized,_=normalize('What about their average?')
    resolved,inherited=resolve_subject(normalized,previous)
    assert inherited and requested_metrics(resolved)==['average_score']
    assert constraints(resolved)['tools']==['get_event_summary']
    assert not resolve_subject(normalized,Context(tools=['get_queue_summary']))[1]
    missing,_=normalize('What about quasar system?')
    assert resolve_routing(RoutingPlan(topic='follow_up'),missing,previous).clarify


def seed_scores(engine,count=4):
    payloads=[simulated_result('win'),simulated_result('loss')]
    expected={}
    with engine.begin() as c:
        execute(c,'UPDATE events SET created_at=:at,starts_at=:at WHERE id=1',at=now()-timedelta(days=1))
        for i in range(count):
            code=f'EXAMPLE-{i:03d}'
            pid=execute(c,"INSERT INTO players(public_id,public_code,nickname,notice_version,notice_ack_at) VALUES(:uuid,:code,'Synthetic','test',:now)",uuid=str(uuid.uuid4()),code=code,now=now()).lastrowid
            qid=execute(c,"INSERT INTO queue_entries(public_id,event_id,player_id,status,closed_at) VALUES(:uuid,1,:pid,'served',:now)",uuid=str(uuid.uuid4()),pid=pid,now=now()).lastrowid
            payload=dict(payloads[i%2],terminalId=str(uuid.uuid4()))
            result=replay(payload['placements'],payload['durationMs'],payload['outcome'])
            expected[code]=result['score']
            execute(c,"""INSERT INTO game_sessions(public_id,event_id,machine_id,queue_entry_id,player_id,ruleset_id,
                status,ready_deadline_at,started_at,completed_at,received_at,terminal_id,result_hash,outcome,end_reason,
                duration_ms,score,highest_level,perfect_rows,overlap_total,attempted_width_total,result_source)
                VALUES(:uuid,1,1,:qid,:pid,1,'completed',:at,:started,:at,:at,:terminal,:hash,:outcome,:reason,:duration,
                :score,:level,:perfect,:overlap,:attempted,'simulator')""",uuid=str(uuid.uuid4()),qid=qid,pid=pid,
                at=now()-timedelta(seconds=1),started=now()-timedelta(seconds=60),terminal=payload['terminalId'],hash=digest(canonical(payload)),
                outcome=payload['outcome'],reason=result['reason'],duration=payload['durationMs'],score=result['score'],level=result['level'],
                perfect=result['perfect'],overlap=result['retained'],attempted=result['attempted'])
    return expected


def test_player_score_sql_is_paginated_and_keeps_source_evidence(environment):
    app,admin,token,engine,settings=environment
    expected=seed_scores(engine,55)
    first=collect_all(engine,tools=['get_player_scores'])
    second=collect_all(engine,tools=['get_player_scores'],score_page=2)
    a=first['cohorts']['simulator']['player_scores'];b=second['cohorts']['simulator']['player_scores']
    assert len(a['rows'])==50 and len(b['rows'])==5
    assert a['has_more'] and not b['has_more'] and a['total_players']==55
    assert {r['public_code']:r['score'] for r in a['rows']+b['rows']}==expected
    assert first['cohorts']['device']['player_scores']['rows']==[]
    answer=compose_all(first,Context(tools=['get_player_scores']))
    assert 'next page' in answer['answer'] and 'EXAMPLE-000' in answer['answer']
    assert 'players joined' not in answer['answer'] and 'players waiting' not in answer['answer']
    assert 'Cabinet / Wokwi: No matching recorded results' in answer['answer']


def test_api_answers_scores_not_a_wrong_model_or_saved_subject(environment,monkeypatch):
    app,admin,token,engine,settings=environment
    expected=seed_scores(engine)
    async def ready(self): return {'available':True}
    async def bad_route(*args,**kwargs): return {'message':{'content':'{"topic":"definition","definition":"accuracy"}'}}
    monkeypatch.setattr(Assistant,'status',ready);monkeypatch.setattr('app.assistant.model_json',bad_route)
    old=Context(tools=['get_queue_summary'],metrics=['registrations'],definition='accuracy').model_dump()
    for question in SCORE_PARAPHRASES[:4]:
        r=admin.post('/api/admin/assistant/query',json={'question':question,'previous':old,'use_memory':False})
        assert r.status_code==200
        response=r.json()
        assert response['context']['tools']==['get_player_scores'] and response['context']['definition'] is None
        for code,score in expected.items(): assert f'{code}: {score:,}' in response['answer']
        assert 'waiting' not in response['answer'] and 'players joined' not in response['answer'] and 'Overlap accuracy is' not in response['answer']
    next_reply=admin.post('/api/admin/assistant/query',json={'question':'next page','previous':response['context'],'use_memory':False}).json()
    assert next_reply['context']['score_page']==2
    assert next_reply['context']['tools']==['get_player_scores']
    assert 'No scores on page 2' in next_reply['answer']
