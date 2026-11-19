"""All-source chat checks against disposable synthetic MariaDB data."""
import json
from datetime import timedelta

from fastapi.testclient import TestClient

from app.analytics import collect_all
from app.assistant import Assistant, Context, Question, RoutingPlan, automatic_scope, compose_all, normalize
from app.database import execute
from app.game import simulated_result
from app.security import now
from test_player_flow import environment, join, post, entry_payload, accept_command


def test_default_scope_and_natural_followups():
    previous=Context(period='yesterday',source='simulator')
    body=Question(question='Show scores',previous=previous)
    assert body.source=='all' and Context().source=='all'
    assert automatic_scope(body,normalize(body.question)[0],RoutingPlan(topic='scores'))==('event_to_date','all')
    assert automatic_scope(body,normalize('What about today?')[0],RoutingPlan(topic='follow_up'))==('today','simulator')
    assert automatic_scope(body,normalize('Show both sources')[0],RoutingPlan(topic='follow_up'))==('yesterday','all')
    assert automatic_scope(body,normalize('Show physical device scores today')[0],RoutingPlan(topic='scores'))==('today','device')


def test_all_sources_are_separate_and_players_are_deduplicated(environment,monkeypatch):
    app,admin,token,engine,settings=environment
    player=join(app,token,1)
    for route in ('/api/admin/simulator/ready','/api/admin/queue/call-next','/api/admin/simulator/start','/api/admin/simulator/win'):
        assert post(admin,route).status_code==200
    assert player.post('/api/player/entry',json=entry_payload(token)).status_code==200
    player.headers['X-CSRF-Token']=player.get('/api/player/context').json()['csrf']
    assert player.post('/api/player/register',json={'nickname':'Test 1','studentId':'DUMMY-TEST-1','acknowledged':True}).status_code==200
    device=TestClient(app,headers={'X-Device-Token':settings.device_token})
    assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic','rssi':-55}).status_code==200
    session=post(admin,'/api/admin/queue/call-next').json()['sessionId']
    accept_command(device)
    assert device.post(f'/api/device/sessions/{session}/start').status_code==200
    with engine.begin() as c:
        execute(c,'UPDATE game_sessions SET started_at=:start WHERE public_id=:id',start=now()-timedelta(seconds=60),id=session)
    assert device.post(f'/api/device/sessions/{session}/result',json=simulated_result('loss')).status_code==200
    data=collect_all(engine,tools=['get_event_summary','get_top_scores','get_queue_summary','get_machine_summary'])
    assert data['global_counts']=={'completed_games':2,'completed_players':1,'registrations':1}
    assert {c['as_of'] for c in data['cohorts'].values()}=={data['as_of']}
    assert all(c['scope']['start']==data['scope']['start'] and c['scope']['end']==data['scope']['end'] for c in data['cohorts'].values())
    assert data['cohorts']['simulator']['summary']['win_rate']==100
    assert data['cohorts']['device']['summary']['win_rate']==0
    assert len(data['cohorts']['simulator']['top'])==len(data['cohorts']['device']['top'])==1
    assert 'machine' not in data['cohorts']['simulator']
    result=compose_all(data,Context(tools=data['tools'],detailed=True))
    assert '1 distinct players completed 2 valid rounds' in result['answer']
    assert result['answer'].count('players joined the event')==1
    assert 'Simulator: Rank 1:' in result['answer'] and 'Physical device: Rank 1:' in result['answer']
    assert '100%' in result['answer'] and '0%' in result['answer'] and '50%' not in result['answer']
    assert len(set(result['source_snapshots']))==3
    assert all('registrations' not in c['evidence']['summary'] for c in result['cohorts'])
    assert result['metric_scopes']['simulator.summary']['source']=='simulator'
    assert result['metric_scopes']['device.summary']['source']=='device'
    assert 'DUMMY' not in json.dumps(result) and 'id_lookup' not in json.dumps(result)
    registrations=compose_all(collect_all(engine,tools=['get_event_summary']),Context(tools=['get_event_summary'],metrics=['registrations']))
    assert registrations['answer']=='1 players joined the event in this period, across all sources.'
    assert registrations['cohorts']==[]
    # Exercise the actual query path, with local routing stubbed, not SQL/data.
    async def ready(self): return {'available':True}
    async def route(*args,**kwargs): return {'message':{'content':'{"topic":"scores"}'}}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',route)
    response=admin.post('/api/admin/assistant/query',json={'question':'What is the win rate?','use_memory':False})
    assert response.status_code==200
    assert response.json()['context']['source']=='all'
    assert len(response.json()['cohorts'])==2


def test_absent_device_results_are_not_inferred_from_registrations(environment):
    app,admin,token,engine,settings=environment
    join(app,token,1)
    for route in ('/api/admin/simulator/ready','/api/admin/queue/call-next','/api/admin/simulator/start','/api/admin/simulator/win'):
        assert post(admin,route).status_code==200
    data=collect_all(engine,tools=['get_event_summary','get_machine_summary'])
    result=compose_all(data,Context(tools=data['tools']))
    assert result['status']=='ok'
    physical=result['cohorts'][1]
    assert physical['status']=='no_data'
    assert physical['evidence']['summary']['win_rate'] is None
    assert 'Physical device: No matching recorded results' in physical['answer']
    assert 'does not confirm a physical ESP32 connection' in result['answer']
