> Current implementation: QR entry, persistent private queue/tickets, admin login and neutral admin light/dark themes now exist. See [player flow and access update](player-flow-and-access.md) for the current behavior, API, migrations and limits. Earlier preview-only statements below are historical.

# Stack Moko Baby — step-by-step build plan

**Latest hosting choice, 22 November:** use the [free PC + XAMPP + HTTPS tunnel](free-online.md) selected after the Render cost discussion. Public health and private image compilation passed. Next run the configured image in Wokwi with the user's approved upload path, verify the cabinet heartbeat and assigned game journey, then retain the separate physical/NVS gates. Keep the prepared Render option inactive.

## Current device/hosting milestone — 22 November 2026

The user selected Wokwi first, Matrix v1 (16 columns, 15 levels, maximum 15 points), online registration/queue/dashboard with physical-button gameplay, and the free PC/XAMPP HTTPS tunnel. [ESP32/online setup](esp32-online.md) is the current work package. Classic histories retain their original rules. Firmware compilation, local Matrix device/API checks and public HTTPS access checks passed. Next verify the actual Wokwi boot/heartbeat and assigned button-game journey using the private configured image. Follow with real ESP32 NVS/power/button/display/audio acceptance and event load tests. Do not mark hardware complete from emulator/browser success.

## Active milestone — Wokwi and free HTTPS, 22 November 2026

Implement the user's selected Matrix v1 game (16 columns, 15 levels, one point per level) with version-bound replay and separate Classic history. Connected firmware, durable boot/journal handling and same-origin React/API serving are prepared; see [integration guide](esp32-online.md). The free launcher configures the temporary HTTPS origin and builds private firmware. Verify the actual Wokwi exchange and complete QR → registration → assigned physical-button round → validated win/loss → notification/leaderboard journey. XAMPP and local Ollama remain on the PC. Keep Render inactive. Actual ESP32, power/NVS/audio and event load checks remain separate gates.

**Implemented on 21 November 2026.** Administrators can open Settings → Review questions or visit `/admin/question-review`. Each card shows one synthetic question, its earlier topic, suggested meaning and expected action. Reviewers can confirm it, correct it or mark it unclear. Search, filters, navigation and a saved progress count cover all 325 cases. Migration 006 stores each administrator's versioned decisions separately from frozen labels and chat training examples. The [typed-context regression](nlp-evaluation/results/typed-context-v2-regression.json) records 146/325 accepted against the original 130/325, including 7/25 follow-ups. Human decisions can guide later adjudication and development using separate examples.

**NLP repair, 20 November 2026:** implement and verify [public language projection, separate topical checking and explicit semantic routing](nlp-routing-repair.md) using independent development probes. Preserve the original 325-case measurement and gold labels; freeze predictor/lexicon/scorer for each explicitly labelled consumed-set replay. Subsequent unseen acceptance requires a new independently authored/adjudicated test set with 20–50 diverse cases per primary intent. Development scores and reused tests do not close that gate. Do not automatically train model weights or start the next progress report.

**Authorized offline comparison completed:** the [isolated NLP lab](nlp-offline-experiment.md) ran TF-IDF, frozen multilingual embeddings, actual local SetFit adaptation and the current Ollama routing adapter. The [measured development report](nlp-evaluation/offline-lab-20261120.md) supports no production replacement: SetFit did not improve the 130-case result and failed misleading-history diagnostics. Live Ollama weights/routing remain unchanged. The [label guide](nlp-label-guide.md) and typed-state prototype are implemented; reviewed rare-class/topic-change training families and independent final collection/review remain next gates. The [325-case candidate collection](nlp-evaluation/candidate-v2-preparation.md) is now filled, with 25 AI-authored questions per intent and no automated reference collisions; independent review and final evaluation remain pending. No progress report is requested.

**History follow-on completed:** [training-only history augmentation and current-question ablation](nlp-evaluation/history-lab-20261120.md) ran in a new frozen experiment without changing the first run. It addresses the shortcut but does not improve overall correctness/coverage enough for promotion. Forty supported development requests are blocked upstream. Next: design a privacy-preserving separation of input refusal, wording and scope; obtain reviewed rare-class/multi-turn data; validate on new development families before a separately reviewed final test. Existing cohorts are consumed regression material.

**Frontend styling, 20 November 2026:** the user confirmed React.js JavaScript/JSX and Tailwind CSS. Tailwind 4.3.5 and its Vite plugin are installed; shared primitives and the recovery layout use utilities. Follow [the Tailwind UI conventions](tailwind-ui.md) for subsequent page updates and migrate specialized CSS as those pages change. This styling task does not create the next progress report.

