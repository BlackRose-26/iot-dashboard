# Verified remaining work

Reviewed 19 November 2026 against the canonical plan, current route/service code, schema, frontend and executed synthetic checks. Graph relationships were used for navigation; they are not proof of live hardware. This is an implementation audit, not a declaration that all release acceptance criteria passed.

## Working software foundation

- React JavaScript/Vite, FastAPI and XAMPP/MariaDB startup, staff sessions and private QR camera/upload registration.
- Required private student identity, persistent FIFO tickets, transactional assignment, validated score replay and source-separated results.
- Neutral light/dark admin views, player registration/ticket/results, post-completion leaderboard, analytics and Settings.
- Local conversational Ollama routing, bounded read-only factual tools, private typed memory and reviewed routing examples. No model-weight fine-tuning has occurred.
- Durable event revisions/outbox, authenticated live invalidation channels, coherent snapshots, reconnect and polling fallback.
- [Device command delivery](device-command-delivery.md): repeated polling, durable idempotent receipts, receipt-required start, a file-journal emulator, command diagnostics and conservative review holds.

Current audit checks: **283 backend tests**, **45 frontend tests**, production build and **8 Edge browser tests** passed, including all six admin pages in both themes, private player journeys and QR/camera lifecycle. See [full audit and measured recovery/load evidence](quality-audit.md). Earlier milestone counts are historical, not additional tests to sum. Actual hardware is not connected.

## What remains

| Priority | Work | What the current implementation does not yet prove or provide |
|---|---|---|
| Next | Trusted device reconciliation and guarded operator resolution | Bind boot IDs, monotonic uptime, active-session/start/terminal markers and expected revisions; distinguish proven never-started from interrupted/terminal-pending state. Resolve review holds transactionally with audit evidence. Current holds intentionally do not release physical-device rounds. |
| Next | Reordered events and interrupted rounds | A terminal result before valid start, reboot during play, lost/contradictory terminal evidence and result receipt recovery need a complete protocol/emulator suite. Preserve original evidence and prevent duplicate ranking. |
| Hardware dependent | ESP32 local firmware and panel integration | Confirm board/panel/pins/power, implement button/debounce/game engine, rendering/audio, immutable rule fixtures and NVS journal; measure latency and playability. Numeric settings remain proposed. |
| Security/operations | Role separation | Staff session authentication exists, but distinct operator/admin capabilities and provisioning flows still need enforcement and tests. |
| Security/operations | Identity lifecycle | Staff-assisted lost-browser recovery, automated retention/anonymization, key rotation and audited exceptional identity operations remain incomplete. Student ID must never become a login secret or model input. |
| Release | Process failure and load | Actual process-kill recovery and 50 independent browser clients were exercised on loopback, with bounded API requests and no duplicated terminal result/notification. Event-LAN p95 targets, Wi-Fi contention and a prolonged mixed-load soak remain unrun. Keep one API worker until shared routing exists. |
| Release | Phone/network deployment | Trusted HTTPS/WSS and cookies on actual phones, camera/notification support, background throttling, firewall/router reachability and real event access checks remain. Closed-tab push is not implemented. |
| Release | Backups and observability | A synthetic XAMPP dump restored into a second disposable database with matching table counts, restored private ticket/result and usable leaderboard. Real operational restore procedures, protected key custody, lag alerting, retention and release packaging still require validation. Do not commit real dumps/exports. |
| AI quality | Held-out evaluation and optional actual fine-tuning | The audit includes 44 actual local-model regressions, language families, misleading histories and scope/privacy checks. Broader independent English/Taglish and real-user evaluations remain. Synthetic dataset volume and memory do not prove model improvement. Training/import/activation must remain a reviewed separate stage with held-out comparisons. |
| Final review | Accessibility and full event rehearsal | Targeted new-page checks passed; a complete current app keyboard/mobile/theme review and physical event rehearsal remain. Hardware telemetry is not implemented and must never be fabricated. |

The next safe software milestone is reconciliation evidence and emulator recovery tests, followed by guarded operator resolution. Firmware work can share the resulting contract when hardware arrives. Remaining release targets stay open until their named checks actually run.

## Audit stop boundary

The current user-authorized audit fixes existing implementation defects. New roadmap milestones remain paused, including trusted device reconciliation, guarded review release, ESP32 firmware, retention and role separation. Auto-continue applies within the authorized audit, and stops when it is complete. These named feature/release gaps are not silently marked done.
