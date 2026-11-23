# Boot-bound device recovery

Development resumed on 20 November 2026 at the user's request. This milestone extends [command delivery](device-command-delivery.md); the next progress report is not being generated yet.

## Authority and limits

The ESP32 owns local timing, button input and the durable game journal. The backend owns queue assignment, validated scores and transactional recovery decisions. Administrators request a stop and review evidence; neither the browser nor Stack Intelligence may fabricate a device receipt. These are authenticated device assertions, not independent proof that physical NVS or the panel works.

`005_device_recovery.sql` adds boot lineage, immutable journal events, command-to-boot bindings and a quarantine flag. Existing score replay and ticket/session uniqueness remain unchanged. Legacy unregistered cabinets retain the original protocol. Once a cabinet registers a boot, ordinary ACK/start/result endpoints cannot bypass the journal protocol. Registration is deliberately not reversible through a browser toggle.

## Wire contract

All device calls require `X-Device-Token`. After registration, calls also require the current `X-Device-Boot-Id`. A retired boot cannot send heartbeats, poll commands, start games or submit results. Authentication is separate from the admin cookie.

The [synthetic JSON examples](../contracts/device-recovery.example.json) validate against the strict API models and show the command/evidence bindings without credentials or player identity.

1. `POST /api/device/boot`: `bootId`, `previousBootId` (null for the first boot), persistent `storageId`, and integer `uptimeMs`. Persist this exact registration before sending it. Exact retries return the original receipt; a new boot must name the server's current boot as predecessor. Registration places any physical assignment into review, invalidates old recovery revisions and requires a fresh heartbeat.
2. `POST /api/device/heartbeat` retains its state/firmware/RSSI contract. It supplies observed readiness, never releases a review hold.
3. `GET /api/device/commands` supplies `reserve` commands as before. During review it can supply a `fence` command containing `id`, `sessionId`, `expectedRevision`, `bootId`, and `expiresAt`. A fence is delivered only to its current target boot. Polling does not mutate state.
4. `POST /api/device/journal` records the next durable event. Fields: `eventId`, `sequence` (consecutive, starting at 1 per boot), nondecreasing `uptimeMs`, `sessionId`, `commandId`, immutable command `expectedRevision`, and `phase`. Each exact event/sequence replay returns its original safe response, including after resolution. Conflicting replay commits a quarantine/review hold rather than rolling that hold back with the error response.

| Phase | Additional data | Backend effect |
|---|---|---|
| `reserved` | None | Accept the reservation and bind the receipt to this boot and uptime. |
| `started` | `roundBootId`, `startUptimeMs` | Start only this boot's accepted, live reservation. Save the immutable start marker. |
| `terminal` | Original `roundBootId`, `startUptimeMs`, `terminal` result | Replay the complete trace. A playing round completes normally; a missing-start/reboot round becomes terminal-pending under review. |
| `fenced_unstarted` | None; references the fence command | Confirm a persistent stop tombstone, intact accepted storage lineage and no recorded start/terminal. Offer reviewed unstarted release. |
| `fenced_interrupted` | None; references the fence command | Confirm this old session is permanently stopped. Offer an explicit no-score void if no terminal result was recorded. |

`terminal` uses the strict result schema: terminal UUID, rules hash, outcome, duration and up to 15 placements. Replay enforces the assigned version's own limits (12 for Classic v1, 15 for Matrix v1). The original start boot and accepted storage epoch must match. Uptime from different boots is never compared as one clock. Start time is bounded by the accepted monotonic offset and reservation window; terminal duration must pass both deterministic replay and server elapsed-time checks. Start markers and terminal payloads are immutable.

A terminal event before a valid accepted reservation is rejected. A complete, validated trace arriving before a server start, or after reboot, is stored for review without immediately awarding a score. A partial trace, wrong rules hash, excessive duration, changed start, changed terminal or changed storage lineage cannot be promoted to a ranked result. Later activity after a recorded fence is rejected conservatively.

## Persistent stop semantics

Before confirming a fence, firmware must stop the old game, save a tombstone identifying that session, and commit it durably. After reboot and after reconnect, that tombstone must prevent every old reserve/start command from activating the game. A timeout, an idle heartbeat, or an assertion that a round is absent from a newly erased journal is insufficient.

A lost/erased journal gets a new `storageId`. It cannot prove never-started status or recover an old result whose accepted storage epoch differs. An explicit interrupted void can still close an unknown old round only after a current-boot stop receipt; it never awards points. Conflicting authenticated evidence quarantines the round and disables these automatic resolution paths for investigation. No unrestricted force-release endpoint is provided.

## Operator workflow

The Cabinet status page shows the current boot, latest recovery phase, round revision and only the actions the server allows.

