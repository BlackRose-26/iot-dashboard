import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
import secrets
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pymysql
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import URL

from app.config import Settings
from app.database import make_engine, one, execute
from app.game import simulated_result
from app.main import create_app
from setup_local import migrate, seed


@pytest.fixture
def environment():
    # Disposable, uniquely named MariaDB database. Never use the application's database.
    database='stack_moko_test_'+secrets.token_hex(5)
    root=pymysql.connect(host='127.0.0.1',user='root',password=os.getenv('STACK_DB_ROOT_PASSWORD',''),autocommit=True)
    migrate(root,database)
    settings=Settings(database_url=URL.create('mysql+pymysql',username='root',password=os.getenv('STACK_DB_ROOT_PASSWORD',''),host='127.0.0.1',database=database).render_as_string(hide_password=False),identity_key=secrets.token_bytes(32),lookup_key=secrets.token_bytes(32),csrf_key=secrets.token_bytes(32),device_token='disposable-test-device-token')
    engine=make_engine(settings.database_url)
    seed(engine,settings,'Only-a-disposable-test-password')
    app=create_app(settings)
    admin=TestClient(app)
    assert admin.post('/api/admin/login',json={'username':'admin','password':'Only-a-disposable-test-password'}).status_code==200
    csrf=admin.get('/api/admin/session').json()['csrf']
    admin.headers['X-CSRF-Token']=csrf
    token=admin.get('/api/admin/snapshot').json()['qrPath'].split('/')[-1]
    yield app,admin,token,engine,settings
    admin.close();app.state.engine.dispose();engine.dispose()
    assert database.startswith('stack_moko_test_') and len(database)==26
    with root.cursor() as c: c.execute(f'DROP DATABASE `{database}`')
    root.close()


def entry_payload(token, method='upload'):
    return {'qrContent':'http://127.0.0.1:5173/join/'+token,'method':method}


def join(app,token,index):
    player=TestClient(app)
    assert player.post('/api/player/entry',json=entry_payload(token)).status_code==200
    context=player.get('/api/player/context').json()
    player.headers['X-CSRF-Token']=context['csrf']
    response=player.post('/api/player/register',json={'nickname':f'Test {index}','studentId':f'DUMMY-TEST-{index}','acknowledged':True})
    assert response.status_code==200,response.text
    player.headers['X-CSRF-Token']=player.get('/api/player/context').json()['csrf']
    return player


def post(admin,path,body=None,key=None):
    return admin.post(path,json=body,headers={'Idempotency-Key':key or str(uuid.uuid4())})


def accept_command(device):
    command=device.get('/api/device/commands').json()['commands'][0]
    response=device.post(f"/api/device/commands/{command['id']}/ack",json={
        'sessionId':command['sessionId'],'expectedRevision':command['expectedRevision'],'status':'accepted'})
    assert response.status_code==200,response.text
    return command


