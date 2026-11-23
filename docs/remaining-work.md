# Verified remaining work

**Latest hosting choice, 22 November:** the user selected the free [PC/XAMPP + HTTPS tunnel](free-online.md). Local/public HTTPS health returned 200 and the private configured image compiled. Next verify that image in Wokwi and its authenticated heartbeat/game journey. Paid Render activation is superseded; its files remain an inactive alternative. Physical and operational gates below remain open.

**Current connection blocker:** actual browser testing loaded the private firmware. Core 4.0.0 hit the TLS watchdog; the compatibility build and network scheduling/reuse fixes compile and boot, but Wokwi repeatedly fails to connect to `wss://netwi.wokwi.com/`. No authenticated fresh heartbeat or connected round was observed. Retest when the public gateway connects; the dashboard remains online. See [evidence and retry instructions](free-online.md).

## NLP admission repair — 24 November 2026

See [the repair](nlp-admission-repair.md): lexicon v2 and admission changes; development admission 99/120 → 112/120 with off-topic holds kept; consumed replay 135/325 → 191/325 (unsupported false acceptances 1 → 3); 457 backend tests passed. Open: fresh independently reviewed test set, wrong-topic answers and generic system replies.

## Physical cabinet preparation — 23 November 2026

Network choice: phone hotspot, ESP32 through the HTTPS tunnel, players on their own mobile data. Software preparation is done: wiring self-test build, `npm run online:device` NVS-preserving USB upload, hotspot name/password validation, Wi-Fi/time serial diagnostics and the ordered gates in [physical bring-up](hardware-bringup.md). Self-test and game builds compiled and the flash-layout check refused an NVS-overlapping write. Open: every physical gate in that guide (self-test stages, Wi-Fi/heartbeat, first assigned round, power loss, hotspot drop, data use). Since 24 November the launcher sends each new Quick Tunnel hostname to the cabinet over USB (no reflash); the registration QR still changes per restart unless a stable named tunnel is adopted.

## Current ESP32/online integration — 22 November 2026

