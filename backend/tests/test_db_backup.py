"""Database backup tool: backup, tamper check, verify, live-restore path and pruning.

Runs only against a generated throwaway database through XAMPP's root account; the real
stack_moko_baby database and the real backup folder are never touched.
"""
import importlib.util
import secrets
from pathlib import Path

import pytest
from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('db_backup', ROOT/'scripts'/'db-backup.py')
backup = importlib.util.module_from_spec(spec); spec.loader.exec_module(backup)


@pytest.fixture
def scratch(tmp_path, monkeypatch):
    try: backup.tool("mysql")
    except SystemExit: pytest.skip('XAMPP MariaDB client tools are not installed')
    login = backup.root_login()
    try: backup.query(login, '', 'SELECT 1')
    except SystemExit: pytest.skip('MariaDB is not running')
    key = Fernet(Fernet.generate_key())
    monkeypatch.setattr(backup, 'backup_key', lambda: key)  # never writes backend/.env
    name = 'stack_moko_backup_test_' + secrets.token_hex(4)
    backup.query(login, '', f'CREATE DATABASE `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    backup.query(login, name, 'CREATE TABLE schema_migrations (version VARCHAR(80) PRIMARY KEY)')
    backup.query(login, name, "INSERT INTO schema_migrations VALUES ('001_initial.sql')")
    backup.query(login, name, 'CREATE TABLE results (id INT PRIMARY KEY, nickname VARCHAR(40), score INT)')
    backup.query(login, name, "INSERT INTO results VALUES (1,'Synthetic Ana',15),(2,'Synthetic Ben',7)")
    yield login, name, tmp_path
    backup.query(login, '', f'DROP DATABASE IF EXISTS `{name}`')


def test_backup_is_encrypted_verified_and_restores_after_data_loss(scratch):
    login, name, folder = scratch
    path = backup.take_backup(database=name, login=login, folder=folder)
    assert backup.NAME.fullmatch(path.name) and b'Synthetic Ana' not in path.read_bytes()
    sql, manifest = backup.read_backup(path)
    assert manifest['row_counts'] == {'results': 2, 'schema_migrations': 1} and b'Synthetic Ana' in sql
    backup.verify(path)
    backup.query(login, name, 'DELETE FROM results')  # simulated data loss
    backup.restore_live(path, database=name, login=login, folder=folder, check_api=False)
    assert backup.row_counts(login, name) == {'results': 2, 'schema_migrations': 1}
    assert any('prerestore' in p.name for p in folder.iterdir()), 'a safety backup precedes every live restore'


def test_tampered_backup_is_refused(scratch):
    login, name, folder = scratch
    path = backup.take_backup(database=name, login=login, folder=folder)
    data = bytearray(path.read_bytes()); data[-5] ^= 1; path.write_bytes(bytes(data))
    with pytest.raises(SystemExit, match='does not match its manifest'):
        backup.read_backup(path)


def test_pruning_keeps_newest_and_never_labelled_backups(tmp_path):
    for stamp in ('20261101-000000', '20261102-000000', '20261103-000000'):
        for suffix in ('.sql.gz.enc', '.sql.gz.enc.json'):
            (tmp_path/f'stack-moko-{stamp}{suffix}').write_text('x')
    (tmp_path/'stack-moko-20261101-000000-prerestore.sql.gz.enc').write_text('x')
    (tmp_path/'unrelated.sql').write_text('x')
    assert backup.prune(tmp_path, keep=2) == 1
    names = {p.name for p in tmp_path.iterdir()}
    assert 'stack-moko-20261101-000000.sql.gz.enc' not in names and 'stack-moko-20261101-000000.sql.gz.enc.json' not in names
    assert {'stack-moko-20261103-000000.sql.gz.enc', 'stack-moko-20261101-000000-prerestore.sql.gz.enc', 'unrelated.sql'} <= names


def test_backup_folder_inside_the_project_is_refused(monkeypatch):
    monkeypatch.setenv('STACK_BACKUP_DIR', str(ROOT/'backups'))
    with pytest.raises(SystemExit, match='outside the project'):
        backup.backup_dir()
    assert not (ROOT/'backups').exists()
