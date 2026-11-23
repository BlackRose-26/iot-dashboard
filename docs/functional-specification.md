> Current implementation: QR entry, persistent private queue/tickets, admin login and neutral admin light/dark themes now exist. See [player flow and access update](player-flow-and-access.md) for the current behavior, API, migrations and limits. Earlier preview-only statements below are historical.

# Stack Moko Baby — functional specification

## Confirmed integration update — 22 November 2026

The user selected the uploaded sketch's **16-column, 15-level stacker**, six-cell starting width and **one point per successful placement, maximum 15**, with no perfect bonus. These Matrix v1 settings supersede older Classic-only proposals below for subsequent assignments. Existing Classic records keep their original ruleset. Players register/queue online, then use the cabinet's physical button; no remote browser gameplay is requested. First integration is Wokwi, followed by physical verification. The current Wokwi link uses a three-step 500 ms countdown, readable score/time HUD, GAME/OVER and DFPlayer tracks; the connected firmware preserves those functions. Timing, power and difficulty still need physical play-testing. Render hosts game/dashboard services; local AI connection is a later phase. See [the current integration contract and gates](esp32-online.md).

Version 0.1 · 15 November 2026 · Implementation baseline

Current browser synchronization uses authenticated revision-only hints and authoritative private/staff snapshots, with polling and reconnect recovery. See [implemented contract and limits](live-updates.md). [Boot-bound device recovery](device-recovery.md) now supports sequenced journals, terminal-pending review, permanent stop receipts and guarded administrative resolution. A timeout alone cannot release a device assignment. Recovery never awards points for an incomplete trace; no-score closure expires the ticket and requires a new scan to rejoin. Physical firmware/NVS and power-loss acceptance remain pending.

## 1. Product and scope

Stack Moko Baby is a carnival cabinet with an ESP32, LED matrix, arcade button and sound/light feedback. A player scans a QR code, registers privately, joins the queue, then times button presses to align moving rows. The device runs the round locally; the server assigns turns, validates results and updates a web dashboard. Authorized staff can ask a read-only AI assistant about recorded game statistics.

The final project name, LED/button gameplay, private required student ID, React JavaScript, XAMPP database and dashboard reference are confirmed. Remaining feature choices below are recommended requirements derived from provisional plans. They are reviewable implementation decisions, not claims that the attached plans were finalized.

### First release

| ID | Capability | Requirement |
|---|---|---|
| FR-01 | Registration | Machine-specific QR opens a mobile page; require student ID and public nickname; present a privacy notice before submission. |
| FR-02 | Identity | Recognize returning players using a keyed student-ID lookup; assign an unrelated random public code. Student ID is never a public identifier or a login secret. |
| FR-03 | Queue | Admit one live queue entry per player per event; assign the oldest eligible entry to an idle machine transactionally. |
| FR-04 | Start | Only a server-authorized session can start a ranked round; the physical button confirms readiness. |
| FR-05 | Game | ESP32 moves rows, resolves button placement, countdown, timeout, sound and LEDs without waiting for network responses. |
| FR-06 | Results | Device retains final placement evidence until server acknowledgment; server recomputes score and deduplicates retries. |
| FR-07 | Leaderboard | Only players whose latest round is completed can access it; updates after committed results and shows nickname/code, best score and rank for their source cohort, without private identity/history. |
| FR-08 | Dashboard | Staff see machine freshness, queue, current round, session history, event metrics and read-only analytics. |
| FR-09 | Recovery | A running round survives Wi-Fi loss; uncertain assignments are reconciled before another ranked round. |
| FR-10 | Administration | Staff can skip absent players, abort with a reason, pause admissions and flag results; changes are authorized and audited. |
| FR-11 | AI analytics | Answer only from approved aggregate tools with event/time/ruleset scope, freshness and denominators. |
| FR-12 | Export | Admin exports event results without student IDs by default; any private export is a separate explicit admin action. |

Deferred: adaptive difficulty, rewards/payments, mobile remote gameplay, computer vision, physical block/collapse sensors, accounts with social login, predictive player profiling, cloud fleet management, automatic AI control and OTA firmware rollout. No energy, temperature or room-control data exists in this product.

## 2. Roles and access

| Actor | Access |
|---|---|
| Visitor | QR camera/upload entry; registration requires a valid detected-code entry grant. No dashboard or leaderboard access. |
| Player with private browser session | Own queue ticket, cancellation and result; leaderboard after the latest round completes. A public code grants no private access. |
| Operator | Dashboard, queue operations, start/abort requests, diagnostics and result review flags. Cannot reveal student IDs or edit rules. |
| Admin | Operator abilities plus staff/device provisioning, future rulesets, event settings, audited invalidation, private identity access and retention. |
| Device | Only its own command polling, acknowledgments, heartbeat and session events/results. |
| AI assistant | Staff-scoped, allowlisted read-only analytics tools; no direct database credential or device commands. |