The user resumed hardware integration using [their Wokwi project](https://wokwi.com/projects/481390138161170433), confirmed physical-button play with online queue/dashboard and selected the sketch's 16×15 one-point rules. The current hosting choice is the free PC/XAMPP tunnel. [The integration guide](esp32-online.md) records the firmware, migration 006, ruleset-bound validation, frontend changes and optional inactive Render files. Classic records are preserved and excluded from Matrix rankings. Public HTTPS health, administrator login, secure cookies, origin rejection and authenticated revision-only WebSockets passed. A real Wokwi heartbeat remains required before calling a player to the cabinet.

Final firmware compilation and local Matrix device/API checks passed. Remaining immediate gates: run the connected version in the user's Wokwi project with a reachable backend, authorize/create the selected Render services, supply private deployment values, validate Docker/MariaDB startup and backup/restore, set HTTPS QR origin and verify phone registration → queue → physical-button simulation → validated result/notification/leaderboard. The existing linked standalone simulation can boot and time out, but Wi-Fi is disabled there; this is not connected-device evidence. Actual ESP32/NVS, brownout, electrical/audio and event load gates remain open. Do not treat local tests as deployed or physical success.

The [new 325-case holdout](nlp-evaluation/holdout-v1.md) exposes a major NLP language-coverage gap: 59/325 accepted matches and 247 valid-request clarifications. Improve on separate development material and reserve fresh independently reviewed cases for the next unseen evaluation; do not add frozen test prompts to training/few-shot data.

The [language pipeline repair](nlp-routing-repair.md) implements common grammar/concept projection, better English/Taglish semantic hints, and explicit read-only answers without waiting for Ollama. A retained-set regression does not close the independent-language-quality gate. Remaining unknown wording and independently adjudicated real-user accuracy stay open; no autonomous fine-tuning or test-prompt transplantation is authorized.

**Current NLP gate remains open:** filtered public vocabulary and topical checking improved the consumed 325-case score to 135/325 (41.54%), but 135 valid questions were clarified and one unsupported case was accepted. Follow-up, level/definition interpretation and unfamiliar-language coverage remain weak. Keep all recorded failures; do not claim 34/34 visible development probes establish general correctness. Next quality work requires independent adjudication and fresh held-out families, with the public lexical asset included in predictor freezing.

**Offline experiment completed:** [comparison and audit](nlp-offline-experiment.md) trained SetFit in an isolated environment and compared five candidates. On 130 developer-labelled development questions, the current router and frozen E5 got 63 primary topics correct; SetFit got 61. Adding unrelated history made SetFit call 73/120 explicit non-follow-up questions follow-ups. No model was promoted. Next: reviewed rare-class and matched topic-change/follow-up training families, then separate development validation. The [325-case candidate collection](nlp-evaluation/candidate-v2-preparation.md) is now filled with AI-authored questions and proposed labels; human review and a frozen final evaluation remain open.

**Follow-on completed:** [history augmentation and question-only ablation](nlp-evaluation/history-lab-20261120.md) reduced the reused E5 context-stress failure (14→47 primary matches out of 120 with augmentation), but ordinary matches fell 63→61/130. Question-only routing is invariant to unrelated history yet remains inadequate. Forty supported development inputs are blocked before classification. Next NLP design work must review privacy/control checks separately from unfamiliar wording and scope, alongside genuinely reviewed rare-class/follow-up families. Do not keep tuning against these consumed diagnostics or deploy these candidates. Fourteen offline checks passed at that milestone. The candidate packet is now filled and overlap-audited, with independent review still pending.

Reviewed 20 November 2026. The user resumed roadmap development; prepare the next progress report only when requested. Graph relationships are navigation evidence, not proof of live hardware. This list does not declare all release acceptance criteria passed.

## Working software foundation

The [20 November NLP improvement](nlp-evaluation/README.md) records measured local routing gains and the remaining overall-accuracy/level-topic confusion. It adds contrastive examples and regression coverage; independent real-user evaluation and actual fine-tuning remain open gates.

- React JavaScript/Vite, FastAPI and XAMPP/MariaDB startup, staff sessions and private QR camera/upload registration.
- Required private student identity, persistent FIFO tickets, transactional assignment, validated score replay and source-separated results.
- Neutral light/dark admin views, player registration/ticket/results, post-completion leaderboard, analytics and Settings.
- Local conversational Ollama routing, bounded read-only factual tools, private typed memory and reviewed routing examples. The live Ollama model has not been fine-tuned. Separate offline SetFit encoder training has occurred without production activation; see the experiment above.
- Durable event revisions/outbox, authenticated live invalidation channels, coherent snapshots, reconnect and polling fallback.
- [Device command delivery](device-command-delivery.md): repeated polling, durable idempotent receipts, receipt-required start, a file-journal emulator, command diagnostics and conservative review holds.

Current audit checks: **283 backend tests**, **45 frontend tests**, production build and **8 Edge browser tests** passed, including all six admin pages in both themes, private player journeys and QR/camera lifecycle. See [full audit and measured recovery/load evidence](quality-audit.md). Earlier milestone counts are historical, not additional tests to sum. Actual hardware is not connected.

## What remains

| Priority | Work | What the current implementation does not yet prove or provide |
|---|---|---|
| Software implemented; hardware gate open | Trusted device reconciliation and guarded operator resolution | Boot lineage, monotonic journal sequences, accepted/start/terminal bindings, permanent fences, guarded no-score release/void and validated result recovery now exist. See [protocol and operator workflow](device-recovery.md). Actual ESP32 persistence and power loss remain unverified. |
| Software implemented; hardware gate open | Reordered events and interrupted rounds | Exact journal retries, missing-start/reboot terminal review, immutable start/result evidence, conservative conflict quarantine and persistent emulator receipt recovery are implemented. Run the same fixtures against firmware/NVS when hardware arrives; quarantined conflicts deliberately remain held for investigation. |
| Hardware dependent | ESP32 local firmware and panel integration | Confirm board/panel/pins/power, implement button/debounce/game engine, rendering/audio, immutable rule fixtures and NVS journal; measure latency and playability. Numeric settings remain proposed. |
| Security/operations | Role separation | Staff session authentication exists, but distinct operator/admin capabilities and provisioning flows still need enforcement and tests. |
| Security/operations | Identity lifecycle | Staff-assisted lost-browser recovery, automated retention/anonymization, key rotation and audited exceptional identity operations remain incomplete. Student ID must never become a login secret or model input. |
| Release | Process failure and load | Actual process-kill recovery and 50 independent browser clients were exercised on loopback, with bounded API requests and no duplicated terminal result/notification. Event-LAN p95 targets, Wi-Fi contention and a prolonged mixed-load soak remain unrun. Keep one API worker until shared routing exists. |
| Release | Phone/network deployment | Trusted HTTPS/WSS and cookies on actual phones, camera/notification support, background throttling, firewall/router reachability and real event access checks remain. Closed-tab push is not implemented. |
| Release | Backups and observability | A synthetic XAMPP dump restored into a second disposable database with matching table counts, restored private ticket/result and usable leaderboard. Real operational restore procedures, protected key custody, lag alerting, retention and release packaging still require validation. Do not commit real dumps/exports. |
| AI quality | Held-out evaluation and optional actual fine-tuning | The audit includes 44 actual local-model regressions, language families, misleading histories and scope/privacy checks. Broader independent English/Taglish and real-user evaluations remain. Synthetic dataset volume and memory do not prove model improvement. Training/import/activation must remain a reviewed separate stage with held-out comparisons. |
| Final review | Accessibility and full event rehearsal | Targeted new-page checks passed; a complete current app keyboard/mobile/theme review and physical event rehearsal remain. Hardware telemetry is not implemented and must never be fabricated. |

Firmware can now use the boot/journal/fence contract when hardware arrives. The next independent software priority is enforcing distinct operator/admin permissions and documenting safe provisioning. Identity lifecycle and release gates remain open until their named checks actually run.

## Resume boundary

The user explicitly resumed development on 20 November. Auto-continue applies to ready roadmap tasks. Do not generate the next progress report until asked. Hardware-dependent work remains blocked on the actual ESP32/panel rather than being simulated and declared complete.
