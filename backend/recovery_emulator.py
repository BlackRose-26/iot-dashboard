"""Explicit, filesystem-journaled protocol-v2 emulator; never runs a physical game.

Use a separate journal from device_emulator.py. Stop markers are retained forever.
The filesystem exercise does not validate ESP32 NVS or power-loss behavior.
"""
import argparse
import json
import os
from pathlib import Path
import time
from typing import Literal
import uuid

import httpx
from pydantic import Field, model_validator

from app.device_commands import UUID_PATTERN
from app.device_protocol import APIInput, BootRegistration, JournalEvent, Result


class SavedRound(APIInput):
    commandId: str = Field(pattern=UUID_PATTERN)
    sessionId: str = Field(pattern=UUID_PATTERN)
    expectedRevision: int = Field(strict=True, ge=1)
    accepted: bool = Field(strict=True, default=False)
    fenced: bool = Field(strict=True, default=False)
    roundBootId: str | None = Field(default=None, pattern=UUID_PATTERN)
    startUptimeMs: int | None = Field(default=None, strict=True, ge=0)
    terminal: Result | None = None

    @model_validator(mode='after')
    def intact_start(self):
        if (self.roundBootId is None) != (self.startUptimeMs is None):
            raise ValueError('Incomplete saved start marker.')
        if self.terminal and self.startUptimeMs is None:
            raise ValueError('A saved terminal result requires a start marker.')
        return self


class SavedJournal(APIInput):
    version: Literal[2] = 2
    registration: BootRegistration
    registered: bool = Field(strict=True, default=False)
    sequence: int = Field(strict=True, ge=0, default=0)
    lastUptimeMs: int = Field(strict=True, ge=0, default=0)
    rounds: dict[str, SavedRound] = Field(default_factory=dict)
    pending: JournalEvent | None = None
    rejected: list[JournalEvent] = Field(default_factory=list)

    @model_validator(mode='after')
    def intact_pending(self):
        if self.pending and self.pending.sequence != self.sequence+1:
            raise ValueError('Pending packet does not follow the saved sequence.')
        if any(key != item.sessionId for key,item in self.rounds.items()):
            raise ValueError('Saved round key does not match its session.')
        if self.pending:
            saved = self.rounds.get(self.pending.sessionId)
            if not saved or (not self.pending.phase.startswith('fenced_') and (
                    self.pending.commandId != saved.commandId
                    or self.pending.expectedRevision != saved.expectedRevision)):
                raise ValueError('Pending packet is not bound to a saved round.')
        return self


