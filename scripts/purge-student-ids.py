"""Delete stored student IDs once they are no longer needed (privacy retention).

  npm run db:purge-ids                         dry run: how many IDs are stored and due (default)
  npm run db:purge-ids -- --apply              delete IDs whose retention date has passed
  npm run db:purge-ids -- --all --apply        after the event: delete EVERY stored student ID now
  ... --delete-older-backups                   also delete backups taken before the purge

Each player's encrypted student ID and its keyed lookup are deleted together. Nicknames,
tickets, scores and the leaderboard stay. Once an ID is deleted the same student could
register again, so use --all only after the event is over.

After a real purge a fresh encrypted backup (label "purged") is taken. Older backups still
contain the deleted IDs; --delete-older-backups removes them, but only after the new backup
has been written. Nothing is printed that identifies a student.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'backend'))


def backup_module():
    spec = importlib.util.spec_from_file_location('db_backup', ROOT/'scripts'/'db-backup.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def older_backups(folder, newest, pattern):
    """Backups (and their manifests) created before `newest`; they may hold purged IDs."""
    return sorted(p for p in folder.iterdir() if pattern.fullmatch(p.name) and p.name < newest.name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--apply', action='store_true', help='Actually delete. Without it nothing changes.')
    parser.add_argument('--all', action='store_true', help='Delete every stored student ID, not only those past their date.')
    parser.add_argument('--delete-older-backups', action='store_true',
                        help='After the post-purge backup, delete older backups that still contain IDs.')
    args = parser.parse_args(argv)

    from app.config import Settings
    from app.database import make_engine
    from app.identity_retention import purge, summary
    from app.security import now

    engine = make_engine(Settings.load().database_url)
    at = now()
    with engine.connect() as c:
        before = summary(c, at)
    scope = before['total'] if args.all else before['due']
    print(f"Stored student IDs: {before['total']}. Past their retention date: {before['due']}."
          + (f" Next retention date: {before['nextDue']:%Y-%m-%d}." if before['nextDue'] else ''))
    if not args.apply:
        print(f"Dry run: {scope} would be deleted"
              + (' (every stored ID).' if args.all else '. Add --all after the event to delete every ID.')
              + ' Add --apply to delete.')
        return 0
    if not scope:
        print('Nothing to delete.')
        return 0
    removed = purge(engine, at, everything=args.all)
    print(f'Deleted {removed} student ID(s) and their lookups. Nicknames and scores are unchanged.')

    backups = backup_module()
    fresh = backups.take_backup(label='purged')
    old = older_backups(fresh.parent, fresh, backups.NAME)
    if args.delete_older_backups:
        for path in old:
            path.unlink()
            path.with_name(path.name + '.json').unlink(missing_ok=True)
        print(f'Deleted {len(old)} older backup(s) that still contained the purged IDs.')
    elif old:
        print(f'{len(old)} older backup(s) in {fresh.parent} still contain the deleted IDs. '
              'Delete them with --delete-older-backups once you no longer need them.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
