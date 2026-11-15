> Current implementation: QR entry, persistent private queue/tickets, admin login and neutral admin light/dark themes now exist. See [player flow and access update](player-flow-and-access.md) for the current behavior, API, migrations and limits. Earlier preview-only statements below are historical.

# Stack Moko Baby — step-by-step build plan

15 November 2026 · Dependency-ordered implementation baseline

This task delivers planning documents and Graphify setup. The initial frontend pages in step 6 are now implemented as a local sample-data preview; backend, identity security, hardware and live integration steps remain future work. Effort estimates are rough engineering estimates for a small student team, excluding procurement, unfamiliar-tool learning and institution approvals; use exit gates rather than dates as proof of completion.

## 0. Resolve physical and operational constraints — 0.5–1 day

Confirm exact ESP32, HUB75 panel resolution/scan/driver and compatible library. Candidate: a standard 64×32 HUB75 panel rotated for a 32×64 logical portrait cabinet, with an 8×12 game board rendered as 4×4-cell squares, leaving 16 logical pixels for labels/foundation. This is a fit proposal, not an asserted panel in the user's photo. Verify portrait coordinate mapping, refresh, RAM and usable cabinet dimensions before buying.

Inventory button, buzzer driver, LEDs, regulated panel supply, fuse, connectors and enclosure. Panel power must come from a rated supply with common ground and suitable level translation; never power the matrix through ESP32 GPIO/USB. Follow the actual panel/board specifications. Produce reviewed wiring and a power/current budget before energizing the assembly. Choose pins only after checking the board's boot/flash constraints and driver mapping.

Confirm student-ID format, identity recovery owner, retention settings, event rules, LAN/certificate plan and AI budget. Record decisions in [research-and-decisions.md](research-and-decisions.md).

**Exit:** panel color test, stable button reading, measured supply behavior, phone-to-server reachability plan, written ruleset proposal. Do not block independent frontend/API scaffolding while awaiting a cabinet enclosure.

## 1. Scaffold the repository and repeatable environment — 0.5–1 day

1. Open `D:\iot-dashboard` as the project. Review `AGENTS.md` and this documentation; initialize Git only if desired for the implementation project, keeping existing files intact.
2. Create frontend React/JavaScript/Vite app using Vite’s `react` template, `.jsx` components and `.js` modules and backend Python package with the modular layout in [tech-stack.md](tech-stack.md). Choose compatible supported versions, write lockfiles and record toolchain versions.
3. Create `.env.example` with dummy values; ignore `.env`, virtual environments, firmware secrets, dumps and exports. Use a local synthetic event seed.
4. Use the existing XAMPP MySQL service (locally MariaDB 10.11.16 on port 3306), add a database health check, native FastAPI development command and one proxy origin. Create a dedicated app user and keep database/phpMyAdmin local. Docker/WSL2 is not required; follow the XAMPP setup in tech-stack.md.
5. Add formatting, linting and basic frontend/backend checks, plus a real XAMPP/MariaDB integration-test target. Generate a JavaScript API client from OpenAPI when contracts exist; use JSDoc for editor hints and runtime validation for network payloads.
6. Verify Graphify CLI and project instructions. Refresh the map after structural changes and verify one query points to real source files.

**Exit:** one documented command sequence starts frontend/API and connects to XAMPP/MariaDB; ready endpoint checks DB; secrets absent from tracked files and graph.

## 2. Implement and prove the local game engine — 1–2 days

1. Implement pure deterministic state machine with injectable clock/button events. Keep rendering, networking and persistence behind interfaces.
2. Encode immutable `classic-v1` proposed rules. Add fixtures for perfect/narrowed rows, bounce, zero overlap, no presses, debounce/held button and simultaneous movement/deadline events.
3. Implement LEDs/audio/display effects and readiness/result screens. Keep networking in a separate task/nonblocking scheduling path.
4. Measure input-to-lock latency and display stability with networking enabled. Validate board portrait mapping and playability.
5. Freeze accepted rule constants and canonical hash; export the same fixtures for backend replay. If rules change, publish `classic-v2` rather than editing a used version.

**Exit:** independent local rounds work; score example is 350; target-row win max is 1,500; AC-03/AC-08 hardware and simulator checks recorded.

## 3. Implement database, identity and staff authentication — 1–2 days

1. Turn [schema.sql](schema.sql) into an initial Alembic migration; apply to an isolated MariaDB instance matching the XAMPP version. Verify generated uniqueness, CHECK and composite FK behavior.
2. Implement identity service with normalized student-ID validation, HMAC lookup and AES-GCM encryption; keys stay outside the database/source. Test nonce handling, duplicates, leading zeros and rotation.
3. Implement registration sessions, private player ticket access, generic duplicate-ID responses, operator-assisted recovery and idempotent registration receipts. Do not treat student ID as a password.
4. Implement staff session cookies, Argon2id passwords, operator/admin permissions, CSRF protection and enabled/revoked/expired checks.
5. Implement safe audit and explicit DTOs for public/staff/private identity responses; test that IDs never leak through errors/logs.

**Exit:** AC-01 and role-boundary tests pass against MySQL; identity decryption is admin-only and audited. Student ID entry uses HTTPS with tested trust.

## 4. Implement queue and transactional session assignment — 1–2 days

1. Build queue join/cancel/position endpoints and FIFO query. Duplicate submissions reuse a live ticket.
2. Provision machine credentials out of band; store hashes. Build fresh-heartbeat eligibility and maintenance/admission states.
3. Implement event → machine → queue → session lock order, one active-session unique constraint, reservation command creation and operation receipts.
4. Add device command polling/acknowledgment, expected revision and idempotent delivery. Persist commands before exposing them.
5. Implement no-show expiry only after device-confirmed non-start; uncertain state enters review and retains the lock.

