# Cross-system quality audit

19 November 2026 · **Completed for the current local implementation.** Confirmed defects below are fixed and the named checks were executed. New roadmap features remain paused. This is a bounded audit, not proof that software is flawless or that every input, deployment or hardware failure is covered.

## Coverage ledger

| Area | Current evidence/status |
|---|---|
| Dependencies | Full npm audit of the final 219-dependency lockfile and pip-audit of pinned Python requirements found zero known advisories. Neither proves absence of vulnerabilities. |
| Auth, origin and identity | Reviewed cookie/CSRF/auth code and registration transactions. Fixed malformed non-ASCII CSRF 500s, Host-derived origin trust, signed-in identity switching and failure to revoke a rotated player cookie. New adversarial tests pass. |
| Request handling/readiness | Strict typed/UTF-8 inputs, forbidden unknown fields, 64 KiB declared/chunked limits, schema/migration/configuration readiness and bounded browser/database waits implemented and checked. |
| Game and queue | Replay, FIFO transactions, command receipt/start/result idempotency and shared cabinet state reviewed and tested, including review holds, disabled/maintenance and disabled simulator states. Hardware reconciliation remains unfinished. |
| Analytics and presentation | Shared AI/dashboard readiness, selected-source overview rankings, N/A denominators, accurate time labels/history order, nickname rules, safer CSV output and bounded pagination implemented. |
| Browser journey | Eight Edge tests passed: private access/registration, two-player queue, win/loss and unlocked leaderboard, all six admin pages in both themes, phone navigation and targeted axe scans. Open Sans Variable computed family checked. Current overview/settings screenshots visually inspected. |
| QR reliability | Reproduced valid-code failure in html5-qrcode; pinned local image API fallback fixes it. Twelve hostname/image-size patterns at 320/480/600 px, invalid images, synthetic camera decoding, denied permission and cancelled/late permission passed. Fallback worker is bundled. |
| React async state | Deadlines/cancellation, protocol validation, stale connection responses and Forget-versus-delayed-memory races checked. Existing revision/coalescing/reconnect tests remain passing. |
| NLP/data/privacy | Normalization, curated knowledge, semantic constraints, corpus split exclusion, owner-scoped memory/examples and read-only tools reviewed. 44 actual local Ollama regressions passed. No weights trained or live identities used. Unknown subjects clarify before data access. |
| Reliability and recovery | Actual forced API termination/restart, terminal deduplication, 50 independent browser contexts, 250 context reads and real XAMPP dump/restore into a second disposable database passed. Detailed method/limits below. |
| Operations and documentation | Portable runner, API-first test startup, preview target and readiness corrected; critical Python static checks, changed frontend formatting and documentation checks passed. Guides aligned; Graphify code/document refresh accompanies this audit. |

## Confirmed defects fixed

1. Non-ASCII CSRF header raised `TypeError` instead of 403.
2. Origin validation authorized request-supplied Host values rather than only configured origins.
3. A signed-in player could submit a different new identity and abandon their old live ticket.
4. Re-registration rotated a cookie without revoking the previous authenticated player session.
5. No bounded request-body parser limit; large JSON could be processed before validation.
6. Completed/missed rounds could report duration later than their terminal placement, corrupting duration metrics.
7. AI analytics could report a disabled/maintenance cabinet ready, contradicting the dashboard; disabled simulator observations could also appear ready.
8. Browser requests could stall refresh/form state indefinitely; invalid successful JSON could enter application state.
9. QR upload failed for a valid generated code because the primary decoder rejected its pattern.
10. Review-held players were omitted from active-ticket navigation/form guards.
11. Overview rankings silently mixed simulator/device results and claimed “today” while using all saved rounds.
12. Unattempted level ratios were shown as 0%; fixed dates and reversed round history misrepresented the saved data.
13. Browser checks depended on an obsolete Codex runtime path and did not cover Settings.
14. Malformed Unicode could reach hashing/database operations; invalid text, unknown fields and improperly typed flags now fail safely.
15. A `SELECT 1` health check claimed readiness despite missing migrations/configuration; required tables, migration filenames and initial configuration are now checked.
16. Delayed memory/status responses could restore forgotten context or replace a newer ready result; stale replies are now suppressed.
17. Vite preview ignored `STACK_API_TARGET`, potentially proxying a test preview to the normal API; development/preview now share the explicit target.
18. The documentation checker parsed `IF` as a table name, causing false duplicate errors; it now recognises `IF NOT EXISTS`. Candidate DDL points to authoritative installation migrations.
19. Browser/API nickname character rules differed. They now agree; CSV formula-prefix handling covers leading whitespace and pagination stays within current bounds. The existing level-comparison sample requirement is explained.
20. NLP rejected valid registration/points/queue wording and confused individual versus aggregate scores; semantic measure/operator families and public metric vocabulary now apply consistently.
21. Public student-ID protection questions were refused and architecture explanations could return cabinet metrics; curated explanations remain separate from identity disclosure/live observations.
22. Unknown subjects removed by sanitization could be replaced with event facts, demonstrated by an unrelated sports question. Such requests now clarify before model routing or analytics.
23. Curated knowledge described removed controls and omitted current settings/typeface/command behavior. It now reflects the UI; public-context fingerprints include metric definitions and stale examples require explicit re-review.

## Executed verification and reproduction

