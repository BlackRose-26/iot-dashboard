# Durable browser updates

Implemented 19 November 2026. This completes the software foundation of build-plan step 7; LAN load and physical-cabinet acceptance gates remain open.

## Behavior and access

Signed-in administrators subscribe to `WS /api/live/admin`. Registered players subscribe to `WS /api/live/player` using their own HttpOnly session cookie. Guests use HTTP context polling; there is no public WebSocket or public leaderboard. The leaderboard still requires the player's latest round to be completed. Chat remains read-only.

Frames contain only `type` (`ready`, `invalidate`, `heartbeat`) and the current integer event `revision`. They contain no ticket, nickname, score, identity, session identifier, command or authentication token. Both roles receive safe invalidation hints and fetch their separately authorized REST views; a hint grants no additional access.

Every handshake requires an allowed browser Origin and the appropriate unexpired, unrevoked session. A player cookie cannot open the staff stream. Authentication is rechecked before each notification and every 15-second keepalive, including staff disabling. Client messages close the connection with code 1008; commands still require HTTP authentication and CSRF. Capacity is 128 sockets per worker and eight per role/account; excess clients retain polling. The combined launcher limits incoming frames to 1,024 bytes and four queued frames. Apply equivalent limits when starting Uvicorn separately.

## Commit, dispatch and recovery

`events.revision` increments inside the state-changing transaction under the existing event lock; the same transaction inserts an `outbox_events` row. Queue registration/cancellation/skipping, admissions, reservation/start/completion, simulator readiness/release and meaningful device heartbeat changes emit hints. Idempotent reservation/start/result retries and unchanged admissions do not create another event revision. Identical fresh heartbeats update timestamps without broadcasting every heartbeat; periodic refresh checks freshness.

The FastAPI lifespan starts one in-process dispatcher. Every 250 ms it reads up to 100 committed pending rows, enqueues coalesced revisions, then marks rows published. Database failures leave pending rows available for retry. Each subscriber queue holds at most one hint; the newest revision replaces the backlog. Database work runs in worker threads, outside socket sends.

Publishing means queued for fanout, not delivered to every browser. A crash before marking published repeats a harmless hint; pending rows survive dispatcher replacement. Every connect/reconnect subscribes first and refetches a snapshot. Older stored outbox rows used per-round revisions and may retain their former safe payload; the dispatcher ignores those payloads/revisions and advertises the current global revision. No migration or data reset is required.

Admin/private player snapshots include `revision` and UTC `generatedAt`, using short repeatable-read database transactions. Writes retain READ COMMITTED and their lock order. The client rejects older revisions, coalesces refreshes and schedules a follow-up for hints received during an in-flight read. Duplicate hints are ignored and gaps cause full refetches. Socket frames never directly modify scores.

Polling runs every two seconds while the stream is unavailable or before registration, and every 15 seconds while connected. Focus, restored connectivity and successful actions refresh state. Stalled streams reconnect with bounded exponential backoff and jitter. Admin footers/private tickets show live/checking status and snapshot time. Analytics and unlocked leaderboards refetch on revision changes. Closed tabs have no push guarantee.

Run **one API worker**. The registry is process-local; shared routing is required before adding workers. Physical row telemetry and trusted boot/terminal reconciliation remain unfinished work; durable command acknowledgements are now implemented separately.

## Validation actually run

- Backend suite: **197 passed**, using disposable XAMPP/MariaDB databases. New checks cover uncommitted/rolled-back changes staying invisible, committed pending-row recovery with a replacement dispatcher, global revisions/idempotency, a concurrent commit during a snapshot, role/Origin boundaries, logout revocation, rejected socket commands and bounded queues/connections. The existing device-result retry fixture verifies no extra event revision.
- Frontend suite: **33 passed**. New checks cover duplicate/gapped hints, reconnect/timeout, online recovery, role cleanup, queued refreshes and rejection of older snapshots. Production build passed.
- Fresh headless Brave, dedicated ports 8001/5174 and synthetic participants: private access; live called/playing status; loss during simulated socket failure with polling fallback; reconnect; win alert; automatic unlocked leaderboard refresh; analytics count updating from 3 to 4 without reload. **25 live frames** had only permitted keys; no browser script errors. Single-run call-to-ticket visibility: **696 ms**; polling result visibility: **413 ms**, dependent on polling phase, not a maximum. Screenshots were visually inspected. Native computer-use access timed out, so browser automation was used.

Those earlier samples are not 50-browser or LAN percentile measurements. The later [quality audit](quality-audit.md) completes actual API process termination/restart and a 50-browser loopback exercise. Event-network contention, phone HTTPS/WSS, prolonged background throttling, power cuts and physical ESP32 behavior remain acceptance work. Synthetic test databases are removed afterward. No real identities, credentials or model data are used.

## Sources and decisions

Cookie authentication/disconnect handling follow [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/); the dispatcher uses its [lifespan pattern](https://fastapi.tiangolo.com/advanced/events/). Origin checks, periodic session validation and resource bounds apply [OWASP WebSocket Security guidance](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html). Revision-only hints and REST recovery are project choices that minimize exposed information and tolerate missed delivery. Real deployment requires HTTPS/WSS.
