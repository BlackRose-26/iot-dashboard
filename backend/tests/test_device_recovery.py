import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
from datetime import timedelta
import uuid
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
import pytest

from app.database import execute, one
from app.game import simulated_result
from app.security import now
from test_player_flow import environment, join, post
from recovery_emulator import RecoveryEmulator


def uid():
    return str(uuid.uuid4())


def setup(environment):
    app, admin, token, engine, settings = environment
    device = TestClient(app, headers={'X-Device-Token':settings.device_token})
    registration = {'bootId':uid(),'previousBootId':None,'storageId':uid(),'uptimeMs':0}
    assert device.post('/api/device/boot',json=registration).status_code == 200
    device.headers['X-Device-Boot-Id'] = registration['bootId']
    player = join(app,token,1)
    assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic-recovery-test'}).status_code == 200
    session = post(admin,'/api/admin/queue/call-next').json()['sessionId']
    command = device.get('/api/device/commands').json()['commands'][0]
    event = {'eventId':uid(),'sequence':1,'uptimeMs':100,'sessionId':session,
             'commandId':command['id'],'expectedRevision':1,'phase':'reserved'}
    assert device.post('/api/device/journal',json=event).status_code == 200
    return device,player,registration,session,command,event


def view(admin):
    return admin.get('/api/admin/snapshot').json()['deviceRecovery']


def fence(admin, session):
    return post(admin,f'/api/admin/sessions/{session}/fence',{
        'expectedRevision':view(admin)['revision'],'reason':'Synthetic operator investigation'})


def fence_receipt(device,session,sequence=2,phase='fenced_unstarted'):
    command = device.get('/api/device/commands').json()['commands'][0]
    return {'eventId':uid(),'sequence':sequence,'uptimeMs':10000,'sessionId':session,
            'commandId':command['id'],'expectedRevision':command['expectedRevision'],'phase':phase}


def resolution(admin,session,action,key=None):
    proof = view(admin)
    body = {'expectedRevision':proof['revision'],'evidenceId':proof['evidenceId'],
            'action':action,'reason':'Synthetic reviewed recovery'}
    return post(admin,f'/api/admin/sessions/{session}/resolve',body,key=key),body


