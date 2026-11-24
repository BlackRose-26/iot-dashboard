"""Operator and administrator roles (24 Nov 2026), against a disposable XAMPP database."""
import re
import uuid

from fastapi.testclient import TestClient

from test_player_flow import environment, join  # noqa: F401

PASSWORD = re.compile(r'^[a-z2-9]{4}(-[a-z2-9]{4}){3}$')


def sign_in(app, username, password):
    client = TestClient(app)
    response = client.post('/api/admin/login', json={'username': username, 'password': password})
    if response.status_code != 200:
        return client, response
    client.headers['X-CSRF-Token'] = client.get('/api/admin/session').json()['csrf']
    return client, response


def add_operator(admin, name='booth.helper'):
    response = admin.post('/api/admin/staff', json={'username': name})
    assert response.status_code == 200, response.text
    body = response.json()
    assert PASSWORD.match(body['password']) and body['staff']['role'] == 'operator'
    assert 'no-store' in response.headers['cache-control'], 'one-time passwords must never be cached'
    return body


def recovery(action):
    return {'expectedRevision': 1, 'reason': 'Synthetic test', 'evidenceId': str(uuid.uuid4()), 'action': action}


def test_operator_runs_the_line_but_cannot_change_scores_accounts_or_training(environment):
    app, admin, token, engine, settings = environment
    assert admin.get('/api/admin/session').json()['role'] == 'admin'
    created = add_operator(admin)
    operator, login = sign_in(app, 'Booth.Helper', created['password'])
    assert login.status_code == 200 and login.json()['role'] == 'operator'
    assert operator.get('/api/admin/session').json() | {'csrf': None} == {'username': 'booth.helper', 'role': 'operator', 'csrf': None}

    # Running the line is allowed.
    join(app, token, 1)
    assert operator.get('/api/admin/snapshot').status_code == 200
    assert operator.get('/api/admin/analytics').status_code == 200
    assert operator.post('/api/admin/admissions', json={'open': False}).status_code == 200
    assert operator.post('/api/admin/admissions', json={'open': True}).status_code == 200
    player = operator.get('/api/admin/players', params={'search': 'Test 1'}).json()['players'][0]
    assert operator.post(f"/api/admin/players/{player['id']}/reentry").status_code == 200
    unknown = str(uuid.uuid4())
    headers = {'Idempotency-Key': str(uuid.uuid4())}
    # A no-show release passes the role check (and then fails only because the round does not exist).
    assert operator.post(f'/api/admin/sessions/{unknown}/resolve', json=recovery('release_unstarted'), headers=headers).status_code == 409

    # Score decisions, accounts, training, question review and the simulator are admin-only.
    for action in ('void_interrupted', 'recover_result'):
        response = operator.post(f'/api/admin/sessions/{unknown}/resolve', json=recovery(action), headers={'Idempotency-Key': str(uuid.uuid4())})
        assert response.status_code == 403 and response.json()['detail'] == 'Only an administrator can do this.'
    denied = [
        operator.get('/api/admin/staff'),
        operator.post('/api/admin/staff', json={'username': 'sneaky'}),
        operator.post(f"/api/admin/staff/{created['staff']['id']}/password"),
        operator.get('/api/admin/assistant/training/options'),
        operator.get('/api/admin/assistant/training'),
        operator.post('/api/admin/assistant/training/export'),
        operator.get('/api/admin/evaluation-review'),
        operator.post('/api/admin/simulator/ready'),
    ]
    assert [r.status_code for r in denied] == [403] * len(denied)
    assert admin.post('/api/admin/simulator/ready').status_code == 200


