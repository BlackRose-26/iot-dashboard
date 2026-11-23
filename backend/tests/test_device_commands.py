import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import httpx
import pytest
from fastapi.testclient import TestClient

from app.database import execute, one
from app.game import simulated_result
from app.main import create_app
from app.security import now
from app.security import digest
from device_emulator import CommandEmulator
from test_player_flow import environment, join, post


def reserve(environment):
    app, admin, token, engine, settings = environment
    player = join(app, token, 1)
    device = TestClient(app, headers={'X-Device-Token':settings.device_token})
    assert device.post('/api/device/heartbeat', json={'state':'ready','firmware':'synthetic-command-test'}).status_code == 200
    session = post(admin,'/api/admin/queue/call-next').json()['sessionId']
    command = device.get('/api/device/commands').json()['commands'][0]
    receipt = {'sessionId':session,'expectedRevision':command['expectedRevision'],'status':'accepted'}
    return device, player, session, command, receipt


def command_row(engine, public):
    with engine.connect() as c:
        return dict(one(c, 'SELECT * FROM device_commands WHERE public_id=:id', id=public))


def test_polling_is_authorized_repeatable_and_contains_no_player_identity(environment):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    assert TestClient(app).get('/api/device/commands').status_code == 401
    assert player.get('/api/device/commands').status_code == 401
    assert admin.get('/api/device/commands').status_code == 401
    first = device.get('/api/device/commands')
    revision = admin.get('/api/admin/snapshot').json()['revision']
    assert all(device.get('/api/device/commands').json() == first.json() for _ in range(3))
    assert command_row(engine,command['id'])['status'] == 'pending'
    assert admin.get('/api/admin/snapshot').json()['revision'] == revision
    for forbidden in ('DUMMY-', 'nickname', 'student', 'token', 'id_lookup', 'receipt_hash'):
        assert forbidden not in first.text
    assert set(command) == {'id','type','deliverySequence','sessionId','expectedRevision','expiresAt','rules','rulesHash'}
    assert type(command['deliverySequence']) is int and command['deliverySequence']>0


def test_start_requires_durable_receipt_and_duplicate_ack_start_result_are_safe(environment):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    path = f"/api/device/commands/{command['id']}/ack"
    assert device.post(f'/api/device/sessions/{session}/start').status_code == 409
    with ThreadPoolExecutor(2) as pool:
        replies = list(pool.map(lambda _:device.post(path,json=receipt),range(2)))
    assert all(r.status_code == 200 for r in replies)
    assert replies[0].json() == replies[1].json()
    stored = command_row(engine,command['id'])
    assert stored['receipt_hash'] and stored['acknowledged_at'] and stored['status']=='accepted'
    before = admin.get('/api/admin/snapshot').json()['revision']
    assert device.post(path,json=receipt).json() == replies[0].json()
    assert command_row(engine,command['id'])['acknowledged_at'] == stored['acknowledged_at']
    assert admin.get('/api/admin/snapshot').json()['revision'] == before
    assert device.post(path,json={**receipt,'status':'rejected','rejectionCode':'busy'}).status_code == 409
    assert device.post(f'/api/device/sessions/{session}/start').status_code == 200
    started = admin.get('/api/admin/snapshot').json()['revision']
    assert device.post(f'/api/device/sessions/{session}/start').status_code == 200
    assert device.post(path,json=receipt).json() == replies[0].json()
    assert admin.get('/api/admin/snapshot').json()['revision'] == started
    assert command_row(engine,command['id'])['status'] == 'applied'
    assert device.get('/api/device/commands').json()['commands'] == []
    with engine.begin() as c:
        execute(c,'UPDATE game_sessions SET started_at=:start WHERE public_id=:id',start=now()-timedelta(seconds=60),id=session)
    payload = simulated_result('loss')
    result = device.post(f'/api/device/sessions/{session}/result',json=payload)
    assert result.status_code == 200
    assert device.post(path,json=receipt).json() == replies[0].json()
    assert device.post(f'/api/device/sessions/{session}/result',json=payload).json() == result.json()
    assert len(player.get('/api/player/context').json()['notifications']) == 1