20 November 2026 · Development resumed; current implementation and remaining acceptance gates

The application now has a React JavaScript frontend, FastAPI backend, XAMPP/MariaDB migrations, private QR registration/tickets, transactional FIFO assignment, score replay, admin views and local Ollama analytics. Browser live synchronization is implemented below. Earlier milestone notes describe their dates, not the current whole application. Numeric rules remain proposals until play-tested. Estimates are rough; acceptance evidence determines completion.

| Step | Current state | Remaining gate |
|---|---|---|
| 0, 2 | Proposed rules and deterministic backend replay/simulator exist | ESP32/panel, wiring, local firmware engine, latency/playability |
| 1 | Repeatable npm startup, database setup and Graphify installed | Release packaging and final operational checks |
| 3 | Staff sessions, encrypted identity and private player access implemented | Distinct operator/admin permissions, staffed recovery, retention/rotation and trusted phone HTTPS |
| 4 | FIFO, reservations, boot-bound journal/stop receipts, emulator and guarded recovery UI implemented | Physical device journal/NVS and power-loss acceptance |
| 5 | Backend trace replay and atomic result/notification/outbox commit implemented | Firmware journal, reboot/power-cut tests and physical integration |
| 6 | Reference-based admin/player pages, settings, real analytics and recovery forms implemented | Hardware telemetry and final release accessibility review |
| 7 | Authorized live hints, reconnect, polling, actual test-process kill/recovery and 50 loopback browser contexts checked | Event-LAN measurements, prolonged soak and phone WSS |
| 8 | Local Ollama routing, verified tools, private memory and reviewed examples; isolated offline SetFit comparison completed without promotion | Reviewed training coverage, independent final evaluation and full release-policy checks; production fine-tuning remains deferred |
| 9 onward | Release/operations work remains | Follow the exit gates below; no hardware completion is claimed |

Next independent work: enforce distinct operator/admin permissions and safe provisioning, then identity lifecycle and operational release gates. Boot/session/terminal reconciliation and guarded recovery are implemented and locally checked; physical ESP32/NVS acceptance still waits for available hardware. See the [verified remaining-work audit](remaining-work.md).

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

**Resumed 20 November 2026:** [boot-bound device recovery](device-recovery.md) adds protocol-v2 journals, immutable start/terminal evidence, boot-targeted fences, audited/idempotent guarded operator decisions and a persistent recovery emulator. Legacy compatibility is retained only for cabinets that have never registered a boot. Physical NVS/power-loss/firmware validation is still pending. See remaining-work.md for executed verification and outstanding gates.

**Command milestone, 19 November 2026:** [device delivery and review holds](device-command-delivery.md) now provides read-only polling, durable accepted/rejected receipts, idempotent retries, receipt-required start, a file-journal emulator and admin/private-player review states. Full suite: 213 backend and 36 frontend checks; build, synthetic Brave and targeted axe checks passed. Lost-ACK replay after API/emulator recreation is checked; actual process termination, physical firmware/NVS and release of uncertain rounds remain pending. No migration or database reset is required.

1. Build queue join/cancel/position endpoints and FIFO query. Duplicate submissions reuse a live ticket.
2. Provision machine credentials out of band; store hashes. Build fresh-heartbeat eligibility and maintenance/admission states.
3. Implement event → machine → queue → session lock order, one active-session unique constraint, reservation command creation and operation receipts.
4. Implemented: device command polling/acknowledgment, expected revision, canonical receipt hashes and idempotent delivery. Commands commit before delivery; the emulator persists before ACK. Actual firmware persistence remains unverified.
5. Implemented in software: rejected/expired reservations and explicit staff review retain the cabinet and ticket. Boot-targeted fence receipts support guarded unstarted release, interrupted no-score void and validated terminal recovery. Conflicting evidence remains quarantined. No timer silently frees a physical-device round; hardware persistence is unverified.

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
2. Implement mobile QR registration, private ticket/result and post-completion player leaderboard. The leaderboard is not public. Use synthetic identity fixtures.
3. Build overview in the reference's two-column silhouette with lime banner, left list and right live gauge/operations tray. Build Queue, Sessions and Machines details using the same design language.
4. Add pending/accepted/applied command status, review lock reasons, safe abort/invalidation forms and clear stale/empty/error states.
5. Implement deterministic aggregate endpoints with timezone/ruleset filters and documented denominators. Avoid charts for nonexistent sensor data.
6. Review realistic screenshot states at desktop/tablet/mobile sizes; verify focus, contrast, labels and reduced motion. Use the supplied image as the visual source, not guessed assets from inaccessible Dribbble content.

