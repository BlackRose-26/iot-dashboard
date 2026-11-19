"""Explicit command-handshake emulator. No queue assignment or automatic gameplay."""
import argparse
import json
import os
from pathlib import Path

import httpx

from app.device_commands import CommandAcknowledgement, UUID_PATTERN
from app.game import canonical
from app.security import digest


class CommandEmulator:
    def __init__(self, client, journal):
        self.client = client
        self.journal = Path(journal)
        self.records = {}
        if self.journal.exists():
            data = json.loads(self.journal.read_text(encoding='utf-8'))
            if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('commands'), dict):
                raise ValueError('Unsupported emulator journal. Keep it for investigation.')
            if len(data['commands']) > 32:
                raise ValueError('Emulator journal exceeds its bounded history.')
            import re
            for key, value in data['commands'].items():
                if (not re.fullmatch(UUID_PATTERN, key) or not isinstance(value, dict)
                        or set(value) != {'receipt','payloadHash','command'}):
                    raise ValueError('Invalid emulator command journal.')
                CommandAcknowledgement.model_validate(value['receipt'])
                if not isinstance(value['payloadHash'], str) or not re.fullmatch(r'[a-f0-9]{64}', value['payloadHash']):
                    raise ValueError('Invalid emulator payload fingerprint.')
                command = value['command']
                if (not isinstance(command,dict) or command.get('id') != key
                        or digest(canonical(command)).hex() != value['payloadHash']):
                    raise ValueError('The emulator command journal is inconsistent.')
                if (value['receipt']['sessionId'] != command.get('sessionId')
                        or value['receipt']['expectedRevision'] != command.get('expectedRevision')):
                    raise ValueError('The emulator receipt does not match its saved command.')
            self.records = data['commands']

    def persist(self):
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.journal.with_suffix(self.journal.suffix+'.tmp')
        with temporary.open('w', encoding='utf-8') as output:
            json.dump({'version':1, 'commands':self.records}, output)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, self.journal)

    def poll_once(self):
        response = self.client.get('/api/device/commands')
        response.raise_for_status()
        data = response.json()
        if data['reviewRequired']:
            return {'accepted':0, 'reviewRequired':True}
        count = 0
        for command in data['commands']:
            receipt = CommandAcknowledgement(sessionId=command['sessionId'],
                expectedRevision=command['expectedRevision'],status='accepted').model_dump()
            fingerprint = digest(canonical(command)).hex()
            record = {'receipt':receipt, 'payloadHash':fingerprint, 'command':command}
            existing = self.records.get(command['id'])
            if existing is not None and existing != record:
                raise ValueError('A saved command changed. Operator review is required.')
            if existing is None:
                while len(self.records) >= 32:
                    self.records.pop(next(iter(self.records)))
                self.records[command['id']] = record
                # Simulates the durable marker required before a real device ACK.
                self.persist()
            response = self.client.post(f"/api/device/commands/{command['id']}/ack", json=receipt)
            response.raise_for_status()
            count += 1
        return {'accepted':count, 'reviewRequired':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='Dedicated synthetic test API URL; no frontend port.')
    parser.add_argument('--journal', type=Path, default=Path(__file__).resolve().parents[1]/'.tools/device-emulator.json')
    args = parser.parse_args()
    token = os.getenv('STACK_EMULATOR_DEVICE_TOKEN')
    if not token:
        parser.error('Set STACK_EMULATOR_DEVICE_TOKEN for the synthetic cabinet; never pass a token in the URL.')
    try:
        with httpx.Client(base_url=args.url, headers={'X-Device-Token':token}, timeout=5) as client:
            result = CommandEmulator(client,args.journal).poll_once()
        print(json.dumps(result))
    except (ValueError, OSError, httpx.HTTPError):
        # Avoid rendering URLs, headers or a corrupt journal in console output.
        parser.exit(1, 'Command handshake stopped. Check the test API and preserved journal.\n')


if __name__ == '__main__':
    main()