@pytest.mark.parametrize('alteration', [
    {'sessionId':str(uuid.uuid4())}, {'expectedRevision':2}, {'expectedRevision':True},
    {'status':'applied'}, {'rejectionCode':'busy'}, {'extra':'untrusted'},
])
def test_invalid_or_stale_receipts_cannot_change_the_command(environment, alteration):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    response = device.post(f"/api/device/commands/{command['id']}/ack",json={**receipt,**alteration})
    assert response.status_code in (409,422)
    assert command_row(engine,command['id'])['receipt_hash'] is None
    assert command_row(engine,command['id'])['status'] == 'pending'


def test_rejection_and_expiry_retain_the_assignment_until_reconciliation(environment):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    response = device.post(f"/api/device/commands/{command['id']}/ack",json={**receipt,'status':'rejected','rejectionCode':'storage_failed'})
    assert response.status_code == 200
    assert player.get('/api/player/context').json()['ticket']['status'] == 'review'
    assert device.get('/api/device/commands').json() == {'commands':[], 'reviewRequired':True,'activeSessionId':session}
    assert post(admin,'/api/admin/queue/call-next').status_code == 409
    assert device.post(f'/api/device/sessions/{session}/start').status_code == 409
    assert post(admin,'/api/admin/simulator/release').status_code == 409
    with engine.connect() as c:
        assert one(c,'SELECT active_machine_id FROM game_sessions WHERE public_id=:id',id=session)['active_machine_id'] == 1
        assert one(c,"SELECT status FROM queue_entries WHERE status='assigned'")['status'] == 'assigned'


@pytest.mark.parametrize('transition', ['ack', 'heartbeat'])
def test_expired_unknown_start_never_becomes_an_automatic_no_show(environment,transition):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    with engine.begin() as c:
        execute(c,'UPDATE game_sessions SET ready_deadline_at=:past WHERE public_id=:id',past=now()-timedelta(seconds=1),id=session)
        execute(c,'UPDATE device_commands SET expires_at=:past WHERE public_id=:id',past=now()-timedelta(seconds=1),id=command['id'])
    assert device.get('/api/device/commands').json()['reviewRequired'] is True
    if transition == 'ack':
        assert device.post(f"/api/device/commands/{command['id']}/ack",json=receipt).status_code == 409
    else:
        assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic'}).status_code == 200
    assert player.get('/api/player/context').json()['ticket']['status'] == 'review'
    assert command_row(engine,command['id'])['status'] == 'expired'
    assert post(admin,'/api/admin/queue/call-next').status_code == 409


def test_review_is_admin_csrf_revision_checked_and_audited(environment):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    path = f'/api/admin/sessions/{session}/review'
    body = {'reason':'Synthetic uncertain device state','expectedRevision':1}
    assert player.post(path,json=body).status_code == 401
    assert admin.post(path,json=body,headers={'X-CSRF-Token':'wrong'}).status_code == 403
    assert admin.post(path,json={**body,'expectedRevision':3}).status_code == 409
    assert admin.post(path,json=body).status_code == 200
    assert admin.post(path,json=body).status_code == 409
    assert admin.post(path,json={**body,'expectedRevision':2}).status_code == 200
    with engine.connect() as c:
        assert one(c,"SELECT COUNT(*) AS n FROM audit_logs WHERE action='device_review_requested'")['n'] == 1
        assert one(c,"SELECT entity_type FROM audit_logs WHERE action='device_review_requested'")['entity_type'] == 'session'
    snapshot = admin.get('/api/admin/snapshot').json()
    assert snapshot['currentPlayer']['status'] == 'review'
    assert snapshot['deviceCommands'][0]['status'] == 'expired'
    assert 'receipt_hash' not in json.dumps(snapshot) and settings.device_token not in json.dumps(snapshot)


