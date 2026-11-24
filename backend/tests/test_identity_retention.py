"""Student-ID purge (24 Nov 2026), against a disposable XAMPP database."""
import importlib.util
import re
from datetime import timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from app.identity_retention import purge, summary
from app.security import now
from test_player_flow import environment, entry_payload, join  # noqa: F401

ROOT = Path(__file__).resolve().parents[2]


def load_script():
    spec = importlib.util.spec_from_file_location('purge_ids', ROOT/'scripts'/'purge-student-ids.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_purge_removes_only_due_ids_then_all_keeping_players_and_tickets(environment):
    app, admin, token, engine, settings = environment
    first, second = join(app, token, 1), join(app, token, 2)
    with engine.begin() as c:
        c.exec_driver_sql("UPDATE student_identities s JOIN players p ON p.id=s.player_id "
                          "SET s.purge_after=NOW(3) - INTERVAL 1 DAY WHERE p.nickname='Test 1'")
    with engine.connect() as c:
        assert summary(c, now()) | {'nextDue': None} == {'total': 2, 'due': 1, 'nextDue': None}

    assert purge(engine, now()) == 1
    with engine.connect() as c:
        left = c.exec_driver_sql('SELECT p.nickname FROM student_identities s JOIN players p ON p.id=s.player_id').all()
        players = c.exec_driver_sql('SELECT COUNT(*) FROM players').scalar()
    assert [r[0] for r in left] == ['Test 2'] and players == 2
    assert first.get('/api/player/context').json()['ticket']['nickname'] == 'Test 1', 'the ticket survives'

    assert purge(engine, now(), everything=True) == 1
    with engine.connect() as c:
        assert summary(c, now())['total'] == 0
        audits = c.exec_driver_sql("SELECT reason,details_safe FROM audit_logs WHERE action='identity_purge' ORDER BY id").all()
    assert len(audits) == 2 and '"removed": 1' in audits[0][1] and '"scope": "all"' in audits[1][1]
    assert all('DUMMY' not in (r[0] or '') + r[1] for r in audits), 'no student ID in the audit log'
    assert second.get('/api/player/context').json()['ticket']['status'] == 'waiting'

    # Without the lookup the same student ID is no longer recognised (why --all waits until after the event).
    second.post('/api/player/cancel')
    again = TestClient(app)
    assert again.post('/api/player/entry', json=entry_payload(token)).status_code == 200
    again.headers['X-CSRF-Token'] = again.get('/api/player/context').json()['csrf']
    response = again.post('/api/player/register', json={'nickname': 'Test 1 again', 'studentId': 'DUMMY-TEST-1', 'acknowledged': True})
    assert response.status_code == 200, response.text


def test_purge_with_nothing_due_changes_nothing(environment):
    app, admin, token, engine, settings = environment
    join(app, token, 3)
    assert purge(engine, now() - timedelta(days=1)) == 0
    with engine.connect() as c:
        assert summary(c, now())['total'] == 1


def test_older_backup_selection_only_picks_earlier_backups(tmp_path):
    script = load_script()
    pattern = re.compile(r'stack-moko-\d{8}-\d{6}(?:-[a-z]+)?\.sql\.gz\.enc$')
    names = ['stack-moko-20261124-100000.sql.gz.enc', 'stack-moko-20261124-110000-manual.sql.gz.enc',
             'stack-moko-20261124-120000-purged.sql.gz.enc', 'stack-moko-20261124-130000.sql.gz.enc', 'notes.txt']
    for name in names:
        (tmp_path/name).write_text('x')
    newest = tmp_path/names[2]
    assert [p.name for p in script.older_backups(tmp_path, newest, pattern)] == names[:2]


def test_dry_run_is_the_default(monkeypatch, capsys, environment):
    app, admin, token, engine, settings = environment
    join(app, token, 4)
    script = load_script()
    import app.config as config
    monkeypatch.setattr(config.Settings, 'load', classmethod(lambda cls: settings))
    assert script.main(['--all']) == 0
    assert 'Dry run: 1 would be deleted (every stored ID).' in capsys.readouterr().out
    with engine.connect() as c:
        assert summary(c, now())['total'] == 1
