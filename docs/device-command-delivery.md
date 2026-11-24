# Device command delivery and review holds

**Display migration, 25 November 2026:** the game moved from the LED-matrix cabinet to a **web game screen** (a second laptop at `/screen`, played with the same arcade button through an ESP32 USB button bridge). The LED cabinet stays supported: it uses the same device protocol, Matrix v1 rules and leaderboard, and an administrator switches between the two in Settings → Game screen. See [the web game screen](game-screen.md).

**22 November 2026:** authenticated reserve/fence envelopes additionally return integer `deliverySequence`, monotonically increasing for commands from this database. Connected Matrix firmware persists the greatest accepted/stopped delivery sequence before acknowledging, rejecting all older reservations even after round details change. Preserve the database and device storage epoch together; replacing either requires explicit lineage recovery. This is delivery ordering, not player identity. See [ESP32 integration](esp32-online.md).

> Extended on 20 November 2026 by [boot-bound device recovery](device-recovery.md), including migration 005, protocol-v2 journals, terminal recovery and guarded review resolution. Original v1 claims below describe the pre-enrollment protocol. Once a cabinet registers a boot, legacy mutation endpoints cannot bypass its journal.

Implemented and checked 19 November 2026. This is the backend/emulator portion of build-plan step 4, with Machine-page diagnostics. Physical firmware, boot/journal reconciliation and release of uncertain physical-device rounds remain unfinished. The ESP32 is unavailable; the checks below used synthetic databases and an emulator.

## Implemented protocol

All device routes authenticate `X-Device-Token` against the cabinet credential hash. Browser player/admin cookies alone cannot call these routes. Current routes use `/api`, not the older proposed `/api/v1` prefix. The application still targets one event/cabinet.

1. An authorized operator calls the next player. One transaction creates the reserved session, assigned queue entry, durable `reserve` command and revision/outbox notification. Repeating the call's idempotency key returns its original session.
2. `GET /api/device/commands` returns up to five eligible commands for the authenticated cabinet. It is read-only: polling neither consumes a command nor records acceptance. Pending and accepted commands remain available until start, expiry or review. Simulator commands are excluded; disabled/maintenance cabinets receive none. No player name, student ID, credential or receipt hash is returned.
3. The device persists the command ID, session ID, expected revision, frozen rules/hash and accepted state locally before posting `POST /api/device/commands/{commandUuid}/ack`. Body: `sessionId`, `expectedRevision`, `status: "accepted"`. The server binds all three identifiers/revisions to the assigned device-source session and saves a canonical receipt hash plus acknowledgement time inside the transaction.
4. The identical receipt returns the same acknowledgement, even after start/completion, without a second transition or revision. A different receipt for that command returns 409. A rejection uses `status: "rejected"` and one code: `not_ready`, `busy`, `rules_mismatch`, `storage_failed`; it holds the round for review.
5. `POST /api/device/sessions/{sessionUuid}/start` now requires a non-expired accepted durable reservation receipt matching the session revision. It records playing/start time and marks the command applied atomically. Repeating a successful start does not create another round. A reservation/start after expiry is not allowed.
6. The existing terminal-result replay/validation endpoint remains authoritative for scores. Its repeated identical terminal payload still produces one saved result/notification.

See [synthetic command/receipt example](../contracts/device-command.example.json) and [terminal-result shape](../contracts/game-result.example.json). A previous device client that skipped the reservation receipt must adopt step 3 before starting; simulator controls retain their explicit development flow.

## Uncertain state is held

Polling reports `reviewRequired` when a reserved session's deadline has elapsed or its status is review. It does not perform writes. A rejected receipt, a first receipt attempted after expiry, or a later heartbeat detecting the elapsed reservation persists a review hold, increments session/event revisions and stops further command delivery. An already recorded identical receipt still replays its original acknowledgement; it does not override the expired start deadline. The active-machine uniqueness lock and assigned player ticket remain in place. Elapsed time is not proof that the device never started.

Administrators can use **Machine → Flag round for review**, supplying a reason. `POST /api/admin/sessions/{sessionUuid}/review` checks the staff cookie, CSRF, current revision and device source. The reason is audited; stale requests fail. This stops further reservation delivery and new server starts, but does not remotely stop an already running physical game. The original command receipt and any recorded start remain evidence. The player sees a private review ticket and has no dashboard or leaderboard access.

