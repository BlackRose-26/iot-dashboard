"""Encrypted backups of the Stack Moko Baby database, with a verified restore.

  backup                      dump -> gzip -> encrypt, plus a manifest of row counts (default)
  --verify [FILE]             restore a backup into a throwaway database and compare row counts
  --restore FILE --replace-live
                              disaster recovery: replace stack_moko_baby (API must be stopped;
                              a safety backup of the current data is taken first)

Backups go OUTSIDE the project (default: %USERPROFILE%\\StackMokoBaby-backups, or
STACK_BACKUP_DIR) so they never reach Git or the knowledge graph. Each file is encrypted
with STACK_BACKUP_KEY from backend/.env (generated on first use, never printed). The dump
holds nicknames, scores, encrypted student IDs and HMAC lookups; decrypting student IDs
after a restore still needs the same backend/.env identity keys. Keep a copy of
backend/.env somewhere safe and separate from the backups.

The dump uses the least-privileged app account (SELECT only is needed). Verify/restore use
XAMPP's root account (STACK_DB_ROOT_PASSWORD if set). Passwords go through MYSQL_PWD,
never the command line.
"""
import argparse
import base64
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import secrets
import socket
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT/'backend'/'.env'
DATABASE = 'stack_moko_baby'
NAME = re.compile(r'stack-moko-\d{8}-\d{6}(?:-[a-z]+)?\.sql\.gz\.enc$')
AUTOMATIC = re.compile(r'stack-moko-\d{8}-\d{6}\.sql\.gz\.enc$')
HIDDEN = {'creationflags': 0x08000000} if os.name == 'nt' else {}


def env_values():
    from dotenv import dotenv_values
    return dotenv_values(ENV)


def backup_key():
    """Fernet key from backend/.env; created once (never printed) if missing."""
    from cryptography.fernet import Fernet
    value = env_values().get('STACK_BACKUP_KEY')
    if not value:
        value = Fernet.generate_key().decode()
        with ENV.open('a', encoding='utf-8') as stream:
            stream.write(f'\n# Encrypts database backups (scripts/db-backup.py). Keep a copy of this file safe.\nSTACK_BACKUP_KEY={value}\n')
        print('Created STACK_BACKUP_KEY in backend/.env (not printed). Keep a copy of backend/.env somewhere safe.')
    return Fernet(value.encode())


def backup_dir():
    folder = Path(os.getenv('STACK_BACKUP_DIR') or Path.home()/'StackMokoBaby-backups').resolve()
    if folder == ROOT or ROOT in folder.parents:
        raise SystemExit('Choose a backup folder outside the project (STACK_BACKUP_DIR); backups must never reach Git.')
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def tool(name):
    folder = Path(os.getenv('STACK_MYSQL_BIN', 'C:/xampp/mysql/bin'))
    path = folder/(name + ('.exe' if os.name == 'nt' else ''))
    if not path.is_file(): raise SystemExit(f'{path} not found. Set STACK_MYSQL_BIN to the MariaDB/XAMPP bin folder.')
    return str(path)


def app_login():
    url = urlsplit(env_values().get('STACK_DATABASE_URL') or '')
    if not url.username: raise SystemExit('Run backend/setup_local.py first; no database login in backend/.env.')
    return url.hostname or '127.0.0.1', str(url.port or 3306), unquote(url.username), unquote(url.password or '')


def root_login():
    return '127.0.0.1', '3306', 'root', os.getenv('STACK_DB_ROOT_PASSWORD', '')


def client_args(login): return ['--no-defaults', '-h', login[0], '-P', login[1], '-u', login[2]]
def client_env(login): return dict(os.environ, MYSQL_PWD=login[3])


def query(login, database, sql):
    result = subprocess.run([tool('mysql'), *client_args(login), '--batch', '--skip-column-names', *([database] if database else []), '-e', sql],
                            env=client_env(login), capture_output=True, text=True, **HIDDEN)
    if result.returncode: raise SystemExit('Database query failed: ' + result.stderr.strip().splitlines()[-1])
    return [line.split('\t') for line in result.stdout.splitlines()]


def row_counts(login, database):
    tables = [row[0] for row in query(login, database, 'SHOW TABLES')]
    return {table: int(query(login, database, f'SELECT COUNT(*) FROM `{table}`')[0][0]) for table in sorted(tables)}