def test_receipt_survives_application_recreation_and_emulator_lost_ack(environment,tmp_path):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    class LostAck:
        def get(self,path): return device.get(path)
        def post(self,path,**kwargs):
            assert command['id'] in json.loads(journal.read_text())['commands']
            response = device.post(path,**kwargs)
            assert response.status_code == 200
            raise httpx.ReadTimeout('synthetic lost acknowledgement')
    journal = tmp_path/'command-journal.json'
    with pytest.raises(httpx.ReadTimeout):
        CommandEmulator(LostAck(),journal).poll_once()
    assert command['id'] in json.loads(journal.read_text())['commands']
    # A fresh API and emulator instance have no in-memory receipt state to reuse.
    replacement = create_app(settings)
    with TestClient(replacement,headers={'X-Device-Token':settings.device_token}) as restarted:
        assert CommandEmulator(restarted,journal).poll_once() == {'accepted':1,'reviewRequired':False}
        assert restarted.post(f'/api/device/sessions/{session}/start').status_code == 200
    replacement.state.engine.dispose()
    assert command_row(engine,command['id'])['status'] == 'applied'
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM game_sessions')['n'] == 1


def test_emulator_refuses_corrupt_journal_before_contacting_device(tmp_path):
    journal = tmp_path/'broken.json'
    journal.write_text('{broken')
    class NoRequests:
        def get(self,*args): pytest.fail('A corrupt journal must not contact the API')
    with pytest.raises(ValueError): CommandEmulator(NoRequests(),journal)
    public, session = str(uuid.uuid4()), str(uuid.uuid4())
    journal.write_text(json.dumps({'version':1,'commands':{public:{
        'receipt':{'sessionId':session,'expectedRevision':1,'status':'accepted'},
        'payloadHash':'0'*64,'command':{'id':public,'sessionId':session,'expectedRevision':1}}}}))
    with pytest.raises(ValueError): CommandEmulator(NoRequests(),journal)


def test_simulator_commands_are_not_delivered_to_the_device(environment):
    app, admin, token, engine, settings = environment
    join(app,token,1)
    post(admin,'/api/admin/simulator/ready')
    session = post(admin,'/api/admin/queue/call-next').json()['sessionId']
    device = TestClient(app,headers={'X-Device-Token':settings.device_token})
    assert device.get('/api/device/commands').json()['commands'] == []
    assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic'}).status_code == 409
    command = admin.get('/api/admin/snapshot').json()['deviceCommands'][0]
    receipt = {'sessionId':session,'expectedRevision':1,'status':'accepted'}
    assert device.post(f"/api/device/commands/{command['id']}/ack",json=receipt).status_code == 409


def test_other_machine_commands_and_maintenance_cannot_be_bypassed(environment):
    app, admin, token, engine, settings = environment
    device, player, session, command, receipt = reserve(environment)
    foreign = str(uuid.uuid4())
    with engine.begin() as c:
        machine_id = execute(c,"INSERT INTO machines(public_id,event_id,code,name,device_token_hash) VALUES(:id,1,'other-test','Other synthetic cabinet',:hash)",id=str(uuid.uuid4()),hash=digest('other-synthetic-device')).lastrowid
        execute(c,"INSERT INTO device_commands(public_id,machine_id,command_type,expected_revision,payload,expires_at) VALUES(:id,:machine,'reserve',1,'{}',:expiry)",id=foreign,machine=machine_id,expiry=now()+timedelta(minutes=1))
        execute(c,'UPDATE machines SET maintenance=1 WHERE id=1')
    assert device.post(f'/api/device/commands/{foreign}/ack',json=receipt).status_code == 404
    assert device.get('/api/device/commands').json()['commands'] == []
    assert device.post(f"/api/device/commands/{command['id']}/ack",json=receipt).status_code == 409
    assert post(admin,'/api/admin/queue/call-next').status_code == 409
    with engine.begin() as c:
        execute(c,'UPDATE machines SET maintenance=0,enabled=0 WHERE id=1')
    assert device.get('/api/device/commands').json()['commands'] == []
    assert device.post(f"/api/device/commands/{command['id']}/ack",json=receipt).status_code == 409
    assert post(admin,'/api/admin/queue/call-next').status_code == 409
