"""Device command delivery and durable receipts. No browser or AI control path."""
import hmac
import json
from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator

from .database import all_rows, one, execute
from .game import canonical
from .live import record_change
from .security import digest, now

UUID_PATTERN = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'


class CommandAcknowledgement(BaseModel):
    model_config = {'extra': 'forbid'}
    sessionId: str = Field(pattern=UUID_PATTERN)
    expectedRevision: int = Field(strict=True, ge=1)
    status: Literal['accepted', 'rejected']
    rejectionCode: Literal['not_ready', 'busy', 'rules_mismatch', 'storage_failed'] | None = None

    @model_validator(mode='after')
    def rejection_matches_status(self):
        if (self.status == 'rejected') != (self.rejectionCode is not None):
            raise ValueError('Rejection requires one supported reason code.')
        return self


def requires_review(g):
    return bool(g and g['result_source'] == 'device' and (
        g['status'] == 'review' or
        (g['status'] == 'reserved' and g['ready_deadline_at'] <= now())))


def hold_for_review(c, g):
    """Retain the active-machine and assigned-ticket locks; never expire a round blindly."""
    if g['status'] == 'review':
        return False
    if g['status'] not in ('reserved', 'countdown', 'playing', 'awaiting_result'):
        raise HTTPException(409, 'This round is already resolved.')
    execute(c, "UPDATE game_sessions SET status='review',revision=revision+1 WHERE id=:id", id=g['id'])
    execute(c, "UPDATE device_commands SET status='expired' WHERE session_id=:id AND status IN ('pending','accepted')", id=g['id'])
    record_change(c, 'session.changed', g['public_id'])
    return True


def poll_commands(c, m):
    g = one(c, 'SELECT * FROM game_sessions WHERE active_machine_id=:id', id=m['id'])
    review = requires_review(g)
    commands = []
    if m['enabled'] and not m['maintenance'] and not review:
        rows = all_rows(c, '''SELECT d.*,g.public_id AS session_uuid FROM device_commands d
          JOIN game_sessions g ON g.id=d.session_id AND g.machine_id=d.machine_id
          WHERE d.machine_id=:machine AND d.command_type='reserve'
          AND d.status IN ('pending','accepted') AND d.expires_at>:now
          AND g.status='reserved' AND g.result_source='device'
          AND d.expected_revision=g.revision ORDER BY d.created_at,d.id LIMIT 5''', machine=m['id'], now=now())
        for row in rows:
            payload = json.loads(row['payload'])
            commands.append({'id':row['public_id'], 'type':'reserve', 'deliverySequence':row['id'],
                'sessionId':row['session_uuid'], 'expectedRevision':row['expected_revision'],
                'expiresAt':row['expires_at'].isoformat()+'Z',
                'rules':payload['rules'], 'rulesHash':payload['rulesHash']})
    if g and g['result_source']=='device' and g['status']=='review':
        fences = all_rows(c, '''SELECT d.*,b.public_id AS boot_uuid FROM device_commands d
          JOIN device_boots b ON b.id=d.target_boot_id AND b.retired_at IS NULL
          WHERE d.session_id=:id AND d.command_type='fence' AND d.status='pending'
          AND d.expected_revision=:revision AND d.expires_at>:now ORDER BY d.id''',
          id=g['id'],revision=g['revision'],now=now())
        commands.extend({'id':d['public_id'],'type':'fence','deliverySequence':d['id'],'sessionId':g['public_id'],
                         'expectedRevision':d['expected_revision'],'bootId':d['boot_uuid'],
                         'expiresAt':d['expires_at'].isoformat()+'Z'} for d in fences)
    return {'commands':commands, 'reviewRequired':review,
            'activeSessionId':g['public_id'] if g and g['result_source']=='device' else None}


def acknowledge(c, m, public, body):
    command = one(c, '''SELECT * FROM device_commands
      WHERE public_id=:id AND machine_id=:machine FOR UPDATE''', id=public, machine=m['id'])
    if not command:
        raise HTTPException(404, 'This command is not available to this device.')
    hashed = digest(canonical(body.model_dump()))
    if command['receipt_hash'] is not None:
        if not hmac.compare_digest(command['receipt_hash'], hashed):
            raise HTTPException(409, 'A different receipt was already recorded for this command.')
        return {'ok':True, 'commandId':public, 'status':body.status}
    g = one(c, 'SELECT * FROM game_sessions WHERE id=:id AND machine_id=:machine FOR UPDATE',
            id=command['session_id'], machine=m['id'])
    if (not g or g['result_source'] != 'device' or command['command_type'] != 'reserve'
            or body.sessionId != g['public_id'] or body.expectedRevision != command['expected_revision']
            or body.expectedRevision != g['revision']):
        raise HTTPException(409, 'The command, round or revision does not match.')
    if g['status'] == 'reserved' and (command['expires_at'] <= now() or g['ready_deadline_at'] <= now()):
        hold_for_review(c, g)
        # Return normally so the caller can commit the conservative review hold.
        return {'ok':False, 'detail':'The reservation expired. Operator review is required.'}
    if command['status'] != 'pending' or g['status'] != 'reserved':
        raise HTTPException(409, 'This command is no longer awaiting a receipt.')
    if body.status == 'accepted' and (not m['enabled'] or m['maintenance']):
        raise HTTPException(409, 'This cabinet is unavailable for a new command.')
    execute(c, '''UPDATE device_commands SET status=:status,receipt_hash=:hash,
      rejection_code=:reason,acknowledged_at=:now WHERE id=:id''',
      status=body.status, hash=hashed, reason=body.rejectionCode, now=now(), id=command['id'])
    if body.status == 'rejected':
        hold_for_review(c, g)
    else:
        record_change(c, 'command.changed', g['public_id'])
    return {'ok':True, 'commandId':public, 'status':body.status}
