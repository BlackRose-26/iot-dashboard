# Database backups and restore

Added 24 November 2026. Tool: `scripts/db-backup.py`. Tests: `backend/tests/test_db_backup.py`.

## What runs automatically

`npm run online` (and `online:device`) takes an encrypted backup when it starts, then every 15 minutes, and once more when you press Ctrl+C. Change the interval with `STACK_BACKUP_MINUTES` (0 turns automatic backups off). A failed backup prints a message but never stops the dashboard. `npm run dev` does not back up; it is for development data.

## Commands

| Command | What it does |
|---|---|
| `npm run db:backup` | Manual backup (labelled `manual`, never pruned) |
| `npm run db:verify` | Restores the newest backup into a throwaway database, compares every table's row count with its manifest, then drops it. Run this at least once before the event. |
| `backend\.venv\Scripts\python.exe scripts\db-backup.py --verify FILE` | Same check for a specific backup |
| `backend\.venv\Scripts\python.exe scripts\db-backup.py --restore FILE --replace-live` | **Disaster recovery.** Replaces all current data. Refuses while the API is running on port 8000, and takes a `prerestore` safety backup first. |

## Where and how backups are stored

- **Folder:** `%USERPROFILE%\StackMokoBaby-backups`, or `STACK_BACKUP_DIR`. The tool refuses any folder inside the project, so backups cannot reach Git or the knowledge graph.
- **File:** `stack-moko-YYYYMMDD-HHMMSS[-label].sql.gz.enc`. This is a compressed `mysqldump` of `stack_moko_baby`, encrypted with Fernet (AES + HMAC) using `STACK_BACKUP_KEY` from `backend/.env`. The key is created on the first backup and never printed.
- **Manifest:** a `.json` beside each backup with the time, table count, per-table row counts, applied migrations and the encrypted file's SHA-256. It holds no personal data. A changed or damaged backup is refused.
- **Retention:** the newest 30 automatic backups are kept (`STACK_BACKUP_KEEP`). Labelled backups (`manual`, `shutdown`, `prerestore`) are never pruned automatically.
- **Account:** the dump uses the least-privileged app account (SELECT is enough; the schema has only tables). Verify and restore use XAMPP's `root` (`STACK_DB_ROOT_PASSWORD` if it has one). Passwords go through `MYSQL_PWD`, never the command line.

## Keys and privacy

A backup contains nicknames, scores, queue history, **encrypted** student IDs and their HMAC lookup values. Treat it as private event data.

- Opening a backup needs `STACK_BACKUP_KEY`. Decrypting student IDs after a restore also needs the original `STACK_IDENTITY_KEY` and `STACK_LOOKUP_KEY`. All three live in `backend/.env`.
- **Keep one copy of `backend/.env` somewhere safe and separate from the backups**, for example a USB drive kept apart from the laptop. Without it, a backup cannot be opened, and a restored database cannot match returning players.
- After the event, delete backups under the retention policy in [schema.md §6](schema.md). Restore copies count as copies of personal data.

## Verification record (24 November 2026)

- A backup of the real local database (27 tables, 238 rows, 24 KB encrypted) restored into a throwaway database with all row counts matching. The throwaway database was dropped.
- `test_db_backup.py` (4 passed) uses a generated database through root. It checks:
  - the encrypted backup does not contain plain names;
  - verify passes;
  - after a simulated data loss, the live-restore path restores the data and leaves a `prerestore` safety backup;
  - a tampered file is refused;
  - pruning keeps labelled backups;
  - a folder inside the project is refused.
- Not yet exercised: a real live restore of `stack_moko_baby`, a restore on a different PC, or launcher-driven periodic backups across a full event.