No user can submit a ranked score through a public browser endpoint. Admin invalidation retains original results and evidence; direct score editing is excluded.

## 3. Gameplay contract — proposed `classic-v1`

These values are an initial reproducible game design. Validate playability on the actual panel before an event; publish any change as a new immutable ruleset.

| Parameter | Proposed value |
|---|---|
| Logical board | 8 columns, 12 scored rows; a foundation marker lies outside the scored rows |
| Foundation | 3 cells at x = 2, 3, 4 (zero-based coordinates) |
| First moving row | Width 3; initial left x = 0, direction right |
| Movement | Integer-cell steps, bouncing within `0..(8-width)`; each new row starts at x = 0 moving right |
| Step interval | At row L (1-based): `max(120, 350 - 20*(L-1))` milliseconds |
| Ready countdown | 3 seconds after readiness button press; presses during countdown are ignored |
| Round limit | 60,000 ms of active play, excluding countdown |
| Debounce | 30 ms stable edge, release before next accepted press; held button cannot lock multiple rows |
| Win | Successful placement of row 12 |
| Loss | Zero overlap or round deadline reached |
| Score | 100 per successful row plus 25 per perfect row; maximum 1,500 |

For support interval `[s, s+w)` and candidate `[x, x+w)`, calculate `left=max(s,x)`, `right=min(s+w,x+w)`, `overlap=max(0,right-left)`. A row is perfect when `overlap==w`. For a successful placement, the next support is `[left,right)` and next moving width is `overlap`. Failed attempts add no score. Highest completed level is the count of successful placements. Example: successful overlaps 3, 2, 2, then 0 produce 3 levels, 2 perfect rows and a score of 350.

Firmware captures button edges with the monotonic clock. Process events in timestamp order. A press timestamp strictly before the next scheduled movement uses the earlier position; at equality process movement first. A press at or after the 60,000 ms deadline is rejected and timeout wins. On successful row 12 strictly before deadline, win ends the round immediately. Failure row is stored only for a zero-overlap placement; timeout has no invented failed placement. Never convert missing telemetry into zero accuracy.

Placement accuracy is a game-derived overlap metric, not a sensor measurement of physical skill: `100 * SUM(overlap) / SUM(candidate_width)` over all recorded placement attempts, including zero-overlap attempts. It is null when no placements exist. Store numerator/denominator and show one decimal in the UI. Record perfect placement rate separately.

## 4. Journeys and state transitions

### Registration and turn assignment

1. QR includes a public event/machine code and URL, never a device credential or student ID. Phone must reach the event server; a QR pointing to `localhost` cannot work on a phone.
2. Enter student ID and nickname (2–24 visible characters). Trim ID outer whitespace; keep leading zeros and internal punctuation; validate against the institution's approved format. Until confirmed, accept 4–32 ASCII letters/digits/hyphens without assuming all IDs are numeric.
3. New identity creates a player and private session. Repeat submission in that same private session is idempotent. On a new browser, submitting an existing student ID does not grant the prior player's history or rename rights: require an operator-assisted recovery or the existing private recovery token. Use generic messages and rate limiting to reduce ID enumeration.
4. Join queue; show private ticket, position and a “wait near the cabinet” message. Queue position is a count ahead, not a guaranteed time.
5. Operator calls next player; backend reserves one session and sends a command. Display public code, not ID. Device acknowledges persistence of reservation; button starts countdown. Reservation expires after a proposed 45 seconds only if the device confirms it never started.
6. Assigned queue entry stays live until completion/abort. Retries and double taps must not create extra entries or sessions.

### Cabinet state machine

`BOOT → SELF_TEST → IDLE → RESERVED → COUNTDOWN → PLAYING → RESULT_PENDING → IDLE`

`FAULT` is entered for display/input/storage faults. `MAINTENANCE` prevents assignment. Server session states are `reserved`, `countdown`, `playing`, `awaiting_result`, `completed`, `expired`, `aborted`, `review`. Device states are observations; the server's validated persisted session is the reporting record.

- One ranked session occupies a machine from reservation through result acknowledgment or explicit reconciliation.
- Button before reservation only shows “Scan QR / wait for turn”; no anonymous ranked game.
- LED/audio feedback: countdown ticks, successful placement, perfect placement, miss, timeout and win. Sound may be muted; visual information remains complete.
- Completed game shows score/result for a proposed 5 seconds; a new reservation can arrive but cannot bypass the result screen or its reset readiness check.
- Abort commands carry command ID, session ID and expected revision. An in-play abort is queued for the game loop; it does not block rendering. If a completed result won the race, record abort as stale and preserve that result.
- Reset clears transient board state only after terminal evidence is persisted. A long press cannot erase a pending upload.

### Loss of connectivity and power