- **283 backend tests passed** against disposable MariaDB databases, including 70 regression cases added during this audit.
- **45 frontend tests passed**, including source separation, validation, review-held registration, unattempted ratios, API deadlines/cancellation and memory/status races.
- **8 real Edge tests passed**, including the 12 QR-image variations. Camera tests use synthetic streams; actual phones were not tested. Targeted axe scans are not accessibility certification.
- Production build, changed-file Prettier and critical Python checks (E9/F821/F822/F823) passed. Local Open Sans normal/italic fonts and QR fallback worker are bundled.
- Documentation links/fences and candidate DDL checks passed. The optional SQL parser is unavailable in the current Python environment; actual migrations were repeatedly executed on MariaDB. One upstream TestClient/HTTPX deprecation warning did not fail the suite.

Tests used generated disposable databases, synthetic identities and ports 8001/5174. Existing user API/Vite processes on 8000/5173 were preserved. No production records or private exports entered model context or graph inputs. Synthetic dumps were removed; detailed runtime artifacts/screenshots are ignored under `docs/ui-review/`.

See [backend quality commands](../backend/README.md#quality-checks--disposable-data-only). Checked-in runners are `backend/run_browser_tests.py`, `backend/check_assistant_quality.py` and `backend/check_quality.py`. The two server-owning exercises must run sequentially. The NLP runner exits unsuccessfully if a case fails; it does not train a model.

### NLP method and limits

The initial audit passed **19/28**. A separate 16-case follow-up initially passed **15/16** and exposed unrelated-domain substitution. After remediation, **44/44** cases pass on local `qwen3:4b-instruct`; these corrected cases are now **regressions**, not an independent estimate of general language accuracy. The 52 parametrized language/constraint tests cover wording families, contradictory history, deliberately wrong model labels, public explanations and disclosure attempts.

The fixes affect semantic routing/safety rather than canned answers to exact messages. Unknown subjects conservatively require clarification; not every paraphrase is understood. More independent English/Taglish and real-user evaluation remains useful. No weights were trained; synthetic dataset size is not proof of model improvement. Memory retains typed topics/preferences, never raw chat or old scores as current facts. Older reviewed examples can become stale after public-context changes and need explicit re-review.

### Loopback load and actual process restart

Latest local sample used the production frontend and 50 independent private browser contexts:

| Check | Observed result |
|---|---|
| Queue-state change across 50 browsers | All observed within **1,123 ms** of write initiation; zero browser script errors |
| 250 context reads, concurrency 20 | **224 ms p50**, **434 ms p95**, zero failed responses |
| API killed after result commit, dispatch deferred | Six pending outbox rows survived; browser recovered after restart |
| Result observed after restarted API became ready | **824 ms** in this sample |
| Identical terminal replay | Original acknowledgement; exactly one completed round and one notification |

UI observation includes HTTP completion, test IPC and locator waiting; it is not browser paint time or pure dispatcher latency. Request timings include client setup. This single-machine sample with background work is not an event-LAN benchmark or hardware SLA. Killing the owned test API intentionally produced connection-refused/reset proxy logs; subsequent browser recovery was checked.

### Synthetic restore

Real XAMPP `mysqldump`/`mysql` tools restored a generated database into a second uniquely named database. Counts matched for **all 23 tables**. A synthetic encrypted identity decrypted using the original test key; its private session/ticket restored, its **375-point** result remained and its authenticated leaderboard endpoint worked. Both databases and the dump were removed. Real operational recovery, protected key custody and larger-event ranking comparisons still need a separate rehearsal.

## Research used

- [OWASP CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html): trusted configured target origins and server-validated tokens; reflected proxy metadata must not become authorization.
- [OWASP sessions](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html): session rotation and invalidation.
- [OWASP LLM prompt injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html): tool-boundary permissions and typed parameters outside the model, least privilege and honest evaluation limits. Pattern lists and temperature zero are not proofs of robustness.
- [React effect guidance](https://react.dev/reference/react/useEffect): cleanup and suppression of stale asynchronous responses.
- [html5-qrcode API](https://scanapp.org/html5-qrcode-docs/docs/apis/classes/Html5Qrcode) and [Nimiq QR Scanner](https://github.com/nimiq/qr-scanner): local library APIs, image scanning and resource lifecycle. The fallback choice is supported by the reproduced image failure, not an assertion that either library decodes every image.
- [PyPA pip-audit](https://github.com/pypa/pip-audit): known Python vulnerability checks. Reports are local ignored artifacts; application data is not submitted.
- [Rasa evaluation guidance](https://legacy-docs-oss.rasa.com/docs/rasa/testing-your-assistant/): separate evaluation from training and inspect intent errors. Applied through independent probes followed by explicit regression classification; Rasa, cross-validation and fine-tuning were not introduced.

## Outstanding feature/release boundaries

ESP32 firmware/panel/power/button tests, trusted boot/session/terminal reconciliation and guarded release, separate staff capabilities, identity recovery/retention, actual phone TLS/WSS/background behavior and deployment validation remain named work. They are not silently marked complete by this audit. Local benchmark samples must be labelled loopback, not event-LAN acceptance.

Closed-tab push, prolonged mixed-load/hardware soak, operational restore/observability and physical event rehearsal also remain. Numeric game settings stay proposed until play-tested. New roadmap implementation remains paused after this audit, as instructed.
