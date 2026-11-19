import asyncio
import json
import uuid

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.database import execute, one, all_rows
from app.live import LiveHub, record_change
from app.security import digest, now
from test_player_flow import environment, join, post

ORIGIN = {'Origin': 'http://127.0.0.1:5173'}


def revision(engine):
    with engine.connect() as c:
        return one(c, "SELECT revision FROM events WHERE code='acs-day'")['revision']


def test_outbox_is_atomic_and_recovers_after_dispatcher_restart(environment):
    app, admin, token, engine, settings = environment
    initial = revision(engine)
    with pytest.raises(ValueError):
        with engine.begin() as c:
            record_change(c, 'queue.changed')
            assert asyncio.run(LiveHub(engine).dispatch_once()) == 0
            raise ValueError('transaction rolls back')
    assert revision(engine) == initial
    with engine.connect() as c:
        assert one(c, 'SELECT COUNT(*) AS n FROM outbox_events')['n'] == 0
    # A committed change survives without a running dispatcher.
    with engine.begin() as c:
        record_change(c, 'event.changed')

    async def restart():
        hub = LiveHub(engine)
        queue = hub.subscribe(('admin', 1))
        assert await hub.dispatch_once() == 1
        assert await queue.get() == initial + 1
        assert await LiveHub(engine).dispatch_once() == 0
    asyncio.run(restart())
    with engine.connect() as c:
        assert one(c, 'SELECT published_at FROM outbox_events')['published_at']


def test_global_revisions_and_idempotent_operations(environment):
    app, admin, token, engine, settings = environment
    base = revision(engine)
    player = join(app, token, 1)
    assert revision(engine) == base + 1
    assert post(admin, '/api/admin/simulator/ready').status_code == 200
    key = str(uuid.uuid4())
    first = post(admin, '/api/admin/queue/call-next', key=key)
    current = revision(engine)
    assert post(admin, '/api/admin/queue/call-next', key=key).json() == first.json()
    assert revision(engine) == current
    assert post(admin, '/api/admin/simulator/start').status_code == 200
    started = revision(engine)
    assert post(admin, '/api/admin/simulator/start').status_code == 200
    assert revision(engine) == started
    assert post(admin, '/api/admin/simulator/win').status_code == 200
    completed = revision(engine)
    assert completed == base + 5
    assert player.get('/api/player/context').json()['revision'] == completed
    assert admin.get('/api/admin/snapshot').json()['revision'] == completed
    with engine.connect() as c:
        rows = all_rows(c, 'SELECT event_revision,payload_safe FROM outbox_events ORDER BY id')
        assert [r['event_revision'] for r in rows] == list(range(base + 1, completed + 1))
        assert all(json.loads(r['payload_safe']) == {} for r in rows)
    assert post(admin, '/api/admin/admissions', {'open': False}).status_code == 200
    paused = revision(engine)
    assert post(admin, '/api/admin/admissions', {'open': False}).status_code == 200
    assert revision(engine) == paused


def test_snapshot_revision_and_rows_share_a_consistent_database_view(environment, monkeypatch):
    app, admin, token, engine, settings = environment
    import app.main as routes
    original = routes.one
    initial = revision(engine)
    changed = False

    def commit_during_read(c, sql, **parameters):
        nonlocal changed
        row = original(c, sql, **parameters)
        if not changed and sql == "SELECT * FROM machines WHERE code='cabinet-01'":
            changed = True
            assert post(admin, '/api/admin/admissions', {'open': False}).status_code == 200
        return row

    monkeypatch.setattr(routes, 'one', commit_during_read)
    snapshot = admin.get('/api/admin/snapshot').json()
    assert changed and revision(engine) == initial + 1
    assert snapshot['revision'] == initial and snapshot['admissionsOpen'] is True
    latest = admin.get('/api/admin/snapshot').json()
    assert latest['revision'] == initial + 1 and latest['admissionsOpen'] is False


@pytest.mark.parametrize('path,headers', [
    ('/api/live/admin', ORIGIN),
    ('/api/live/player', ORIGIN),
    ('/api/live/public', ORIGIN),
])
def test_live_requires_the_right_authenticated_role(environment, path, headers):
    app, admin, token, engine, settings = environment
    with TestClient(app) as guest:
        with pytest.raises(WebSocketDisconnect):
            with guest.websocket_connect(path, headers=headers): pass


@pytest.mark.parametrize('headers', [{}, {'Origin': 'https://evil.example'}, {'Origin':'null'}])
def test_live_rejects_missing_or_foreign_origin(environment, headers):
    app, admin, token, engine, settings = environment
    with TestClient(app, cookies=admin.cookies) as client:
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect('/api/live/admin', headers=headers): pass


def test_player_notifications_are_safe_and_staff_channel_is_private(environment):
    app, admin, token, engine, settings = environment
    first = join(app, token, 1)
    second = join(app, token, 2)
    with TestClient(app, cookies=first.cookies) as player:
        with pytest.raises(WebSocketDisconnect):
            with player.websocket_connect('/api/live/admin', headers=ORIGIN): pass
        with player.websocket_connect('/api/live/player', headers=ORIGIN) as ws:
            ready = ws.receive_json()
            assert ready['type'] == 'ready'
            # Drain historic changes before creating a fresh one.
            assert post(admin, '/api/admin/simulator/ready').status_code == 200
            target = revision(engine)
            for _ in range(10):
                frame = ws.receive_json()
                assert set(frame) == {'type', 'revision'}
                if frame['revision'] >= target: break
            else: pytest.fail('Committed revision was not delivered')
            assert first.get('/api/player/context').json()['ticket']['position'] == 1
            assert second.get('/api/player/context').json()['ticket']['position'] == 2
            assert first.get('/api/player/leaderboard').status_code == 403


def test_logout_revokes_existing_socket_and_commands_are_rejected(environment):
    app, admin, token, engine, settings = environment
    app.state.live.heartbeat = 0.05
    with TestClient(app, cookies=admin.cookies) as client:
        with client.websocket_connect('/api/live/admin', headers=ORIGIN) as ws:
            assert ws.receive_json()['type'] == 'ready'
            assert admin.post('/api/admin/logout').status_code == 200
            with pytest.raises(WebSocketDisconnect) as closed:
                ws.receive_json()
            assert closed.value.code == 1008
    # An authenticated player cannot use the stream to mutate the game.
    first = join(app, token, 1)
    with TestClient(app, cookies=first.cookies) as client:
        with client.websocket_connect('/api/live/player', headers=ORIGIN) as ws:
            ws.receive_json()
            ws.send_text('{"command":"start"}')
            with pytest.raises(WebSocketDisconnect) as closed:
                while True: ws.receive_json()
            assert closed.value.code == 1008


def test_slow_clients_coalesce_and_connection_caps_are_bounded():
    async def check():
        hub = LiveHub(None)
        queues = [hub.subscribe(('player', n)) for n in range(128)]
        assert all(queues) and hub.subscribe(('player', 129)) is None
        for revision_number in range(1000): hub.broadcast(revision_number)
        assert all(q.qsize() == 1 and q.get_nowait() == 999 for q in queues)
        for queue in queues: hub.unsubscribe(queue)
        assert all(hub.subscribe(('admin', 1)) for _ in range(8))
        assert hub.subscribe(('admin', 1)) is None
    asyncio.run(check())