class RecoveryEmulator:
    def __init__(self, client, journal, clock=None):
        self.client = client
        self.path = Path(journal)
        self.started = time.monotonic()
        self.clock = clock
        if self.path.exists():
            # A corrupt journal is preserved and fails before any network request.
            self.saved = SavedJournal.model_validate_json(self.path.read_text(encoding='utf-8'))
        else:
            self.saved = SavedJournal(registration=BootRegistration(
                bootId=str(uuid.uuid4()), storageId=str(uuid.uuid4()), uptimeMs=0))
            self.persist()
        self.base_uptime = self.saved.lastUptimeMs
        self.client.headers['X-Device-Boot-Id'] = self.saved.registration.bootId

    def uptime(self):
        return max(self.saved.lastUptimeMs, self.clock() if self.clock else
                   self.base_uptime+int((time.monotonic()-self.started)*1000))

    def persist(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix+'.tmp')
        with temporary.open('w', encoding='utf-8') as output:
            output.write(self.saved.model_dump_json())
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, self.path)

    def connect(self):
        if not self.saved.registered:
            response = self.client.post('/api/device/boot', json=self.saved.registration.model_dump())
            response.raise_for_status()
            self.saved.registered = True
            self.persist()
        return self.flush()

    def flush(self):
        if not self.saved.pending:
            return None
        packet = self.saved.pending
        response = self.client.post('/api/device/journal',json=packet.model_dump(mode='json'))
        if response.status_code == 409 and response.json().get('code') in ('reservation_expired','start_held'):
            # The server definitively rejected this uncommitted sequence. Preserve
            # its packet, then permit a stop receipt at that same next sequence.
            self.saved.rejected.append(packet)
            self.saved.pending = None
            self.persist()
            return {'reviewRequired':True}
        response.raise_for_status()
        if packet.phase == 'reserved':
            self.saved.rounds[packet.sessionId].accepted = True
        self.saved.sequence = packet.sequence
        self.saved.lastUptimeMs = packet.uptimeMs
        self.saved.pending = None
        self.persist()
        return response.json()

    def send(self, command, phase, **extra):
        self.flush()
        self.saved.pending = JournalEvent(eventId=str(uuid.uuid4()), sequence=self.saved.sequence+1,
            uptimeMs=self.uptime(), sessionId=command['sessionId'], commandId=command['id'],
            expectedRevision=command['expectedRevision'], phase=phase, **extra)
        # Persist both the marker and exact packet before sending any request.
        self.persist()
        return self.flush()

    def poll_once(self):
        self.connect()
        response = self.client.get('/api/device/commands')
        response.raise_for_status()
        data = response.json()
        for command in data['commands']:
            saved = self.saved.rounds.get(command['sessionId'])
            if command['type'] == 'reserve':
                if saved and (saved.fenced or saved.commandId != command['id']):
                    raise ValueError('Refusing to reuse a fenced or contradictory reservation.')
                if not saved:
                    saved = SavedRound(commandId=command['id'],sessionId=command['sessionId'],
                                       expectedRevision=command['expectedRevision'])
                    self.saved.rounds[saved.sessionId] = saved
                if not saved.accepted:
                    self.send(command,'reserved')
            elif command['type'] == 'fence':
                if saved and saved.terminal:
                    self.report_terminal(saved.sessionId)
                    continue
                if saved:
                    saved.fenced = True
                else:
                    saved = SavedRound(commandId=command['id'],sessionId=command['sessionId'],
                                       expectedRevision=command['expectedRevision'],fenced=True)
                    self.saved.rounds[saved.sessionId] = saved
                self.persist()
                self.send(command,'fenced_unstarted' if saved.accepted and saved.startUptimeMs is None else 'fenced_interrupted')
        return data

    def start_round(self, session):
        self.connect()
        saved = self.saved.rounds[session]
        if not saved.accepted or saved.fenced or saved.terminal:
            raise ValueError('Only an accepted, unfenced reservation may start.')
        if saved.startUptimeMs is None:
            saved.roundBootId = self.saved.registration.bootId
            saved.startUptimeMs = self.uptime()
            self.persist()
        return self.send(self.command(saved),'started',roundBootId=saved.roundBootId,startUptimeMs=saved.startUptimeMs)

    @staticmethod
    def command(saved):
        return {'id':saved.commandId,'sessionId':saved.sessionId,'expectedRevision':saved.expectedRevision}

    def save_terminal(self, session, payload):
        saved = self.saved.rounds[session]
        terminal = Result.model_validate(payload)
        if saved.fenced or saved.startUptimeMs is None:
            raise ValueError('A fenced or unstarted session cannot produce a new result.')
        if saved.terminal and saved.terminal != terminal:
            raise ValueError('A saved terminal result is immutable.')
        saved.terminal = terminal
        self.persist()

    def report_terminal(self, session):
        self.connect()
        saved = self.saved.rounds[session]
        if not saved.terminal:
            raise ValueError('No terminal result was durably saved.')
        return self.send(self.command(saved),'terminal',roundBootId=saved.roundBootId,
                         startUptimeMs=saved.startUptimeMs,terminal=saved.terminal)

    def reboot(self):
        # Resolve any uncertain old-boot receipt before retiring that boot.
        self.connect()
        previous = self.saved.registration
        self.saved.registration = BootRegistration(bootId=str(uuid.uuid4()), previousBootId=previous.bootId,
                                                   storageId=previous.storageId,uptimeMs=0)
        self.saved.registered = False
        self.saved.sequence = 0
        self.saved.lastUptimeMs = 0
        self.base_uptime = 0
        self.started = time.monotonic()
        self.persist()
        self.client.headers['X-Device-Boot-Id'] = self.saved.registration.bootId
        self.connect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',required=True)
    parser.add_argument('--journal',default='.tools/recovery-emulator.json')
    parser.add_argument('--reboot',action='store_true')
    args = parser.parse_args()
    token = os.getenv('STACK_EMULATOR_DEVICE_TOKEN')
    if not token:
        parser.error('Set STACK_EMULATOR_DEVICE_TOKEN in this terminal; do not put it in command arguments.')
    try:
        with httpx.Client(base_url=args.url,headers={'X-Device-Token':token},timeout=10) as client:
            emulator = RecoveryEmulator(client,args.journal)
            if args.reboot:
                emulator.reboot()
            emulator.poll_once()
            print('Boot/journal synchronized. No game was automatically started or scored.')
    except (ValueError, httpx.HTTPError, OSError):
        raise SystemExit('Emulator stopped. Preserve the journal and inspect the cabinet in the admin UI.') from None