def test_boot_lineage_retries_retirement_and_legacy_bypass(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    assert device.post('/api/device/boot',json=registration).status_code == 200
    assert device.post(f'/api/device/sessions/{session}/start').status_code == 409
    assert device.post(f"/api/device/commands/{command['id']}/ack",json={
        'sessionId':session,'expectedRevision':1,'status':'accepted'}).status_code == 409
    second = {**registration,'bootId':uid(),'previousBootId':registration['bootId']}
    assert device.post('/api/device/boot',json=second).status_code == 200
    assert device.post('/api/device/journal',json=event).status_code == 409
    assert device.post('/api/device/boot',json=registration).status_code == 409
    assert device.post('/api/device/boot',json={**second,'bootId':uid()}).status_code == 409
    device.headers['X-Device-Boot-Id'] = second['bootId']
    assert player.get('/api/player/context').json()['ticket']['status'] == 'review'
    assert view(admin)['allowedActions'] == []


def test_unstarted_fence_resolves_once_and_requires_fresh_readiness(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    assert fence(admin,session).status_code == 200
    assert view(admin)['allowedActions'] == []
    proof = fence_receipt(device,session)
    ack = device.post('/api/device/journal',json=proof)
    assert ack.status_code == 200
    assert device.post('/api/device/journal',json=proof).json() == ack.json()
    assert view(admin)['allowedActions'] == ['release_unstarted']
    key = uid()
    response,body = resolution(admin,session,'release_unstarted',key)
    assert response.status_code == 200
    assert post(admin,f'/api/admin/sessions/{session}/resolve',body,key=key).json() == response.json()
    assert post(admin,f'/api/admin/sessions/{session}/resolve',{**body,'reason':'Different'},key=key).status_code == 409
    context = player.get('/api/player/context').json()
    assert context['ticket']['status'] == 'expired'
    assert context['notifications'] == []
    assert admin.get('/api/admin/snapshot').json()['machineState'] == 'offline'
    with engine.connect() as c:
        assert one(c,"SELECT COUNT(*) AS n FROM audit_logs WHERE action='device_resolve'")['n'] == 1
        assert one(c,'SELECT score FROM game_sessions WHERE public_id=:id',id=session)['score'] is None
    assert post(admin,'/api/admin/queue/call-next').status_code == 409
    late = {**event,'eventId':uid(),'sequence':3,'uptimeMs':11000,'phase':'started',
            'roundBootId':registration['bootId'],'startUptimeMs':1000}
    assert device.post('/api/device/journal',json=late).status_code == 409


def test_conflicting_replay_is_durable_quarantine_not_rollback(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    assert device.post('/api/device/journal',json={**event,'uptimeMs':101}).status_code == 409
    assert view(admin)['quarantined'] is True
    assert view(admin)['allowedActions'] == []
    assert fence(admin,session).status_code == 409
    assert player.get('/api/player/context').json()['ticket']['status'] == 'review'
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM device_recovery_conflicts')['n'] == 1
        assert one(c,'SELECT COUNT(*) AS n FROM device_journal_events')['n'] == 1


@pytest.mark.parametrize('changes',[{'sequence':3},{'uptimeMs':99},{'sequence':True},{'expectedRevision':2},
                                  {'sessionId':uid()},{'unexpected':'field'}])
def test_invalid_or_out_of_order_evidence_does_not_release(environment,changes):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    packet = {**event,'eventId':uid(),'sequence':2,'uptimeMs':200,**changes}
    assert device.post('/api/device/journal',json=packet).status_code in (409,422)
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM device_journal_events')['n'] == 1
    assert view(admin)['allowedActions'] == []


def start_event(device,registration,event):
    packet = {**event,'eventId':uid(),'sequence':2,'uptimeMs':1000,'phase':'started',
              'roundBootId':registration['bootId'],'startUptimeMs':1000}
    return device.post('/api/device/journal',json=packet),packet


def test_started_round_cannot_claim_never_started_and_void_awards_no_score(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    # Reserve acknowledgement reached the server a second ago (synthetic clock setup).
    with engine.begin() as c:
        execute(c,'UPDATE device_commands SET acknowledged_at=:t WHERE public_id=:id',t=now()-timedelta(seconds=1),id=command['id'])
    assert start_event(device,registration,event)[0].status_code == 200
    assert fence(admin,session).status_code == 200
    proof = fence_receipt(device,session,3)
    assert device.post('/api/device/journal',json=proof).status_code == 409
    proof['phase'] = 'fenced_interrupted'
    assert device.post('/api/device/journal',json=proof).status_code == 200
    response,body = resolution(admin,session,'void_interrupted')
    assert response.status_code == 200
    assert player.get('/api/player/context').json()['ticket']['status'] == 'expired'
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM player_notifications')['n'] == 0


def test_reboot_terminal_pending_is_recovered_without_duplicate_result(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    with engine.begin() as c:
        execute(c,'UPDATE device_commands SET acknowledged_at=:t WHERE public_id=:id',t=now()-timedelta(seconds=10),id=command['id'])
    second = {**registration,'bootId':uid(),'previousBootId':registration['bootId']}
    assert device.post('/api/device/boot',json=second).status_code == 200
    device.headers['X-Device-Boot-Id'] = second['bootId']
    packet = {**event,'eventId':uid(),'sequence':1,'uptimeMs':500,'phase':'terminal',
              'roundBootId':registration['bootId'],'startUptimeMs':1000,'terminal':simulated_result('loss')}
    pending = device.post('/api/device/journal',json=packet)
    assert pending.status_code == 200 and pending.json()['reviewRequired']
    assert view(admin)['allowedActions'] == ['recover_result']
    response,body = resolution(admin,session,'recover_result')
    assert response.status_code == 200 and response.json()['score'] == 375
    assert device.post('/api/device/journal',json=packet).json() == pending.json()
    assert len(player.get('/api/player/context').json()['notifications']) == 1
    with engine.connect() as c:
        assert one(c,"SELECT COUNT(*) AS n FROM game_sessions WHERE status='completed'")['n'] == 1


def test_recovery_auth_csrf_revision_and_evidence_guards(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    path = f'/api/admin/sessions/{session}/fence'
    body = {'reason':'Test','expectedRevision':1}
    assert player.post(path,json=body).status_code == 401
    assert TestClient(app).post('/api/device/boot',json=registration).status_code == 401
    assert admin.post(path,json=body,headers={'X-CSRF-Token':'bad'}).status_code == 403
    assert post(admin,path,{**body,'expectedRevision':9}).status_code == 409
    assert fence(admin,session).status_code == 200
    assert device.post('/api/device/journal',json=fence_receipt(device,session)).status_code == 200
    evidence = view(admin)
    assert post(admin,f'/api/admin/sessions/{session}/resolve',{
        'reason':'Test','expectedRevision':evidence['revision'],'evidenceId':uid(),'action':'release_unstarted'}).status_code == 409
    assert 'storageId' not in player.get('/api/player/context').text


def emulator_setup(environment,tmp_path):
    app,admin,token,engine,settings = environment
    device = TestClient(app,headers={'X-Device-Token':settings.device_token})
    clock = [0]
    emulator = RecoveryEmulator(device,tmp_path/'recovery.json',clock=lambda:clock[0])
    emulator.connect()
    join(app,token,1)
    device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic-emulator'})
    session = post(admin,'/api/admin/queue/call-next').json()['sessionId']
    clock[0] = 100
    return device,emulator,clock,session


def test_emulator_lost_journal_receipt_survives_disk_reload(environment,tmp_path):
    device,emulator,clock,session = emulator_setup(environment,tmp_path)
    import httpx
    original = device.post

    def lose_response(path,**kwargs):
        response = original(path,**kwargs)
        if path == '/api/device/journal':
            assert response.status_code == 200
            raise httpx.ReadTimeout('Synthetic response loss after commit')
        return response

    device.post = lose_response
    with pytest.raises(httpx.ReadTimeout):
        emulator.poll_once()
    device.post = original
    recovered = RecoveryEmulator(device,tmp_path/'recovery.json',clock=lambda:clock[0])
    assert recovered.saved.pending is not None
    recovered.poll_once()
    assert recovered.saved.pending is None and recovered.saved.rounds[session].accepted
    app,admin,token,engine,settings = environment
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM device_journal_events')['n'] == 1
    assert fence(admin,session).status_code == 200
    recovered.poll_once()
    assert view(admin)['allowedActions'] == ['release_unstarted']
    with pytest.raises(ValueError,match='unfenced'):
        recovered.start_round(session)


def test_emulator_reboot_recovers_saved_terminal_after_missing_server_start(environment,tmp_path):
    device,emulator,clock,session = emulator_setup(environment,tmp_path)
    app,admin,token,engine,settings = environment
    emulator.poll_once()
    # A local start/terminal journal survives a power loss before server start delivery.
    saved = emulator.saved.rounds[session]
    saved.roundBootId = emulator.saved.registration.bootId
    saved.startUptimeMs = 1000
    emulator.save_terminal(session,simulated_result('loss'))
    with engine.begin() as c:
        execute(c,'UPDATE device_commands SET acknowledged_at=:t WHERE public_id=:id',t=now()-timedelta(seconds=10),id=saved.commandId)
    emulator.reboot()
    result = emulator.report_terminal(session)
    assert result['reviewRequired'] is True
    assert resolution(admin,session,'recover_result')[0].json()['score'] == 375


def test_emulator_corrupt_journal_is_preserved_before_network(tmp_path):
    path = tmp_path/'recovery.json'
    path.write_text('{"version":2,"registration":{}}',encoding='utf-8')
    class NoNetwork:
        headers = {}
        def post(self,*args,**kwargs):
            raise AssertionError('Corrupt journals must fail before network')
    with pytest.raises(ValueError):
        RecoveryEmulator(NoNetwork(),path)
    assert path.read_text(encoding='utf-8') == '{"version":2,"registration":{}}'


def test_emulator_rejected_start_can_still_receive_and_acknowledge_a_stop(environment,tmp_path):
    device,emulator,clock,session = emulator_setup(environment,tmp_path)
    app,admin,token,engine,settings = environment
    emulator.poll_once()
    assert fence(admin,session).status_code == 200
    clock[0] = 1000
    assert emulator.start_round(session)['reviewRequired'] is True
    assert len(emulator.saved.rejected) == 1
    assert emulator.saved.pending is None
    emulator.poll_once()
    assert view(admin)['allowedActions'] == ['void_interrupted']


@pytest.mark.parametrize('phase',['started','terminal'])
def test_extreme_uptime_is_rejected_without_datetime_overflow(environment,phase):
    device,player,registration,session,command,event = setup(environment)
    packet = {**event,'eventId':uid(),'sequence':2,'phase':phase,'uptimeMs':2**53-1,
              'roundBootId':registration['bootId'],'startUptimeMs':2**53-1}
    if phase == 'terminal':
        packet['terminal'] = simulated_result('loss')
    assert device.post('/api/device/journal',json=packet).status_code == 422


def test_two_operators_cannot_resolve_one_fence_twice(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    assert fence(admin,session).status_code == 200
    assert device.post('/api/device/journal',json=fence_receipt(device,session)).status_code == 200
    proof = view(admin)
    body = {'expectedRevision':proof['revision'],'evidenceId':proof['evidenceId'],
            'action':'release_unstarted','reason':'Concurrent reviewed decision'}
    with ThreadPoolExecutor(2) as pool:
        responses = list(pool.map(lambda _:post(admin,f'/api/admin/sessions/{session}/resolve',body),range(2)))
    assert sorted(r.status_code for r in responses) == [200,409]
    with engine.connect() as c:
        assert one(c,"SELECT COUNT(*) AS n FROM audit_logs WHERE action='device_resolve'")['n'] == 1


def test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started(environment):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    assert fence(admin,session).status_code == 200
    assert device.post('/api/device/journal',json=fence_receipt(device,session)).status_code == 200
    old = view(admin)
    second = {**registration,'bootId':uid(),'previousBootId':registration['bootId'],'storageId':uid()}
    assert device.post('/api/device/boot',json=second).status_code == 200
    device.headers['X-Device-Boot-Id'] = second['bootId']
    assert view(admin)['allowedActions'] == []
    assert post(admin,f'/api/admin/sessions/{session}/resolve',{
        'expectedRevision':old['revision'],'evidenceId':old['evidenceId'],
        'action':'release_unstarted','reason':'Stale boot proof'}).status_code == 409
    assert fence(admin,session).status_code == 200
    packet = fence_receipt(device,session,sequence=1)
    assert device.post('/api/device/journal',json=packet).status_code == 409
    packet['phase'] = 'fenced_interrupted'
    assert device.post('/api/device/journal',json=packet).status_code == 200
    assert view(admin)['allowedActions'] == ['void_interrupted']


@pytest.mark.parametrize('mutation',['rules','trace','timing'])
def test_invalid_terminal_cannot_be_recovered_or_notified(environment,mutation):
    device,player,registration,session,command,event = setup(environment)
    app,admin,token,engine,settings = environment
    payload = simulated_result('loss')
    if mutation == 'rules':
        payload['rulesHash'] = '0'*64
    if mutation == 'trace':
        payload['placements'][0]['overlap_width'] = 0
    packet = {**event,'eventId':uid(),'sequence':2,'uptimeMs':10000,'phase':'terminal',
              'roundBootId':registration['bootId'],'startUptimeMs':1000,'terminal':payload}
    if mutation != 'timing':
        with engine.begin() as c:
            execute(c,'UPDATE device_commands SET acknowledged_at=:t WHERE public_id=:id',t=now()-timedelta(seconds=10),id=command['id'])
    assert device.post('/api/device/journal',json=packet).status_code == 422
    assert view(admin)['allowedActions'] == []
    assert player.get('/api/player/context').json()['notifications'] == []
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) AS n FROM device_journal_events')['n'] == 1