def test_access_control_csrf_and_privacy(environment):
    app,admin,token,engine,settings=environment
    guest=TestClient(app)
    assert guest.get('/api/admin/snapshot').status_code==401
    assert guest.post('/api/admin/queue/call-next').status_code==401
    assert guest.post('/api/player/register',json={'nickname':'Test','studentId':'DUMMY-TEST-1','acknowledged':True}).status_code==403
    p=join(app,token,1)
    assert p.get('/api/admin/snapshot').status_code==401
    assert p.get('/api/player/leaderboard').status_code==403
    assert p.post('/api/admin/admissions',json={'open':False}).status_code==401
    assert admin.post('/api/admin/admissions',json={'open':False},headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert admin.post('/api/admin/admissions',json={'open':False},headers={'Origin':'https://evil.example'}).status_code==403
    private=p.get('/api/player/context').text
    public=admin.get('/api/admin/snapshot').text
    for payload in (private,public):
        assert 'DUMMY-TEST' not in payload and 'id_lookup' not in payload and 'encrypted_id' not in payload
    malformed=p.post('/api/player/register',json={'nickname':'Test','studentId':['DUMMY-PRIVATE'],'acknowledged':True})
    assert malformed.status_code==422 and 'DUMMY-PRIVATE' not in malformed.text
    assert TestClient(app).get('/api/player/context').json()['ticket'] is None
    assert admin.post('/api/admin/logout').status_code==200
    assert admin.get('/api/admin/snapshot').status_code==401


def test_fifo_concurrency_idempotency_and_results(environment):
    app,admin,token,engine,settings=environment
    first=join(app,token,1);second=join(app,token,2)
    assert first.get('/api/player/context').json()['ticket']['position']==1
    assert second.get('/api/player/context').json()['ticket']['position']==2
    assert post(admin,'/api/admin/queue/call-next').status_code==409  # no device heartbeat
    assert post(admin,'/api/admin/simulator/ready').status_code==200
    key=str(uuid.uuid4())
    with ThreadPoolExecutor(2) as pool:
        results=list(pool.map(lambda _:post(admin,'/api/admin/queue/call-next',key=key),range(2)))
    assert all(r.status_code==200 for r in results),[r.text for r in results]
    assert results[0].json()==results[1].json()
    assert post(admin,'/api/admin/queue/call-next').status_code==409
    assert first.get('/api/player/context').json()['ticket']['status']=='called'
    assert second.get('/api/player/context').json()['ticket']['position']==1
    assert post(admin,'/api/admin/simulator/start').status_code==200
    assert first.get('/api/player/context').json()['ticket']['status']=='playing'
    assert post(admin,'/api/admin/simulator/win').status_code==200
    first_context=first.get('/api/player/context').json()
    assert first_context['ticket']['outcome']=='win' and first_context['ticket']['score']==1500
    assert len(first_context['notifications'])==1
    assert first.get('/api/player/leaderboard').status_code==200
    assert second.get('/api/player/leaderboard').status_code==403
    post(admin,'/api/admin/queue/call-next');post(admin,'/api/admin/simulator/start')
    assert post(admin,'/api/admin/simulator/loss').status_code==200
    assert second.get('/api/player/context').json()['ticket']['outcome']=='loss'
    assert len(second.get('/api/player/context').json()['notifications'])==1
    assert len(second.get('/api/player/leaderboard').json()['rounds'])==2


def test_registration_retries_duplicates_pause_and_cancel(environment):
    app,admin,token,engine,settings=environment
    p=join(app,token,1)
    # Retrying a consumed entry with its authenticated owner cannot add a duplicate.
    response=p.post('/api/player/register',json={'nickname':'Test 1','studentId':'DUMMY-TEST-1','acknowledged':True})
    assert response.status_code==200
    assert len(admin.get('/api/admin/snapshot').json()['queue'])==1
    stranger=TestClient(app);stranger.post('/api/player/entry',json=entry_payload(token))
    stranger.headers['X-CSRF-Token']=stranger.get('/api/player/context').json()['csrf']
    assert stranger.post('/api/player/register',json={'nickname':'Other','studentId':'DUMMY-TEST-1','acknowledged':True}).status_code==409
    assert stranger.get('/api/player/context').json()['ticket'] is None
    assert p.post('/api/player/cancel').status_code==200
    assert p.get('/api/player/context').json()['ticket']['status']=='cancelled'
    post(admin,'/api/admin/admissions',{'open':False})
    assert stranger.post('/api/player/register',json={'nickname':'Other','studentId':'DUMMY-TEST-2','acknowledged':True}).status_code==409


def test_device_result_replay_and_cohort_separation(environment):
    app,admin,token,engine,settings=environment
    p=join(app,token,1)
    device=TestClient(app,headers={'X-Device-Token':settings.device_token})
    assert TestClient(app).post('/api/device/heartbeat',json={'state':'ready','firmware':'test'}).status_code==401
    assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'test','rssi':-55}).status_code==200
    session=post(admin,'/api/admin/queue/call-next').json()['sessionId']
    accept_command(device)
    assert device.post(f'/api/device/sessions/{session}/start').status_code==200
    payload=simulated_result('loss')
    with engine.begin() as c:
        from app.security import now
        from datetime import timedelta
        execute(c,'UPDATE game_sessions SET started_at=:start WHERE public_id=:id',start=now()-timedelta(seconds=60),id=session)
    bad=dict(payload,score=99999,placements=[dict(payload['placements'][0],overlap_width=8)])
    assert device.post(f'/api/device/sessions/{session}/result',json=bad).status_code==422
    result=device.post(f'/api/device/sessions/{session}/result',json=payload)
    assert result.status_code==200,result.text
    completed_revision=p.get('/api/player/context').json()['revision']
    assert device.post(f'/api/device/sessions/{session}/result',json=payload).json()==result.json()
    assert device.post(f'/api/device/sessions/{session}/result',json=dict(payload,terminalId=str(uuid.uuid4()))).status_code==409
    assert p.get('/api/player/context').json()['revision']==completed_revision
    assert p.get('/api/player/leaderboard').json()['source']=='device'


