"""Durable, post-commit invalidations. REST snapshots remain authoritative."""
import asyncio
from contextlib import suppress
import logging
import uuid

from sqlalchemy.exc import SQLAlchemyError

from .database import all_rows, execute, one
from .security import now

logger = logging.getLogger(__name__)


def record_change(c, kind, entity=None):
    # Call inside the same transaction as the state change, under the event lock.
    execute(c, "UPDATE events SET revision=revision+1 WHERE code='acs-day'")
    event = one(c, "SELECT id,public_id,revision FROM events WHERE code='acs-day'")
    execute(c, '''INSERT INTO outbox_events
      (public_id,event_id,event_revision,event_type,entity_public_id,payload_safe)
      VALUES(:id,:event,:revision,:kind,:entity,'{}')''',
      id=str(uuid.uuid4()), event=event['id'], revision=event['revision'],
      kind=kind, entity=entity or event['public_id'])
    return event['revision']


class LiveHub:
    """Single-worker fanout; one coalesced hint per subscriber bounds memory."""
    def __init__(self, engine, interval=0.25, heartbeat=15):
        self.engine = engine
        self.interval = interval
        self.heartbeat = heartbeat
        self.clients = {}
        self.task = None

    def subscribe(self, principal):
        if len(self.clients) >= 128 or sum(p == principal for p in self.clients.values()) >= 8:
            return None
        queue = asyncio.Queue(maxsize=1)
        self.clients[queue] = principal
        return queue

    def unsubscribe(self, queue):
        self.clients.pop(queue, None)

    def broadcast(self, revision):
        for queue in self.clients:
            if queue.full():
                previous = queue.get_nowait()
                revision_for_client = max(previous, revision)
            else:
                revision_for_client = revision
            queue.put_nowait(revision_for_client)

    def pending(self):
        with self.engine.connect() as c:
            rows = all_rows(c, '''SELECT id FROM outbox_events
              WHERE published_at IS NULL AND next_attempt_at<=:now ORDER BY id LIMIT 100''', now=now())
            # Old outbox rows used per-session revisions. Only the current global
            # revision is advertised, so a legacy row cannot invent future state.
            revision = one(c, "SELECT revision FROM events WHERE code='acs-day'")['revision']
            return rows, revision

    def published(self, rows):
        with self.engine.begin() as c:
            for row in rows:
                execute(c, '''UPDATE outbox_events SET published_at=:now,attempts=attempts+1
                  WHERE id=:id AND published_at IS NULL''', now=now(), id=row['id'])

    async def dispatch_once(self):
        rows, revision = await asyncio.to_thread(self.pending)
        if rows:
            self.broadcast(revision)
            # Mark only after enqueue. A crash before this commit repeats a safe hint.
            await asyncio.to_thread(self.published, rows)
        return len(rows)

    async def run(self):
        while True:
            try:
                await self.dispatch_once()
            except SQLAlchemyError:
                # Do not log SQL parameters or credentials. Polling also retries.
                logger.warning('Live updates are waiting for the event database.')
            await asyncio.sleep(self.interval)

    def start(self):
        self.task = asyncio.create_task(self.run())

    async def close(self):
        if self.task:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                await self.task
