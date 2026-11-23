"""Authenticated boot lineage, immutable journal receipts and guarded reconciliation.

Every write is called inside the event -> machine transaction lock in main.py.
Device assertions are evidence, not proof of physical hardware reliability.
"""
from datetime import timedelta
import hmac
import json
import uuid

from fastapi import HTTPException

from .database import execute, one
from .device_commands import CommandAcknowledgement, acknowledge, hold_for_review
from .game import rules_hash, stored_rules, canonical, replay
from .live import record_change
from .security import digest, now


def current_boot(c, machine_id):
    return one(c, 'SELECT * FROM device_boots WHERE active_machine_id=:id', id=machine_id)


def require_boot(c, m, header):
    boot = current_boot(c, m['id'])
    if boot and header != boot['public_id']:
        raise HTTPException(409, 'Register the current boot and send X-Device-Boot-Id.')
    return boot


def register_boot(c, m, body):
    hashed = digest(canonical(body.model_dump()))
    boot = current_boot(c, m['id'])
    existing = one(c, 'SELECT * FROM device_boots WHERE public_id=:id', id=body.bootId)
    if existing:
        if (not boot or existing['id'] != boot['id']
                or not hmac.compare_digest(existing['registration_hash'], hashed)):
            raise HTTPException(409, 'This boot is retired or its registration changed.')
        return {'ok': True, 'bootId': body.bootId}
    if body.previousBootId != (boot['public_id'] if boot else None):
        raise HTTPException(409, 'The previous boot does not match the cabinet lineage.')
    g = one(c, 'SELECT * FROM game_sessions WHERE active_machine_id=:id FOR UPDATE', id=m['id'])
    if g and g['result_source'] != 'device':
        raise HTTPException(409, 'A simulator round owns this cabinet.')
    if boot:
        execute(c, 'UPDATE device_boots SET retired_at=:now WHERE id=:id', now=now(), id=boot['id'])
    execute(c, '''INSERT INTO device_boots(public_id,machine_id,previous_boot_id,storage_id,
      registration_hash,last_uptime_ms) VALUES(:public,:machine,:previous,:storage,:hash,:uptime)''',
      public=body.bootId, machine=m['id'], previous=boot['id'] if boot else None,
      storage=body.storageId, hash=hashed, uptime=body.uptimeMs)
    if g:
        hold_for_review(c, g)
        # A new boot invalidates even an already applied fence from the old boot.
        execute(c, 'UPDATE game_sessions SET revision=revision+1 WHERE id=:id', id=g['id'])
    execute(c, "UPDATE machines SET observed_state='offline',last_seen_at=NULL WHERE id=:id", id=m['id'])
    record_change(c, 'machine.changed')
    return {'ok': True, 'bootId': body.bootId}


def quarantine(c, g, message, boot, body):
    execute(c, '''INSERT INTO device_recovery_conflicts(session_id,boot_id,attempted_event_id,
      sequence_number,phase,payload_hash,reason) VALUES(:session,:boot,:public,:seq,:phase,:hash,:reason)''',
      session=g['id'],boot=boot['id'],public=body.eventId,seq=body.sequence,phase=body.phase,
      hash=digest(canonical(body.model_dump(mode='json'))),reason=message)
    if g['status'] in ('reserved', 'countdown', 'playing', 'awaiting_result', 'review'):
        hold_for_review(c, g)
        execute(c, 'UPDATE game_sessions SET recovery_quarantined=TRUE,revision=revision+1 WHERE id=:id', id=g['id'])
        record_change(c, 'session.changed', g['public_id'])
    # Normal return commits the safety hold; raising would roll it back.
    return {'ok': False, 'detail': message}


def terminal_start(c, boot, command, body):
    accepted = one(c, 'SELECT * FROM device_boots WHERE id=:id', id=command['accepted_boot_id'])
    if (not accepted or body.roundBootId != accepted['public_id']
            or accepted['storage_id'] != boot['storage_id']
            or body.startUptimeMs < command['accepted_uptime_ms']):
        raise HTTPException(409, 'The round start is not bound to the accepted durable journal.')
    if body.roundBootId == boot['public_id']:
        end = body.startUptimeMs + (body.terminal.durationMs if body.terminal else 0)
        if end > body.uptimeMs:
            raise HTTPException(422, 'The round duration exceeds the reported monotonic uptime.')
    elapsed = body.startUptimeMs-command['accepted_uptime_ms']
    if elapsed > 180000:
        raise HTTPException(422, 'The start marker exceeds the three-minute reservation window.')
    return command['acknowledged_at'] + timedelta(milliseconds=elapsed)