- After authorization and acknowledgment, a round may continue offline. Persist start marker before countdown and a complete terminal record before showing upload success.
- No new ranked reservation is accepted offline. A separate explicitly labeled practice mode is optional and never enters rankings.
- After 15 seconds without a 5-second heartbeat, show “connection stale” with last seen; preserve the machine lock. Do not infer that the game ended.
- On reboot, upload any completed record; if a start marker exists without terminal evidence, reconcile as interrupted/aborted, with no ranked score. Never silently restart the same session.
- A session with uncertain start is placed in review and holds the machine until the device reports its durable state or an operator performs a physical reset and audited reconciliation. Server restart reconstructs outstanding work from MySQL.
- Durable upload storage must hold at least one full terminal record. If it is full/corrupt, block further ranked play and show a storage fault.

## 5. Dashboard and metrics

Use [dashboard-design.md](dashboard-design.md) as the visual contract. Routes: `/register/:eventCode/:machineCode`, `/ticket`, `/leaderboard/:eventCode`, `/admin/overview`, `/admin/queue`, `/admin/sessions`, `/admin/machines`, `/admin/analytics`, `/admin/settings`.

Leaderboard uses one best valid completed round per player within the selected event and ruleset. Sort score descending, completed levels descending, duration ascending, completion time ascending, then session ID ascending. Show deterministic sequential ranks; label the tie-break rule. Never combine difficulty/ruleset versions into one competitive ranking by default.

Metric definitions:

- Completed games: valid completed win/loss sessions; exclude practice, aborted, expired, review and invalidated results.
- Players: distinct players among those completed games, not registration count.
- Win rate: wins / completed games; show `N/A` when denominator is zero.
- Level failure rate: zero-overlap failures at L / sessions with a recorded attempt at L. Report timeout separately; timeouts without an attempt are not failures at an invented row.
- Games today: completions from midnight to next midnight in Asia/Manila, converted to UTC bounds before querying.
- Live row/progress: device observation with timestamp and age. Never animate a fictitious round during disconnection.

## 6. Acceptance criteria and quality targets

Targets are proposed acceptance thresholds, not measured performance claims.

| ID | Scenario / pass condition |
|---|---|
| AC-01 | Student ID absent from public responses, QR, WebSocket payloads, browser persistence, analytics tool data and routine logs. Raw ID is not sent to an LLM. |
| AC-02 | 20 simultaneous calls/assignment retries create exactly one live session per machine and one live ticket per player/event. |
| AC-03 | The scoring example above returns 350 in firmware simulator and backend replay. Boundary tests cover bounce, narrowing, zero overlap and deadline ties. |
| AC-04 | Re-send identical final result 10 times: one completed session, one leaderboard contribution; a changed payload under the same ID is rejected/quarantined. |
| AC-05 | Disconnect Wi-Fi mid-round: gameplay remains responsive; reconnect commits that round once. Power loss with no final record becomes an interrupted round. |
| AC-06 | Unknown-start and unacknowledged-result machines cannot be automatically reassigned because a server timer elapsed. |
| AC-07 | Public leaderboard reflects committed results within 2 seconds p95 on the event LAN; reconnect refreshes a complete snapshot. |
| AC-08 | Button-to-visible-lock response within 50 ms p95, measured on hardware, independent of network calls. |
| AC-09 | Registration/API reads within 500 ms p95 on event LAN at 50 connected browser clients; AI calls excluded. |
| AC-10 | Every staff command checks role, current session/revision and produces a redacted audit record. Device credentials cannot access another machine. |
| AC-11 | 360 px mobile and 1440 px desktop views remain usable; keyboard navigation, visible focus, semantic labels, non-color status cues and reduced motion work. |
| AC-12 | AI fabricates no numbers in fixed evaluations; data absent, provider unavailable, malicious nicknames and forbidden control requests are handled per policy. |
| AC-13 | Backup restored into an isolated MariaDB instance matching XAMPP reproduces result counts and rankings; no private data enters exported public files. |
| AC-14 | 50 consecutive hardware rounds and a 2-hour mixed-load soak finish without a duplicate result, stuck lock or lost acknowledged result. |

## 7. Decisions still needed before hardware/event release

Confirm actual ESP32 and panel model/scan driver, power supply/current budget, pin map, student-ID format and operator identity recovery process. Play-test proposed rules and absence timeout. Confirm event LAN, stable hostname/certificate trust, AI provider/budget and identity retention owner. Baseline retention proposal is 30 days after event close for identity linkage and 90 days for redacted diagnostics; make these explicit settings and validate with the institution before collecting real IDs.


## Current quality hardening — 19 November 2026

The [audit](quality-audit.md) adds strict typed/UTF-8 input handling and a 64 KiB JSON body limit, configured-origin authorization, player-session rotation/revocation, prevention of signed-in identity switching, consistent cabinet readiness/review presentation, bounded requests and current readiness checks. A terminal win or zero-overlap loss must report duration equal to its final placement timestamp; a timeout retains the documented round limit. Numeric gameplay settings remain proposed until physical play-testing.