def test_identity_encryption_and_cookie_flags(environment):
    app,admin,token,engine,settings=environment
    p=join(app,token,1)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    with engine.connect() as c:
        record=one(c,'SELECT i.*,p.public_id FROM student_identities i JOIN players p ON p.id=i.player_id LIMIT 1')
        assert b'DUMMY-TEST-1' not in record['encrypted_id']
        decoded=AESGCM(settings.identity_key).decrypt(record['nonce'],record['encrypted_id']+record['auth_tag'],record['public_id'].encode())
        assert decoded==b'DUMMY-TEST-1'
    cookie=next(cookie for cookie in p.cookies.jar if cookie.name=='sm_player')
    assert 'HttpOnly' in cookie._rest and cookie._rest.get('SameSite')=='strict'
    assert cookie.path=='/api'


def test_rate_limit_expired_sessions_and_skip_audit(environment):
    app,admin,token,engine,settings=environment
    stranger=TestClient(app)
    for _ in range(8): assert stranger.post('/api/admin/login',json={'username':'other-admin','password':'incorrect'}).status_code==401
    assert stranger.post('/api/admin/login',json={'username':'other-admin','password':'incorrect'}).status_code==429
    p=join(app,token,1)
    ticket=p.get('/api/player/context').json()['ticket']['id']
    assert post(admin,f'/api/admin/queue/{ticket}/skip',{'reason':' '}).status_code==422
    assert post(admin,f'/api/admin/queue/{ticket}/skip',{'reason':'Synthetic test: player absent'}).status_code==200
    assert p.get('/api/player/context').json()['ticket']['status']=='cancelled'
    with engine.begin() as c:
        assert one(c,"SELECT COUNT(*) AS n FROM audit_logs WHERE action='queue_skipped'")['n']==1
        execute(c,"UPDATE auth_sessions SET expires_at='2000-01-01' WHERE staff_user_id IS NOT NULL")
    assert admin.get('/api/admin/snapshot').status_code==401


def test_leaderboard_relocks_on_next_registration(environment):
    app,admin,token,engine,settings=environment
    p=join(app,token,1)
    post(admin,'/api/admin/simulator/ready');post(admin,'/api/admin/queue/call-next');post(admin,'/api/admin/simulator/start');post(admin,'/api/admin/simulator/loss')
    assert p.get('/api/player/leaderboard').status_code==200
    assert p.post('/api/player/entry',json=entry_payload(token)).status_code==200
    p.headers['X-CSRF-Token']=p.get('/api/player/context').json()['csrf']
    assert p.post('/api/player/register',json={'nickname':'Test 1','studentId':'DUMMY-TEST-1','acknowledged':True}).status_code==200
    assert p.get('/api/player/leaderboard').status_code==403


def test_scanner_entry_contract_rejects_unregistered_and_unrelated_content(environment):
    app,admin,token,engine,settings=environment
    guest=TestClient(app)
    assert guest.post('/api/player/entry',json={'token':token}).status_code==422
    assert guest.get('/api/player/context').json()['canRegister'] is False
    for content in ['https://other.example/join/'+token, 'javascript:alert(1)', 'http://127.0.0.1:5173/admin/login']:
        assert guest.post('/api/player/entry',json={'qrContent':content,'method':'upload'}).status_code==422
    assert guest.post('/api/player/entry',json=entry_payload(token,'manual')).status_code==422
    assert guest.post('/api/player/entry',json=entry_payload('a'*43)).status_code==404
    assert guest.get('/api/player/context').json()['canRegister'] is False
    for method in ('camera','upload'):
        assert guest.post('/api/player/entry',json=entry_payload(token,method)).status_code==200
        assert guest.get('/api/player/context').json()['canRegister'] is True
    with engine.begin() as c: execute(c,'UPDATE qr_links SET enabled=0')
    assert guest.post('/api/player/entry',json=entry_payload(token)).status_code==404