**Exit:** AC-02/AC-06/AC-10 concurrency and race fixtures pass; repeated command delivery produces one reserved round.

## 5. Integrate firmware persistence and validated results — 1–2 days

1. Persist accepted reservation/start/terminal markers with version/checksum and bounded journal. Test storage-full and corruption behavior.
2. Add HTTP/S polling and upload with verified certificate, per-device authentication, bounded bodies, backoff/jitter and short networking deadlines.
3. Add backend pure replay using shared traces; compute score/levels/accuracy, legal timing and terminal outcome without trusting a reported score.
4. Commit session/placements/queue/outbox/receipt in one transaction. ACK only after commit. Replay identical terminal ID returns original receipt.
5. Exercise reordered start/result messages, lost ACK, reboot before start, power cut during play and reboot after terminal persistence. Add operator reconciliation UI/API without deleting original evidence.

**Exit:** AC-04/AC-05/AC-06 pass with device emulator and real cabinet; no new ranked round while terminal evidence is unacknowledged.

## 6. Implement reference-matched web views — 2–3 days

1. Build CSS tokens and reusable rounded card, pill row, circle control, blue tile, gauge and state badge from [dashboard-design.md](dashboard-design.md).
2. Implement mobile QR registration, private ticket and result, then public event/ruleset leaderboard. Use synthetic identity fixtures.
3. Build overview in the reference's two-column silhouette with lime banner, left list and right live gauge/operations tray. Build Queue, Sessions and Machines details using the same design language.
4. Add pending/accepted/applied command status, review lock reasons, safe abort/invalidation forms and clear stale/empty/error states.
5. Implement deterministic aggregate endpoints with timezone/ruleset filters and documented denominators. Avoid charts for nonexistent sensor data.
6. Review realistic screenshot states at desktop/tablet/mobile sizes; verify focus, contrast, labels and reduced motion. Use the supplied image as the visual source, not guessed assets from inaccessible Dribbble content.

**Exit:** AC-01/AC-10/AC-11 pass; a visual comparison demonstrates the requested reference treatment, and no sample metrics masquerade as real data.

## 7. Add durable live updates — 0.5–1 day

1. Implement outbox dispatcher and authorized public/player/staff channels. Emit only safe post-commit notifications with event revisions.
2. Client subscribes and refreshes snapshots, deduplicates IDs and refetches on gaps/reconnect. Include fallback polling and last-updated indicators.
3. Restart API between result commit and dispatch; verify refresh eventually arrives. Disconnect/reconnect browser mid-round; no stale action or duplicate ranking.
4. Load-test proposed 50 browsers and capture API/live-update latency; tune only after measurement. Keep one API worker until shared notification routing is implemented.

**Exit:** AC-07/AC-09 meet measured LAN targets; restarting API cannot erase a committed result or durable command.

## 8. Add constrained AI analytics — 1–2 days

**UI milestone, 16 November 2026:** the [Stack Intelligence bottom chat](admin-assistant.md) is implemented in the signed-in admin shell. Expand/minimize, suggested questions, drafting, local preview replies and conversation clearing are present. This is design only; provider selection, NLP, server tools and live analytical responses remain pending. Preserve its neutral light/dark theme and admin-only placement during integration. Cover IoT, dashboard definitions, aggregate players, queue, scores/results and trends under the read-only policy.

1. Choose provider/model based on actual access, structured-tool support, budget and data policy. Record exact model/version and configured limits.
2. Implement prewritten aggregate tools and server-bound scope. Use opaque public codes; resolve nicknames locally. Block/redact private input before provider calls.
3. Apply system policy and strict response schema from [ai-system-rules.md](ai-system-rules.md); validate every quantitative claim/reference. Format metrics in code where possible.
4. Implement deadlines, call/rate/token limits, usage logging and deterministic unavailable/no-data fallback.
5. Run full policy fixture suite, including injected nickname, student-ID request, fake metric references, different rulesets and provider outage.

**Exit:** AC-12 passes; AI has no SQL, identity or device-control capability; gameplay and normal dashboard functions survive AI shutdown.

## 9. Event readiness and release rehearsal — 1–2 days

1. Configure event PC hostname/IP, HTTPS trust, firewall, LAN isolation settings and startup/restart behavior. Test actual phones scanning printed QR while internet is disconnected.
2. Verify encrypted backups and isolated restore; exercise identity purge/anonymization on synthetic data, then verify public exports.
3. Run 50 consecutive cabinet rounds and a 2-hour mixed-load soak. Include Wi-Fi drops, stale device, full queue, lost ACK, API restart, MySQL restart and physical power interruption.
4. Rehearse full demonstration: QR → required private student ID → queue → reserved device → button game → validated result → live public ranking → staff analytics with evidence.
5. Write operator runbook for absent player, reboot, jammed button, storage fault, connection stale, disputed result and server restart. Make a spare-parts list.
6. Record release hashes: frontend/backend commit, migration head, rules hash, firmware build and Graphify snapshot freshness. Resolve open release blockers.

**Exit:** all acceptance criteria recorded with evidence; outstanding limitations are visible. Do not label hardware, TLS, MySQL recovery or AI validation complete without running them.

## Dependency and scope discipline

Steps 1 and the pure engine in 2 can progress independently of enclosure fabrication. Identity/schema precede queue and device integration; verified results precede rankings and AI. UI components can be built with labeled fixtures while APIs mature. Adaptive difficulty is deferred until the fixed ruleset, reliability and fairness are demonstrated; any later adaptive mode gets a separate leaderboard cohort.

Estimated total: roughly 11–20 focused working days for a small team, subject to hardware availability and experience. This is a planning range, not a delivery commitment.
