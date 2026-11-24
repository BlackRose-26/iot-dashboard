"""Student-ID retention: delete encrypted student IDs and their keyed lookups.

Each player has at most one row in student_identities holding both the encrypted ID and
the HMAC lookup used to refuse duplicate registrations. Deleting that row removes both;
nicknames, tickets, scores and the leaderboard stay. After a purge the same student could
register again, so purge everything only after the event is over.
"""
import json
import uuid

from .database import all_rows, execute, one


def summary(c, at):
    row = one(c, '''SELECT COUNT(*) AS total, COALESCE(SUM(purge_after<=:at),0) AS due,
      MIN(CASE WHEN purge_after>:at THEN purge_after END) AS next_due FROM student_identities''', at=at)
    return {'total': int(row['total']), 'due': int(row['due']), 'nextDue': row['next_due']}


def purge(engine, at, everything=False, reason=None):
    """Delete due identities (or all with everything=True); return how many were removed.

    One audited transaction. The audit row holds counts only, never an ID or lookup.
    """
    condition = '' if everything else ' WHERE purge_after<=:at'
    with engine.begin() as c:
        rows = all_rows(c, 'SELECT player_id FROM student_identities' + condition + ' FOR UPDATE', at=at)
        if rows:
            execute(c, 'DELETE FROM student_identities' + condition, at=at)
        remaining = one(c, 'SELECT COUNT(*) AS n FROM student_identities')['n']
        execute(c, '''INSERT INTO audit_logs(event_id,staff_user_id,action,entity_type,entity_public_id,reason,details_safe,request_id)
          VALUES(1,NULL,'identity_purge','identity',NULL,:reason,:details,:request)''',
                reason=(reason or ('all identities after the event' if everything else 'retention date reached'))[:300],
                details=json.dumps({'removed': len(rows), 'remaining': int(remaining), 'scope': 'all' if everything else 'due'}),
                request=str(uuid.uuid4()))
    return len(rows)