def journal(c, m, boot, body, start, finish):
    if not boot:
        raise HTTPException(409, 'Register a boot before submitting journal evidence.')
    hashed = digest(canonical(body.model_dump(mode='json')))
    previous = one(c, '''SELECT * FROM device_journal_events
      WHERE (boot_id=:boot AND sequence_number=:seq) OR public_id=:public''',
      boot=boot['id'], seq=body.sequence, public=body.eventId)
    g = one(c, 'SELECT * FROM game_sessions WHERE public_id=:id AND machine_id=:machine FOR UPDATE',
            id=body.sessionId, machine=m['id'])
    if not g or g['result_source'] != 'device':
        raise HTTPException(409, 'This journal does not belong to a physical-device round.')
    if previous:
        if (previous['boot_id'] == boot['id'] and previous['sequence_number'] == body.sequence
                and previous['public_id'] == body.eventId
                and hmac.compare_digest(previous['payload_hash'], hashed)):
            return json.loads(previous['response_safe'])
        return quarantine(c, g, 'Conflicting journal replay. The round remains held for investigation.', boot, body)
    if body.sequence != boot['last_sequence']+1 or body.uptimeMs < boot['last_uptime_ms']:
        raise HTTPException(409, 'Send the next journal sequence with nondecreasing boot uptime.')
    command = one(c, '''SELECT * FROM device_commands WHERE public_id=:id
      AND session_id=:session AND machine_id=:machine FOR UPDATE''',
      id=body.commandId, session=g['id'], machine=m['id'])
    if not command or command['expected_revision'] != body.expectedRevision:
        raise HTTPException(409, 'The journal command or revision does not match.')
    fence = body.phase.startswith('fenced_')
    if command['command_type'] != ('fence' if fence else 'reserve'):
        raise HTTPException(409, 'The journal phase does not match the command type.')
    if g['recovery_quarantined']:
        raise HTTPException(409, 'Conflicting evidence requires investigation; automatic reconciliation is disabled.')
    result = {'ok': True, 'eventId': body.eventId}
    sealed = one(c, "SELECT id FROM device_journal_events WHERE session_id=:id AND phase LIKE 'fenced_%' LIMIT 1", id=g['id'])
    if not fence and sealed:
        return quarantine(c, g, 'The device reported activity after fencing this session.', boot, body)
    if body.phase == 'reserved':
        result.update(acknowledge(c, m, command['public_id'], CommandAcknowledgement(
            sessionId=body.sessionId, expectedRevision=body.expectedRevision, status='accepted')))
        if not result['ok']:
            result['code'] = 'reservation_expired'
            return result
        if command['accepted_boot_id'] and command['accepted_boot_id'] != boot['id']:
            raise HTTPException(409, 'The reservation was accepted by another boot.')
        if command['accepted_boot_id'] is None:
            execute(c, '''UPDATE device_commands SET accepted_boot_id=:boot,accepted_uptime_ms=:uptime
              WHERE id=:id''', boot=boot['id'], uptime=body.uptimeMs, id=command['id'])
    elif body.phase in ('started', 'terminal'):
        started_at = terminal_start(c, boot, command, body)
        marker = one(c, "SELECT payload FROM device_journal_events WHERE session_id=:id AND phase IN ('started','terminal') ORDER BY id LIMIT 1", id=g['id'])
        if marker:
            original = json.loads(marker['payload'])
            if (original['roundBootId'],original['startUptimeMs']) != (body.roundBootId,body.startUptimeMs):
                return quarantine(c, g, 'The immutable round start marker changed.', boot, body)
        if started_at > g['ready_deadline_at'] or started_at > now()+timedelta(seconds=2):
            raise HTTPException(422, 'The start marker is outside the reservation window.')
        if body.phase == 'started':
            if body.roundBootId != boot['public_id']:
                raise HTTPException(409, 'A retired boot cannot start a round.')
            if g['status'] == 'review' or (g['status'] == 'reserved' and g['ready_deadline_at'] <= now()):
                hold_for_review(c, g)
                return {'ok':False,'code':'start_held','detail':'The round is held. Persist a stop receipt before operator resolution.'}
            result.update(start(c, body.sessionId, 'device'))
            execute(c, 'UPDATE game_sessions SET started_at=:start WHERE id=:id', start=started_at, id=g['id'])
        else:
            payload = body.terminal.model_dump(mode='json')
            _, rules = stored_rules(c, ruleset_id=g['ruleset_id'])
            if payload['rulesHash'] != rules_hash(rules).hex():
                raise HTTPException(422, 'Ruleset mismatch.')
            try:
                replay(payload['placements'], payload['durationMs'], payload['outcome'], rules)
            except (ValueError, KeyError, TypeError):
                raise HTTPException(422, 'The placement trace is invalid.') from None
            if (now()-started_at).total_seconds()*1000+2000 < payload['durationMs']:
                raise HTTPException(422, 'Result timing is not valid.')
            prior = one(c, "SELECT payload FROM device_journal_events WHERE session_id=:id AND phase='terminal' ORDER BY id LIMIT 1", id=g['id'])
            if prior and json.loads(prior['payload'])['terminal'] != payload:
                return quarantine(c, g, 'Conflicting terminal results require investigation.', boot, body)
            if g['status'] in ('playing', 'completed'):
                result.update(finish(c, body.sessionId, body.terminal, 'device'))
            else:
                hold_for_review(c, g)
                result['reviewRequired'] = True
    else:
        if (g['status'] != 'review' or g['revision'] != body.expectedRevision
                or command['target_boot_id'] != boot['id'] or command['expires_at'] <= now()
                or command['status'] != 'pending'):
            raise HTTPException(409, 'This fence is expired, stale or not awaiting a receipt.')
        terminal = one(c, "SELECT id FROM device_journal_events WHERE session_id=:id AND phase='terminal' LIMIT 1", id=g['id'])
        if terminal:
            raise HTTPException(409, 'A recorded terminal result must be reviewed before discarding this round.')
        if body.phase == 'fenced_unstarted':
            accepted = one(c, '''SELECT b.storage_id FROM device_commands d JOIN device_boots b ON b.id=d.accepted_boot_id
              WHERE d.session_id=:id AND d.command_type='reserve' ''', id=g['id'])
            if g['started_at'] or not accepted or accepted['storage_id'] != boot['storage_id']:
                raise HTTPException(409, 'An unstarted fence requires an intact accepted journal and no start marker.')
        execute(c, "UPDATE device_commands SET status='applied',receipt_hash=:hash,acknowledged_at=:now,applied_at=:now WHERE id=:id", hash=hashed, now=now(), id=command['id'])
    execute(c, '''INSERT INTO device_journal_events(public_id,boot_id,sequence_number,uptime_ms,session_id,
      command_id,phase,payload_hash,payload,response_safe)
      VALUES(:public,:boot,:seq,:uptime,:session,:command,:phase,:hash,:payload,:response)''',
      public=body.eventId, boot=boot['id'], seq=body.sequence, uptime=body.uptimeMs,
      session=g['id'], command=command['id'], phase=body.phase, hash=hashed,
      payload=canonical(body.model_dump(mode='json')), response=canonical(result))
    execute(c, '''UPDATE device_boots SET last_sequence=:seq,last_uptime_ms=:uptime,last_seen_at=:now
      WHERE id=:id''', seq=body.sequence, uptime=body.uptimeMs, now=now(), id=boot['id'])
    record_change(c, 'session.changed', body.sessionId)
    return result