**There is no force-release button or timeout-based no-show resolution.** (Since 24 November a one-click "Player didn't come" action exists, but it releases only after the device confirms an unstarted fence; see [device recovery](device-recovery.md).) A trusted boot/session/terminal reconciliation protocol and audited operator resolution remain the next milestone. A result received before a valid start, a reboot with uncertain local state, or a review-held started round is not automatically reconstructed/released by this change. Physical power-cut tests and durable NVS markers must accompany that later implementation.

## UI and storage

Admin snapshots expose only safe metadata for the last five cabinet commands: type, source, expected revision, state, timestamps, rejection code and public command/session identifiers. The Machine page shows pending/accepted/applied/rejected/expired states and review warnings. Simulator entries are labelled. Acceptance is a device assertion, not independent verification of hardware or flash persistence. Live revision hints refresh the card without broadcasting command details to players. AI remains read-only and gains no command/review capability.

No migration is needed. Existing `device_commands.receipt_hash`, `acknowledged_at`, `applied_at`, `rejection_code`, `status`, `expected_revision` and expiry fields are used. Review uses existing `game_sessions.status = 'review'`, revisions, audit logs and transactional outbox. No identity data is added. Request bodies are validated and invalid inputs are not reflected in error responses.

## Emulator

`backend/device_emulator.py` performs one explicit poll/persist/receipt exchange. It never registers players, assigns turns, presses a button, starts gameplay, sends scores or frees a review hold. Use a dedicated synthetic test event/cabinet, not live event credentials. Set `STACK_EMULATOR_DEVICE_TOKEN` privately in that test terminal, then run from the project root:

```powershell
backend\.venv\Scripts\python.exe backend\device_emulator.py --url http://127.0.0.1:8001
```

The synthetic test API must already be running at that address; this command does not launch one. The default journal is ignored `.tools/device-emulator.json`. It stores at most 32 commands/receipts with fingerprints, flushes before atomic file replacement and refuses invalid/inconsistent journals. Re-running a single emulator with the same journal resends the same receipt if a response was lost. One emulator process per journal is supported. Do not commit journals or place them in Graphify inputs. This filesystem emulator does not prove ESP32 NVS behavior.

## Verification and limits

Full backend suite: **213 passed**, including 16 new command/emulator cases. Coverage includes repeated read-only polls, device/browser boundaries, concurrent duplicate receipts, conflicting/stale/malformed receipts, receipt-required start, duplicate start/result, source separation, disabled delivery, foreign-cabinet command rejection, maintenance, expiry/rejection holds, audited revision/CSRF checks, an ACK response lost after commit, and a fresh API/emulator instance replaying from MariaDB and its local journal. Corrupt/inconsistent journals stop before contacting the API. This is application recreation, not actual process-kill/power-cut testing.

Frontend suite: **36 passed**, including review-reason/revision submission, stale-write errors and a held state without release controls. Production build passed. Fresh Brave browser checks on isolated ports 8001/5174 exercised pending → accepted → applied, private playing/review updates, a disabled Call next action while another player waits, and light/dark visuals. Targeted axe WCAG 2 A/AA and 2.1 AA checks passed for the administrator Machine page and 390 px player review ticket after correcting low-contrast ticket text. Screenshots were visually inspected; no browser script errors occurred. Test servers/databases were removed afterward. XAMPP MariaDB had been stopped before testing and was started normally; application data was not reset.

Still unverified: actual ESP32 storage/button/timing behavior, boot/reboot and terminal reconciliation, interrupted-game recovery, safe no-show release, 50-browser LAN targets, real process-kill recovery and trusted phone HTTPS/WSS. See the [verified remaining-work list](remaining-work.md).

## Research basis

Polling is read-only and receipt retries have a stable intended effect, following the safe/idempotent distinction in [RFC 9110 §9.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2). The POST receipt's idempotency is an explicit application guarantee, not a claim that all POST requests are idempotent. State/receipt writes run under the existing event → machine serialization and transaction-scoped row locks described by [MariaDB FOR UPDATE](https://mariadb.com/docs/server/reference/sql-statements/data-manipulation/selecting-data/for-update). Persist-before-ACK, source isolation and conservative review holds are project-specific protocol decisions.