- **Request device stop:** reason and current round revision are required. The backend holds the assignment, increments the revision, expires older pending fences and issues a boot-targeted fence. The cabinet remains reserved while the operator waits for a device receipt.
- **Release unstarted round:** requires the applied current-boot fence and matching revision/evidence. Closes the old ticket as expired with no score.
- **Void interrupted round:** requires the applied current-boot stop receipt and no pending terminal result. Closes the ticket without a score. This is an explicit operator decision, not a statement that the player never started.
- **Recover recorded result:** validates the saved full terminal trace through the same score service. Exactly one result/notification is created. This path cannot discard a known terminal trace in favor of an unstarted release.

Mutation endpoints are `POST /api/admin/sessions/{sessionId}/fence` and `/resolve`, protected by admin session, CSRF, reason, expected revision and `Idempotency-Key`. Resolution additionally requires `evidenceId` and an allowed `action`. The receipt binds the key to the complete request. The same retry returns the saved response; reuse with different content fails. Audit rows retain operator, reason, session, revision and command/evidence identifiers without student identity or credentials.

Event → machine → session serialization prevents two operators from resolving the same revision twice. Database state, ticket closure, command changes, result/notification, audit, request receipt and live invalidation commit together. Recovery leaves the cabinet offline until a new authenticated ready heartbeat arrives. No old ticket is silently recycled: the schema permits one session per ticket, so an expired player must scan again to rejoin.

## Emulator and reproducibility

`backend/recovery_emulator.py` is a separate protocol-v2 emulator. Its ignored journal contains persistent storage/boot IDs, exact unsent packets, start/terminal markers and permanent session fences. Writes use flush, fsync and atomic replacement before sending. Corrupt journals fail before network access. Keep the file for investigation; do not erase it to bypass a hold. Do not reuse a v1 `device_emulator.py` journal as v2.

From the project root, set `STACK_EMULATOR_DEVICE_TOKEN` privately in the terminal, then run:

```powershell
.\backend\.venv\Scripts\python.exe backend/recovery_emulator.py --url http://127.0.0.1:8000 --journal .tools/recovery-emulator.json
```

Add `--reboot` for an explicit simulated reboot with preserved storage lineage. An ordinary invocation resumes the saved logical boot and retries uncertain receipts first. This CLI only synchronizes/polls; it never assigns turns, automatically presses the button or creates scores. Python tests call explicit start/save-terminal/report-terminal methods with synthetic traces. Actual power-loss startup/receipt recovery on firmware is still a hardware acceptance gate.

## Verification — 20 November 2026

- Full backend regression: 305 passed against disposable XAMPP databases. After the rejected-start retry fix, all 23 recovery-specific tests passed, including the additional regression (306 distinct backend cases are now collected).
- Frontend: 48 tests passed and production build passed. Formatting and Ruff E9/F821/F822/F823 checks passed. Documentation link/structure checks passed; the optional MySQL-dialect parser was unavailable, so the checker itself provides structural SQL checks only.
- Actual Edge browser suite: 9 passed, including a boot-bound stop/release journey, private expired player ticket with no result notification, and light/dark recovery-page axe checks. Adding a 360 px assertion exposed overflow in cabinet facts/the shared status badge; wrapping was fixed without hiding overflow, then all four affected browser flows passed again. Screenshots were visually inspected.
- Migration 005 was applied to the local XAMPP project schema after disposable-database verification. Daily setup retained existing credentials/data. Existing user API/Vite processes were kept running; direct and proxied health both returned HTTP 200.
- Checked protocol cases include retired/changed boots, stale revisions/evidence, missing/invalid acceptance, wrong command binding, out-of-order sequences, nonmonotonic/extreme uptime, immutable start/terminal data, invalid rules/trace/timing, concurrent operator resolution, no-score void, storage-lineage loss, quarantined conflicting replay, exact terminal retry, missing-start/reboot result recovery, corrupt emulator journals and lost receipt after commit.

Physical ESP32/NVS, electrical power loss, panel/button timing and event-LAN/phone behavior were not run. Existing upstream Starlette/TestClient deprecation warnings remain; they do not represent failed assertions.

## Research basis

Espressif documents that [`esp_timer_get_time()` restarts from zero after deep sleep](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/esp_timer.html). Boot IDs therefore scope monotonic clocks. Its [NVS documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html) requires committing pending changes and describes recovery/error conditions. Persist-before-receipt and retaining a failed journal are project decisions derived from those guarantees; filesystem emulator success does not validate flash behavior. Transactional serialization follows [MariaDB row-lock behavior](https://mariadb.com/docs/server/reference/sql-statements/data-manipulation/selecting-data/for-update).