def request_fence(c, m, g, body, staff):
    if body.expectedRevision != g['revision'] or g['result_source'] != 'device':
        raise HTTPException(409, 'The round changed. Refresh before requesting a fence.')
    boot = current_boot(c, m['id'])
    if not boot or g['recovery_quarantined']:
        raise HTTPException(409, 'A registered, unquarantined device journal is required.')
    hold_for_review(c, g)
    execute(c, "UPDATE device_commands SET status='expired' WHERE session_id=:id AND command_type='fence' AND status='pending'", id=g['id'])
    execute(c, 'UPDATE game_sessions SET revision=revision+1 WHERE id=:id', id=g['id'])
    revision = one(c, 'SELECT revision FROM game_sessions WHERE id=:id', id=g['id'])['revision']
    public = str(uuid.uuid4())
    execute(c, '''INSERT INTO device_commands(public_id,machine_id,session_id,command_type,
      expected_revision,payload,issued_by,expires_at,target_boot_id)
      VALUES(:public,:machine,:session,'fence',:revision,:payload,:staff,:expires,:boot)''',
      public=public, machine=m['id'], session=g['id'], revision=revision,
      payload=canonical({'sessionId':g['public_id']}), staff=staff,
      expires=now()+timedelta(minutes=3), boot=boot['id'])
    record_change(c, 'session.changed', g['public_id'])
    return {'ok': True, 'commandId': public, 'revision': revision}