def test_admin_manages_operator_accounts_with_audit(environment):
    app, admin, token, engine, settings = environment
    created = add_operator(admin, 'gate-1')
    staff_id = created['staff']['id']
    assert admin.post('/api/admin/staff', json={'username': 'GATE-1'}).status_code == 409
    assert admin.post('/api/admin/staff', json={'username': 'bad name!'}).status_code == 422
    assert admin.post('/api/admin/staff', json={'username': 'ok', 'role': 'admin'}).status_code == 422
    listed = admin.get('/api/admin/staff').json()['staff']
    assert [(s['username'], s['role'], s['enabled']) for s in listed] == [('admin', 'admin', True), ('gate-1', 'operator', True)]
    assert 'password' not in str(listed).lower()

    # The administrator account cannot be disabled or reset from the dashboard.
    admin_id = listed[0]['id']
    assert admin.post(f'/api/admin/staff/{admin_id}/enabled', json={'enabled': False}).status_code == 403
    assert admin.post(f'/api/admin/staff/{admin_id}/password').status_code == 403
    assert admin.post('/api/admin/staff/999999/password').status_code == 404

    operator, _ = sign_in(app, 'gate-1', created['password'])
    assert admin.post(f'/api/admin/staff/{staff_id}/enabled', json={'enabled': False}).json()['staff']['enabled'] is False
    assert operator.get('/api/admin/snapshot').status_code == 401, 'disabling signs the operator out'
    assert sign_in(app, 'gate-1', created['password'])[1].status_code == 401
    assert admin.post(f'/api/admin/staff/{staff_id}/enabled', json={'enabled': True}).status_code == 200

    operator, _ = sign_in(app, 'gate-1', created['password'])
    reset = admin.post(f'/api/admin/staff/{staff_id}/password').json()
    assert PASSWORD.match(reset['password']) and reset['password'] != created['password']
    assert operator.get('/api/admin/snapshot').status_code == 401, 'a reset signs the operator out'
    assert sign_in(app, 'gate-1', created['password'])[1].status_code == 401
    assert sign_in(app, 'gate-1', reset['password'])[1].status_code == 200

    with engine.connect() as c:
        rows = c.exec_driver_sql("SELECT action,entity_type,details_safe FROM audit_logs WHERE entity_type='staff' ORDER BY id").all()
    assert [r[0] for r in rows] == ['staff_created', 'staff_disabled', 'staff_enabled', 'staff_password_reset']
    assert all(created['password'] not in r[2] and reset['password'] not in r[2] for r in rows)


def test_staff_changes_need_csrf(environment):
    app, admin, token, engine, settings = environment
    no_csrf = TestClient(app)
    no_csrf.cookies = admin.cookies
    assert no_csrf.post('/api/admin/staff', json={'username': 'nocsrf'}).status_code in (401, 403)
    assert TestClient(app).get('/api/admin/staff').status_code == 401


def test_one_strangers_wrong_guesses_through_the_tunnel_do_not_lock_out_staff(environment):
    app, admin, token, engine, settings = environment
    tunnel = TestClient(app, client=('127.0.0.1', 50000))  # cloudflared connects from this PC
    stranger = {'CF-Connecting-IP': '203.0.113.7'}
    for _ in range(8):
        assert tunnel.post('/api/admin/login', json={'username': 'admin', 'password': 'wrong'}, headers=stranger).status_code == 401
    assert tunnel.post('/api/admin/login', json={'username': 'admin', 'password': 'wrong'}, headers=stranger).status_code == 429
    staff_phone = {'CF-Connecting-IP': '198.51.100.20'}
    ok = tunnel.post('/api/admin/login', json={'username': 'admin', 'password': 'Only-a-disposable-test-password'}, headers=staff_phone)
    assert ok.status_code == 200, 'the stranger is limited, not every staff member'
    # The header is ignored from anyone but a loopback peer, so it cannot be used to dodge the limit.
    remote = TestClient(app, client=('192.0.2.50', 50000))
    for index in range(8):
        remote.post('/api/admin/login', json={'username': 'admin', 'password': 'wrong'}, headers={'CF-Connecting-IP': f'10.0.0.{index}'})
    assert remote.post('/api/admin/login', json={'username': 'admin', 'password': 'wrong'}, headers={'CF-Connecting-IP': '10.0.0.99'}).status_code == 429
