import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
import json
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.database import execute, one
from app.game import MATRIX_RULES, RULES, active_rules, replay, rules_hash, simulated_result
from app.analytics import collect, collect_all
from app.security import now
from test_player_flow import environment, join, post
from test_device_recovery import setup as recovery_setup, fence, resolution, uid


def activate(engine):
    with engine.begin() as c:
        execute(c, "UPDATE events SET settings=JSON_SET(settings,'$.active_ruleset','matrix-v1') WHERE id=1")
        assert active_rules(c)[1] == MATRIX_RULES


def test_erased_wokwi_storage_discovers_lineage_but_cannot_claim_never_started(environment):
    app,admin,token,engine,settings=environment
    device,player,old,session,command,event=recovery_setup(environment)
    fresh=TestClient(app,headers={'X-Device-Token':settings.device_token})
    assert TestClient(app).get('/api/device/enrollment').status_code==401
    assert player.get('/api/device/enrollment').status_code==401
    assert admin.get('/api/device/enrollment').status_code==401
    lineage=fresh.get('/api/device/enrollment').json()
    assert lineage=={'currentBootId':old['bootId']}
    registration={'bootId':uid(),'previousBootId':lineage['currentBootId'],'storageId':uid(),'uptimeMs':0}
    assert fresh.post('/api/device/boot',json=registration).status_code==200
    fresh.headers['X-Device-Boot-Id']=registration['bootId']
    assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'old-test-boot'}).status_code==409
    assert admin.get('/api/admin/snapshot').json()['machineState']=='review'
    assert fence(admin,session).status_code==200
    stop=fresh.get('/api/device/commands').json()['commands'][0]
    assert stop['deliverySequence']>command['deliverySequence']
    packet={'eventId':uid(),'sequence':1,'uptimeMs':100,'sessionId':session,
            'commandId':stop['id'],'expectedRevision':stop['expectedRevision'],'phase':'fenced_unstarted'}
    assert fresh.post('/api/device/journal',json=packet).status_code==409
    packet.update(eventId=uid(),phase='fenced_interrupted')
    assert fresh.post('/api/device/journal',json=packet).status_code==200
    response,_=resolution(admin,session,'void_interrupted')
    assert response.status_code==200
    context=player.get('/api/player/context').json()
    assert context['ticket']['score'] is None and context['notifications']==[]


def test_matrix_win_timeout_and_invalid_trace():
    win = simulated_result('win', MATRIX_RULES)
    result = replay(win['placements'], win['durationMs'], 'win', MATRIX_RULES)
    assert result['score'] == result['level'] == result['perfect'] == 15
    assert replay([], 60000, 'loss', MATRIX_RULES)['score'] == 0
    assert replay([], 60000, 'loss', RULES)['score'] == 0
    assert replay(simulated_result('loss', MATRIX_RULES)['placements'], 60000, 'loss', MATRIX_RULES)['score'] == 3
    with pytest.raises(ValueError): replay(win['placements'], win['durationMs'], 'win', RULES)
    bad = [dict(p) for p in win['placements']]
    bad[0]['candidate_x'] += 1
    with pytest.raises(ValueError): replay(bad, win['durationMs'], 'win', MATRIX_RULES)
    with pytest.raises(ValueError): replay([], 59999, 'loss', MATRIX_RULES)


def test_matrix_assignment_completion_analytics_and_private_leaderboard(environment):
    app, admin, token, engine, settings = environment
    activate(engine)
    device, player, registration, session, command, reserved = recovery_setup(environment)
    assert command['rules'] == MATRIX_RULES
    assert command['rulesHash'] == rules_hash(MATRIX_RULES).hex()
    start = dict(reserved, eventId=__import__('uuid').uuid4().__str__(), sequence=2,
                 phase='started', uptimeMs=100, roundBootId=registration['bootId'], startUptimeMs=100)
    assert device.post('/api/device/journal', json=start).status_code == 200
    terminal = simulated_result('win', MATRIX_RULES)
    with engine.begin() as c:
        execute(c, "UPDATE game_sessions SET started_at=:at WHERE public_id=:id", at=now()-timedelta(seconds=20),id=session)
        execute(c, "UPDATE device_commands SET acknowledged_at=:at WHERE session_id=(SELECT id FROM game_sessions WHERE public_id=:id)",at=now()-timedelta(seconds=20),id=session)
    event = dict(start, eventId=__import__('uuid').uuid4().__str__(), sequence=3, phase='terminal',
                 uptimeMs=100+terminal['durationMs'], terminal=terminal)
    response=device.post('/api/device/journal',json=event)
    assert response.status_code == 200, response.text
    assert response.json()['score'] == 15
    assert device.post('/api/device/journal',json=event).json() == response.json()
    ticket=player.get('/api/player/context').json()
    assert ticket['ticket']['score'] == 15 and ticket['ticket']['game']['levels'] == 15
    assert len(ticket['notifications']) == 1
    board=player.get('/api/player/leaderboard').json()
    assert board['game']['code']=='matrix-v1' and len(board['rounds'])==1
    snapshot=admin.get('/api/admin/snapshot').json()
    assert snapshot['game']['levels']==15 and snapshot['rounds'][0]['maxLevel']==15
    data=collect(engine,source='device')
    assert len(data['levels'])==15 and data['summary']['highest_score']==15
    assert sum(b['rounds'] for b in data['scores'])==1 and data['scores'][-1]['label']=='12–15'
    assert collect_all(engine)['scope']['ruleset']=='matrix-v1'
    assert 'DUMMY-TEST' not in json.dumps(command)


def test_old_reserved_round_keeps_original_rules_after_activation(environment):
    app, admin, token, engine, settings = environment
    device, player, registration, session, command, reserved = recovery_setup(environment)
    activate(engine)
    from app.game import simulated_result
    payload=simulated_result('win')
    start=dict(reserved, eventId=str(__import__('uuid').uuid4()), sequence=2, phase='started',
               roundBootId=registration['bootId'],startUptimeMs=100)
    assert device.post('/api/device/journal',json=start).status_code==200
    with engine.begin() as c:
        execute(c,"UPDATE game_sessions SET started_at=:at WHERE public_id=:id",at=now()-timedelta(seconds=40),id=session)
        execute(c,"UPDATE device_commands SET acknowledged_at=:at WHERE session_id=(SELECT id FROM game_sessions WHERE public_id=:id)",at=now()-timedelta(seconds=40),id=session)
    event=dict(start,eventId=str(__import__('uuid').uuid4()),sequence=3,phase='terminal',uptimeMs=100+payload['durationMs'],terminal=payload)
    response=device.post('/api/device/journal',json=event)
    assert response.status_code==200,response.text
    assert response.json()['score']==1500
    assert player.get('/api/player/leaderboard').json()['game']['code']=='classic-v1'
    assert admin.get('/api/admin/snapshot').json()['rounds']==[]
    assert collect(engine,source='device')['summary']['completed_games']==0
