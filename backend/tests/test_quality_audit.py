"""Adversarial regressions found by the cross-system quality audit (synthetic DB only)."""
import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from app.analytics import collect
from app.assistant import Assistant
from app.database import execute
from app.game import replay, simulated_result
from test_player_flow import environment, join, post, entry_payload


@pytest.mark.parametrize('question', ['Who won the basketball game?',
    'Show the football score.', 'How many cryptocurrency players registered?'])
def test_unknown_subject_cannot_be_replaced_with_event_data(environment,monkeypatch,question):
    app,admin,token,engine,settings=environment
    async def ready(*args,**kwargs): return {'available':True}
    async def scope_only(settings,payload,*args,**kwargs):
        assert set(payload['format']['properties'])=={'scope'},'A foreign subject must stop before intent routing'
        return {'message':{'content':'{"scope":"unsupported"}'}}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',scope_only)
    monkeypatch.setattr('app.assistant.collect_all',lambda *a,**k:pytest.fail('No data for an unknown subject'))
    response=admin.post('/api/admin/assistant/query',json={'question':question,'use_memory':False})
    assert response.status_code==200
    assert response.json()['reason'] in {'unrecognized_context','system_scope'}
    assert response.json()['status']=='needs_clarification' and response.json()['context']['tools']==[]


def test_non_ascii_csrf_is_rejected_without_a_server_error(environment):
    app,admin,token,engine,settings=environment
    response=admin.post('/api/admin/admissions',json={'open':False},headers={b'X-CSRF-Token':b'\xff'})
    assert response.status_code==403


def test_request_host_does_not_authorize_a_foreign_origin(environment):
    app,admin,token,engine,settings=environment
    response=admin.post('/api/admin/admissions',json={'open':False},headers={'Host':'evil.example','Origin':'http://evil.example'})
    assert response.status_code==403


def test_signed_in_player_cannot_replace_their_identity_and_abandon_a_ticket(environment):
    app,admin,token,engine,settings=environment
    player=join(app,token,1)
    original=player.get('/api/player/context').json()['ticket']['id']
    assert player.post('/api/player/entry',json=entry_payload(token)).status_code==200
    response=player.post('/api/player/register',json={'nickname':'Different Test','studentId':'DUMMY-TEST-NEW','acknowledged':True})
    assert response.status_code==409
    assert player.get('/api/player/context').json()['ticket']['id']==original
    assert len(admin.get('/api/admin/snapshot').json()['queue'])==1


def test_registration_session_rotation_revokes_the_previous_cookie(environment):
    app,admin,token,engine,settings=environment
    player=join(app,token,1)
    previous=TestClient(app,cookies=player.cookies)
    for route in ('/api/admin/simulator/ready','/api/admin/queue/call-next','/api/admin/simulator/start','/api/admin/simulator/win'):
        assert post(admin,route).status_code==200
    assert player.post('/api/player/entry',json=entry_payload(token)).status_code==200
    assert player.post('/api/player/register',json={'nickname':'Test 1','studentId':'DUMMY-TEST-1','acknowledged':True}).status_code==200
    assert previous.get('/api/player/context').json()['ticket'] is None
    assert player.get('/api/player/context').json()['ticket']['status']=='waiting'


@pytest.mark.parametrize('flag',['maintenance','enabled'])
def test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(environment,flag):
    app,admin,token,engine,settings=environment
    post(admin,'/api/admin/simulator/ready')
    with engine.begin() as c:
        execute(c,'UPDATE machines SET '+('maintenance=1' if flag=='maintenance' else 'enabled=0')+' WHERE id=1')
    assert admin.get('/api/admin/snapshot').json()['machineState']=='offline'
    assert collect(engine,tools=['get_machine_summary'])['machine']['state']=='offline'


@pytest.mark.parametrize('outcome',['win','loss'])
def test_terminal_duration_cannot_extend_beyond_the_ending_placement(outcome):
    result=simulated_result(outcome)
    with pytest.raises(ValueError):
        replay(result['placements'],result['durationMs']+1000,outcome)


def test_oversized_json_is_rejected_before_processing_the_action(environment):
    app,admin,token,engine,settings=environment
    response=admin.post('/api/admin/admissions',json={'open':False,'padding':'x'*70000})
    assert response.status_code==413
    assert admin.get('/api/admin/snapshot').json()['admissionsOpen'] is True


def test_chunked_body_limit_cannot_be_bypassed_without_content_length(environment):
    app,admin,token,engine,settings=environment
    def chunks():
        yield b'{"open":false,"padding":"'
        yield b'x'*70000
        yield b'"}'
    response=admin.post('/api/admin/admissions',content=chunks(),headers={'Content-Type':'application/json'})
    assert response.status_code==413
    assert admin.get('/api/admin/snapshot').json()['admissionsOpen'] is True


@pytest.mark.parametrize('payload',[
    {'username':'bad\ud800','password':'synthetic'},
    {'username':'admin','password':'bad\ud800'},
    {'username':'admin','password':'synthetic','unrecognized':'input'},
])
def test_malformed_login_text_or_unknown_fields_fail_without_server_errors(environment,payload):
    app,admin,token,engine,settings=environment
    import json
    response=admin.post('/api/admin/login',content=json.dumps(payload),headers={'Content-Type':'application/json'})
    assert response.status_code==422


def test_readiness_requires_applied_migrations_and_schema(environment):
    app,admin,token,engine,settings=environment
    assert admin.get('/api/health').status_code==200
    with engine.begin() as c:
        execute(c,"DELETE FROM schema_migrations WHERE version='004_assistant_training.sql'")
    assert admin.get('/api/health').status_code==503


def test_fresh_disabled_simulator_cannot_accept_a_new_assignment(environment):
    app,admin,token,engine,settings=environment
    post(admin,'/api/admin/simulator/ready')
    from app.main import create_app
    replacement=create_app(replace(settings,simulator_enabled=False))
    try:
        client=TestClient(replacement,cookies=admin.cookies,headers=admin.headers)
        assert client.get('/api/admin/snapshot').json()['machineState']=='offline'
        assert collect(engine,tools=['get_machine_summary'],simulator_enabled=False)['machine']['state']=='offline'
    finally: replacement.state.engine.dispose()
