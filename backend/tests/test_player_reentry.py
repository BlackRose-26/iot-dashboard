"""Operator-assisted ticket re-entry (24 Nov 2026), against a disposable XAMPP database."""
from fastapi.testclient import TestClient

from test_player_flow import environment, join, entry_payload  # noqa: F401


def reentry_token(admin, player_id):
    response = admin.post(f'/api/admin/players/{player_id}/reentry')
    assert response.status_code == 200, response.text
    path = response.json()['path']
    assert path.startswith('/reenter#') and '?' not in path, 'the token must ride in the URL fragment'
    return path.split('#', 1)[1]


def find(admin, search):
    return admin.get('/api/admin/players', params={'search': search}).json()['players']


def test_lost_ticket_is_restored_once_and_old_device_is_signed_out(environment):
    app, admin, token, engine, settings = environment
    old_phone = join(app, token, 1)
    assert old_phone.get('/api/player/context').json()['ticket']['status'] == 'waiting'
    found = find(admin, 'Test 1')
    assert [p['nickname'] for p in found] == ['Test 1'] and found[0]['ticket'] == 'waiting'
    assert 'studentId' not in found[0] and 'student' not in str(found[0]).lower()

    # A new hostname/phone has no cookie, and registering again is refused.
    new_phone = TestClient(app)
    assert new_phone.post('/api/player/entry', json=entry_payload(token)).status_code == 200
    new_phone.headers['X-CSRF-Token'] = new_phone.get('/api/player/context').json()['csrf']
    again = new_phone.post('/api/player/register', json={'nickname': 'Test 1', 'studentId': 'DUMMY-TEST-1', 'acknowledged': True})
    assert again.status_code == 409

    code = reentry_token(admin, found[0]['id'])
    restored = new_phone.post('/api/player/reenter', json={'token': code})
    assert restored.status_code == 200, restored.text
    ticket = new_phone.get('/api/player/context').json()['ticket']
    assert ticket['status'] == 'waiting' and ticket['nickname'] == 'Test 1'
    assert old_phone.get('/api/player/context').json().get('ticket') is None, 'the old device is signed out'

    third = TestClient(app)
    assert third.post('/api/player/reenter', json={'token': code}).status_code == 410, 'single use'
    with engine.connect() as c:
        actions = [row[0] for row in c.exec_driver_sql("SELECT action FROM audit_logs WHERE action='player_reentry_issued'")]
    assert actions == ['player_reentry_issued']


def test_only_the_newest_code_works_and_expired_codes_fail(environment):
    app, admin, token, engine, settings = environment
    join(app, token, 2)
    player = find(admin, 'Test 2')[0]
    first = reentry_token(admin, player['id'])
    second = reentry_token(admin, player['id'])
    phone = TestClient(app)
    assert phone.post('/api/player/reenter', json={'token': first}).status_code == 410
    with engine.begin() as c:
        c.exec_driver_sql('UPDATE player_reentry_tokens SET expires_at=NOW(3) - INTERVAL 1 SECOND WHERE used_at IS NULL')
    assert phone.post('/api/player/reenter', json={'token': second}).status_code == 410


def test_reentry_requires_an_admin_and_csrf_and_rejects_bad_tokens(environment):
    app, admin, token, engine, settings = environment
    player = join(app, token, 3)
    target = find(admin, 'Test 3')[0]['id']
    assert player.post(f'/api/admin/players/{target}/reentry').status_code == 401
    assert player.get('/api/admin/players').status_code == 401
    no_csrf = TestClient(app)
    no_csrf.cookies = admin.cookies
    assert no_csrf.post(f'/api/admin/players/{target}/reentry').status_code in (401, 403)
    assert admin.post('/api/admin/players/not-a-player/reentry').status_code == 404
    anyone = TestClient(app)
    assert anyone.post('/api/player/reenter', json={'token': 'x' * 43}).status_code == 410
    assert anyone.post('/api/player/reenter', json={'token': 'short'}).status_code == 422
    assert find(admin, '%') == [] and find(admin, '_') == [], 'LIKE wildcards are matched literally'