def take_backup(label=None, keep=30, database=DATABASE, login=None, folder=None):
    login = login or app_login()
    fernet = backup_key()
    stamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    folder = folder or backup_dir()
    target = folder/f'stack-moko-{stamp}{"-" + label if label else ""}.sql.gz.enc'
    dump = subprocess.run([tool('mysqldump'), *client_args(login), '--single-transaction', '--skip-lock-tables',
                           '--no-tablespaces', '--hex-blob', '--skip-comments', '--default-character-set=utf8mb4', database],
                          env=client_env(login), capture_output=True, **HIDDEN)
    if dump.returncode or not dump.stdout.strip():
        raise SystemExit('Backup failed: ' + dump.stderr.decode(errors='replace').strip()[-300:])
    counts = row_counts(login, database)
    migrations = [row[0] for row in query(login, database, 'SELECT version FROM schema_migrations ORDER BY version')]
    token = fernet.encrypt(gzip.compress(dump.stdout, compresslevel=6))
    partial = target.with_suffix('.partial')
    partial.write_bytes(token)
    partial.replace(target)  # never leave a half-written backup with the final name
    manifest = {'file': target.name, 'created_at': dt.datetime.now().astimezone().isoformat(timespec='seconds'),
                'host': socket.gethostname(), 'database': database, 'encrypted_sha256': hashlib.sha256(token).hexdigest(),
                'dump_bytes': len(dump.stdout), 'tables': len(counts), 'row_counts': counts, 'migrations': migrations,
                'note': 'Row counts only; no personal data. Restoring student IDs needs the same backend/.env keys.'}
    target.with_name(target.name + '.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    removed = prune(folder, keep)
    print(f'Backup saved: {target} ({len(token)//1024} KB, {len(counts)} tables, {sum(counts.values())} rows)'
          + (f'; removed {removed} older backup(s)' if removed else ''))
    return target


def prune(folder, keep):
    """Keep the newest automatic backups; labelled ones (pre-restore, manual) are never pruned."""
    automatic = sorted(p for p in folder.iterdir() if AUTOMATIC.fullmatch(p.name))
    old = automatic[:-keep] if keep > 0 else []
    for path in old:
        path.unlink(); path.with_name(path.name + '.json').unlink(missing_ok=True)
    return len(old)


def read_backup(path):
    path = Path(path)
    manifest = json.loads(path.with_name(path.name + '.json').read_text(encoding='utf-8'))
    token = path.read_bytes()
    if hashlib.sha256(token).hexdigest() != manifest['encrypted_sha256']:
        raise SystemExit('Backup file does not match its manifest (damaged or replaced).')
    return gzip.decompress(backup_key().decrypt(token)), manifest


def load_into(login, database, sql):
    result = subprocess.run([tool('mysql'), *client_args(login), '--default-character-set=utf8mb4', database],
                            input=sql, env=client_env(login), capture_output=True, **HIDDEN)
    if result.returncode: raise SystemExit('Restore failed: ' + result.stderr.decode(errors='replace').strip()[-300:])


def latest():
    files = sorted(p for p in backup_dir().iterdir() if NAME.fullmatch(p.name))
    if not files: raise SystemExit('No backups yet. Run: npm run db:backup')
    return max(files, key=lambda p: p.stat().st_mtime)


def verify(path):
    sql, manifest = read_backup(path)
    login = root_login()
    scratch = 'stack_moko_restore_check_' + secrets.token_hex(4)
    query(login, '', f'CREATE DATABASE `{scratch}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    try:
        load_into(login, scratch, sql)
        counts = row_counts(login, scratch)
    finally:
        query(login, '', f'DROP DATABASE IF EXISTS `{scratch}`')
    if counts != manifest['row_counts']:
        changed = sorted(t for t in set(counts) | set(manifest['row_counts']) if counts.get(t) != manifest['row_counts'].get(t))
        raise SystemExit('Restore check FAILED; row counts differ in: ' + ', '.join(changed))
    print(f'Restore check passed: {Path(path).name} restored into a throwaway database; '
          f'{len(counts)} tables and {sum(counts.values())} rows match. Throwaway database removed.')


def api_running():
    with socket.socket() as probe:
        probe.settimeout(1)
        return probe.connect_ex(('127.0.0.1', 8000)) == 0


def restore_live(path, database=DATABASE, login=None, folder=None, check_api=True):
    if check_api and api_running(): raise SystemExit('Stop the dashboard/API first (port 8000 is in use), then run the restore again.')
    sql, manifest = read_backup(path)
    print('Taking a safety backup of the current database first...')
    take_backup(label='prerestore', keep=0, database=database, login=login, folder=folder)
    login = root_login()
    query(login, '', f'DROP DATABASE IF EXISTS `{database}`')
    query(login, '', f'CREATE DATABASE `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    load_into(login, database, sql)
    if row_counts(login, database) != manifest['row_counts']:
        raise SystemExit('Restored, but row counts differ from the manifest. Keep the pre-restore backup and investigate.')
    print(f'Restored {Path(path).name} into {database}. The app account keeps its grants (they are not tied to the database). '
          'Start the dashboard again; the previous data is in the "prerestore" backup.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--verify', nargs='?', const='latest', metavar='FILE')
    parser.add_argument('--restore', metavar='FILE')
    parser.add_argument('--replace-live', action='store_true')
    parser.add_argument('--label', choices=['manual', 'shutdown'], help='Labelled backups are never pruned automatically.')
    parser.add_argument('--keep', type=int, default=int(os.getenv('STACK_BACKUP_KEEP', '30')))
    args = parser.parse_args()
    if args.restore:
        if not args.replace_live: raise SystemExit('Restoring replaces ALL current data. Add --replace-live to confirm.')
        restore_live(args.restore)
    elif args.verify:
        verify(latest() if args.verify == 'latest' else args.verify)
    else:
        take_backup(args.label, args.keep)


if __name__ == '__main__':
    try: main()
    except subprocess.SubprocessError as error: sys.exit(f'Database tool failed: {error}')