**Exit:** AC-01/AC-10/AC-11 pass; a visual comparison demonstrates the requested reference treatment, and no sample metrics masquerade as real data.

## 7. Add durable live updates — 0.5–1 day

**Implemented, 19 November 2026:** [durable browser updates](live-updates.md) records the protocol, recovery guarantees, actual checks and limits. Full checks: 197 backend tests, 33 frontend tests, Vite production build and synthetic Brave flows passed. The later [quality audit](quality-audit.md) adds an actual process kill/restart, 50 loopback browser clients and synthetic restore. Hardware and event-LAN gates remain open.

1. Implemented: transactional global event revisions, bounded outbox dispatcher and separate authenticated staff/player endpoints. There is no unauthenticated stream; frames contain only type/revision.
2. Implemented: subscribe then fetch coherent snapshots, deduplicate revisions, refetch on gaps/reconnect, coalesce in-flight refreshes, reject older views, poll at 2 seconds on fallback/15 seconds live, and display last-updated indicators. Analytics and completed-player leaderboards refresh on revisions.
3. Local release exercise completed: force-terminate the actual test API after result commit with outbox dispatch deferred, restart it, recover the browser result, then replay the identical terminal payload. One completed round and one notification remain. Hardware power failure/reconciliation is a separate open gate.
4. Local exercise completed with 50 independent browser sessions and 250 context requests at concurrency 20. See measured latencies in the audit. Run the event-LAN/phone load test separately; loopback is not that acceptance gate. Keep one API worker until shared notification routing is implemented.

**Exit:** AC-07/AC-09 meet measured LAN targets; restarting API cannot erase a committed result or durable command.

## 8. Add constrained AI analytics — 1–2 days

**Reviewed-example update, 18 November 2026:** the user chose memory plus reviewed examples. Admins can explicitly select sanitized routing inputs, correct labels, save pending, approve/reject/revise/remove, and export approved current-context JSONL. Migration 004 adds private owner-scoped `ai_training_examples`; no raw messages, answers or game values are captured. 100 backend tests (14 new workflow cases), the Vite build and synthetic computer-use review/download flow passed. Actual fine-tuning/import/activation and held-out model improvement remain a separate unimplemented stage; see [assistant-training.md](assistant-training.md).

**Grounded memory update, 18 November 2026:** flexible system-topic/social classification, reviewed knowledge cards, private per-admin typed conversation memory, language/length preferences, memory-off and Forget controls are implemented. Migration 003 adds `ai_admin_memory`; no raw conversation or game facts are retained, and no model-weight training occurs. Revisions prevent forgotten context returning from an older request. 86 backend tests (75 targeted assistant/memory checks), the production build, formatting and targeted synthetic computer-use flows passed. See the assistant guide for measured scope and remaining release gates.

**Conversational update, 17 November 2026:** local English/Taglish social replies, preserved analytical context across small talk, concise requested-metric templates, and expandable evidence are implemented. Social exchanges work while Ollama loads; factual analytics still requires the local model and approved backend tools. The response contract adds `conversation` and typed summary presentation fields. 63 assistant unit checks, the Vite build and targeted synthetic computer-use flows passed; see the assistant guide for exact scope. Broader release/hardware gates remain open.

**Source-review corrections, 17 November 2026:** corrected the end-to-end query deadline/background metadata queue, unsupported time-window interpretation, per-level accuracy and metric scopes, empty result-cohort classification, and stale retries after filter changes. Targeted assistant checks have now run; see the assistant guide for exact coverage and remaining acceptance work.

**Implementation update, 17 November 2026:** local Ollama schema-constrained intent routing, approved-vocabulary privacy normalization, seven bounded read-only analytics operations, safe request metadata, protected API routes and factual English/Taglish chat answers are implemented. Analytics charts share the same backend calculations. See [current implementation and manual acceptance](admin-assistant.md). Local Ollama installation/model status is recorded in the assistant guide. After the user requested testing, 38 assistant unit checks and the Vite build passed; local routing and disposable MariaDB/browser chat flows were exercised. A separate 120-second background model preparation fixes cold loading without extending the 20-second question deadline. See the guide for measured samples and exact browser cases. Broader policy/load/recovery and ESP32 gates remain pending. Earlier UI-only milestones and prospective steps below are historical where superseded; do not mark their exit gates passed.

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

## Quality audit — 19 November 2026

The [cross-system audit](quality-audit.md) fixes confirmed request/authentication, QR, game-duration, cabinet-state, chart, async-state and NLP-scope defects. It records executed checks and remaining limitations. The user explicitly resumed roadmap development on 20 November; the earlier audit pause is superseded. Proposed numeric game settings remain subject to physical play-testing.