def recovery_view(c, m, g):
    boot = current_boot(c, m['id'])
    evidence = one(c, '''SELECT j.*,d.expected_revision,d.target_boot_id,d.status AS command_status
      FROM device_journal_events j JOIN device_commands d ON d.id=j.command_id
      WHERE j.session_id=:id AND j.phase IN ('terminal','fenced_unstarted','fenced_interrupted')
      ORDER BY j.id DESC LIMIT 1''', id=g['id'])
    actions = []
    if g['status'] == 'review' and not g['recovery_quarantined'] and boot and evidence:
        same_boot = evidence['boot_id'] == boot['id']
        if evidence['phase'] == 'terminal':
            lineage = one(c, 'SELECT storage_id FROM device_boots WHERE id=:id', id=evidence['boot_id'])
            if lineage and lineage['storage_id'] == boot['storage_id']:
                actions = ['recover_result']
        elif (same_boot and evidence['target_boot_id'] == boot['id']
              and evidence['expected_revision'] == g['revision'] and evidence['command_status'] == 'applied'):
            actions = ['release_unstarted' if evidence['phase'] == 'fenced_unstarted' else 'void_interrupted']
    return {'bootId':boot['public_id'] if boot else None, 'revision':g['revision'],
            'quarantined':bool(g['recovery_quarantined']), 'allowedActions':actions,
            'evidenceId':evidence['public_id'] if evidence else None,
            'phase':evidence['phase'] if evidence else None,
            'canFence':bool(boot and not g['recovery_quarantined'] and g['status'] in ('reserved','playing','review')
                            and (not evidence or evidence['phase'] != 'terminal'))}


def resolve(c, m, g, body, finish):
    view = recovery_view(c, m, g)
    if (g['revision'] != body.expectedRevision or body.evidenceId != view['evidenceId']
            or body.action not in view['allowedActions']):
        raise HTTPException(409, 'The round or recovery evidence changed. Refresh and inspect it again.')
    evidence = one(c, 'SELECT * FROM device_journal_events WHERE public_id=:id', id=body.evidenceId)
    if body.action == 'recover_result':
        from .device_protocol import JournalEvent
        event = JournalEvent.model_validate(json.loads(evidence['payload']))
        command = one(c, 'SELECT * FROM device_commands WHERE id=:id', id=evidence['command_id'])
        boot = current_boot(c, m['id'])
        started_at = terminal_start(c, boot, command, event)
        execute(c, "UPDATE game_sessions SET status='playing',started_at=:start WHERE id=:id", start=started_at, id=g['id'])
        result = finish(c, g['public_id'], event.terminal, 'device')
    else:
        execute(c, '''UPDATE game_sessions SET status=:status,end_reason=:reason,
          completed_at=:now,revision=revision+1 WHERE id=:id''',
          status='expired' if body.action == 'release_unstarted' else 'aborted',
          reason='no_show' if body.action == 'release_unstarted' else 'operator_abort', now=now(), id=g['id'])
        execute(c, "UPDATE queue_entries SET status='expired',closed_at=:now,revision=revision+1 WHERE id=:id", now=now(), id=g['queue_entry_id'])
        result = {'ok': True}
    execute(c, "UPDATE device_commands SET status='expired' WHERE session_id=:id AND status IN ('pending','accepted')", id=g['id'])
    execute(c, "UPDATE machines SET observed_state='offline',last_seen_at=NULL WHERE id=:id", id=m['id'])
    record_change(c, 'session.changed', g['public_id'])
    return result
