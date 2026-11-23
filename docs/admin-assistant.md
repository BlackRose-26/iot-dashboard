# Stack Intelligence — local administrator analytics

**Current language repair:** [linguistic projection and explicit semantic routing](nlp-routing-repair.md) now handle common contractions, public English/Taglish synonyms and question grammar. Familiar explicit metrics and system explanations do not wait for model inference; broader wording uses the separate topical check and router. Unknown subjects, privacy/action guards and schema-validated facts remain enforced. This supersedes older statements that every analytical question requires a ready model; the assistant-enabled switch still applies. A fresh independent evaluation is still needed for the repaired predictor.

The final v11 pipeline adds filtered WordNet/Tagalog word forms and separate topical input checking for broader wording. Its preserved 325-case **regression** scored **135/325 (41.54%)**, with 135 valid clarifications and one incorrectly accepted unsupported question. Backend checks passed 406 tests; visible development probes passed 34/34. These do not close the broader reliability gate or replace the original first-use result.

**Broader evaluation:** the [325-case first-use synthetic holdout](nlp-evaluation/holdout-v1.md), kept outside runtime examples, measured 59/325 accepted intent/context matches. Vocabulary/scope gates clarified 247 valid requests. This exposes limited novel-language coverage; the older high small-set scores below remain development regressions. The frozen predictor was not repaired using the new test prompts.

**Routing improvement, 20 November 2026:** [measured changes and evidence](nlp-evaluation/README.md) add 42 contrastive routing examples, semantic kind-constrained Ollama output, English/Taglish retrieval and consistent learning labels. Actual runs improved the reused 21-case set from 12 to 21 correct and the synthetic validation set from 14 to 23 of 24. These are development measurements, not independent real-user/factual-answer accuracy. The model weights remain unchanged; old private approvals require re-review under the new context fingerprint.

18 November 2026 · Grounded conversation and private structured memory implemented; local Ollama installation and model download completed on this development PC. Targeted unit, local-model and disposable browser validation completed; broader release acceptance remains pending.

## Current behavior

The existing bottom-fixed chat is connected to authenticated FastAPI endpoints and uses a conversational, brief-answer default. It accepts English and Taglish, interprets questions with local Ollama, and renders numerical answers from backend templates. The model never calculates metrics, writes SQL, receives database rows or writes answer prose. Chat automatically uses the full event period and checks both simulator and physical-device results; there are no Period or Results selectors. The Analytics page retains its chart filters and uses the same per-source calculation service. Overview totals retain their existing all-source meaning; compare only identical scopes.

The ESP32 is not required for this feature. Queue and saved simulator results can be analyzed without hardware. No physical connectivity is implied by simulator readiness, an old timestamp, or a configured cabinet. Recorded physical heartbeat age, Wi-Fi signal and firmware are reported only when available. Temperature, power use, physical tower stability, forecasting and player personality assessment are unsupported.

## Automatic context (18 November 2026)

Ask directly: “How many players registered?”, “What is the win rate?”, or “What about yesterday?”. The assistant selects relevant allowlisted tools from the question, with access to all supported system domains. It does not require a manual context choice or send the entire database to Ollama.

Both result cohorts are read in one read-only repeatable-read transaction, using one as-of time and identical millisecond window bounds. Registrations and deduplicated completed-player/round counts can be event-wide. Competitive rates, score averages, overlap accuracy, trends and leaderboards remain separate, explicitly labelled **Simulator** and **Physical device**. Empty physical results are stated as missing records, never inferred from simulator readiness. Each cohort has its own snapshot reference and metric scope, with source-labelled details in chat evidence. An unavailable cohort query fails the answer honestly rather than silently returning an incomplete all-source result.

Synthetic MariaDB tests verify default scope, natural-language narrowing, follow-up inheritance, deduplicated player counts, per-source rates/rankings, registration-only answers, and missing physical results. These do not prove live hardware connectivity. Desktop Computer Use stopped before visual validation because it could not reliably identify the current browser URL; visual validation of this change remains unconfirmed.

## Local development installation record

On 17 November 2026, user-authorized setup installed **Ollama 0.40.16** using WinGet (installer hash verified) and successfully pulled **qwen3:4b-instruct**. The model is stored in the current Windows user's standard Ollama model directory; it is not included in Git or Graphify. The local server listens on **127.0.0.1:11434**. Cloud features are disabled with `disable_ollama_cloud: true` in the private Ollama server configuration and user environment `OLLAMA_NO_CLOUD=1`; Ollama was restarted after configuration. No cloud account or API key was configured.

The initial installation was observed without inference. Subsequent user-authorized timeout investigation exercised local inference and a disposable synthetic application/database, as recorded below; this does not establish full release readiness. Open a new terminal application if the newly installed `ollama` command is not yet on its inherited PATH.

## Setup on another computer (performed manually)

1. Install the Windows application from [Ollama](https://ollama.com/download/windows), then open Ollama. It serves a local API; do not expose that service to carnival Wi-Fi.
2. In a new terminal run:

```powershell
ollama pull qwen3:4b-instruct
```

3. Start MySQL in XAMPP and use the existing `npm run dev` command. If servers were already running, restart them to load backend configuration changes.
4. Sign in and open Stack Intelligence. Opening the panel automatically prepares the installed model; wait for **Local model ready**, then send a question. Use **Check connection** to retry preparation after a failure. A missing model, stopped Ollama or disabled service is displayed clearly. The application does not download or start Ollama automatically.

Existing backend installations use these defaults without editing private configuration:

```dotenv
STACK_AI_ENABLED=true
STACK_OLLAMA_URL=http://127.0.0.1:11434
STACK_OLLAMA_MODEL=qwen3:4b-instruct
```

Only a loopback HTTP endpoint is accepted. Redirects, credential-bearing URLs and cloud model names are rejected; environment proxy configuration is ignored. The model tag must match the installed name. No external API key is needed. Cold preparation took about 59 seconds on this development PC; allow up to two minutes. Performance varies by computer. An unavailable model never blocks normal startup, authentication, charts, queues or gameplay.

## Data and NLP architecture

Question → admin session/CSRF checks → local privacy/action guard → approved-vocabulary normalization → Ollama JSON intent → schema/enum validation → fixed read-only MariaDB analytics → bilingual factual templates and evidence.

Only approved English/Taglish system/analytics vocabulary, validated previous context, bounded level/top numbers and typed private-memory hints reach Ollama. The vocabulary includes words from reviewed public system cards, never private files. Names, arbitrary identifiers, URLs, email addresses, credentials, long numbers, raw chat history and unknown tokens are not forwarded. This intentionally narrows v1 paraphrase coverage: unsupported/ambiguous questions ask for clarification. The backend refuses identity and game-control requests before inference. Numeric thresholds and arbitrary calendar dates are not supported; ask for a named period in the message instead.

Ollama returns one required topic from a strict schema, plus optional curated definition, system-knowledge or social-response selectors. The backend maps the topic to relevant allowlisted analytics operations, never SQL or commands. General overview uses summary/queue/cabinet; simple queue questions use the queue operation; queue diagnosis can also inspect cabinet observations, rather than returning every metric. Supported filters and bilingual template selection come from normalized input, not model-generated values. Fixed Taglish meaning hints help the local classifier. Follow-ups carry only validated tool/filter/language context. Supported periods are `event_to_date`, `today`, `yesterday`, `last_7_days`; chat sources are `all` (default), `simulator` and `device`. A supported period/source explicitly requested in the question narrows the answer. Follow-ups inherit the preceding scope unless the message changes it; a new unqualified subject resets to event-to-date and all sources. Saved older simulator-only context does not silently narrow a new subject. The actual scope is shown in answer evidence. Event and ruleset are fixed server-side to the initial event and Classic v1.

Defaults: event-to-date, all available result sources, automatic English/Taglish templates; one inference at a time, ten questions/minute/staff account, 1,000 characters/question. Model calls use temperature zero, 4,096-token context, 256 output tokens, no streaming, `think: false` and thirty-minute model keep-alive. Preparation uses a separate background 120-second deadline and the inference gate. It primes model loading, first-inference GPU kernels and the common prompt with a fixed non-user metric-definition request; it does not query the database or submit the draft. Readiness requires both a running 4,096-context model and successful calibration in this API process. Eviction requires preparation again. The query handler has one 20-second deadline covering authentication and analysis, with no automatic retries. Metadata writes are queued and never awaited by the answer. Cancellation closes the client request and cancels the model operation; an already-running SQL worker may finish its bounded read-only queries. No game action occurs in either case. Rate limits are in-process and reset on API restart; keep the existing single API worker.

## Metric definitions

- Only completed, non-invalidated sessions in the selected event, ruleset, result source and half-open UTC window count toward competitive metrics. Proposed Classic v1 scoring remains unchanged.
- Registrations count each player's first event queue entry in the chosen window, across sources. All-source completed players are deduplicated across both result sources. Each source also has its own distinct completed-player count; those counts must not be added together. They are separate measures.
- Win rate is wins/completed rounds. Accuracy pools retained cells/attempted width. Missing denominators produce N/A, not zero. Duration and score averages use qualifying completed rounds.
- Leaderboards take one best result per player, then apply score descending, level descending, duration ascending, completion ascending, session UUID ascending. Only public player codes are returned; nicknames and identity records are not queried.
- Level failures are zero-overlap placements. Timeouts are separate. Fewer than 20 attempts receives a small-sample caveat; failure rates do not establish causes.
- Trends use hourly buckets when they fit within 168 buckets, otherwise daily buckets capped at 168. A truncated trend declares its narrower window. Do not sum per-bucket distinct players into a whole-window unique count.
- Queue and cabinet observations are current event-wide state, independent of a historical result window/source. Oldest waiting time is elapsed time, not a prediction of how soon a player will start.

Analytics use a repeatable-read snapshot and a next-transaction READ ONLY mode. Each fixed query has a two-second MariaDB statement limit. No identity-table access, unbounded result rows or dynamically generated SQL is permitted. Analytics itself needs no new table; private structured memory requires migration `003_assistant_memory.sql`. The existing `ai_requests` table records safe policy/model, source/window/level, operation names, status, token counts and latency through a separate best-effort metadata worker. Its queue is capped at 32 jobs; overflow or shutdown can omit metadata rather than delaying the answer. Each audit statement is time-bounded, and the worker is cancelled during application shutdown. Raw questions and responses are not logged or stored.

## API and UI contract

- `GET /api/admin/assistant/status`: authenticated availability/configuration metadata, without loading a model or modifying gameplay. Distinguishes installed, loaded, ready, warming, failed preparation and unavailable.
- `POST /api/admin/assistant/prepare`: admin session and CSRF required; starts one background calibration and promptly returns preparation state. Repeated calls reuse an active task. The UI polls status every 1.5 seconds while warming; greetings and other supported social exchanges remain sendable while loading. Analytical requests made before readiness receive an honest loading response and preserve the draft.
- `GET /api/admin/analytics?period=event_to_date&source=simulator`: authenticated deterministic analytics, independent of Ollama. Returns scope, as-of time, snapshot ID, grouped metrics and caveats.
- `POST /api/admin/assistant/query`: authenticated and CSRF-protected; strict request with `question`, optional typed `previous` and `use_memory` (default true). The UI sends no period/source selectors. Optional API `period`/`source` fields remain schema-validated for compatibility, with defaults `event_to_date`/`all`. See [request example](../contracts/assistant-query.example.json).
- `GET /api/admin/assistant/memory`: authenticated, current-admin-only structured context/preferences and availability; it accepts no target user ID.
- `DELETE /api/admin/assistant/memory`: session and CSRF required; forgets this admin’s saved context/preferences and advances a revision tombstone.
- Answers contain `status` (`conversation`, `ok`, `no_data`, `needs_clarification`, `refused`, `unavailable`), plain `answer`, `claims` and metric references, `scope`, `scope_label`, `as_of`, `caveats`, `source_snapshots`, `evidence`, per-metric `metric_scopes`, and validated next `context`. Errors without evidence never invent an as-of snapshot. Authentication/validation/rate failures use standard HTTP errors.

The neutral light/dark panel remains admin-only, nonmodal and keyboard accessible, with Font Awesome webfonts. It preserves drafts on errors/cancellation and supports source/time selectors, connection checks, clarification and explicit retry. Up to 20 messages remain in component memory. Refresh/sign-out removes history; raw history is not saved in browser storage or a message table. Private typed context/preferences can persist in `ai_admin_memory` when memory is enabled; this is distinct from raw chat history. Clearing chat cancels the request and ignores late responses. Minimize preserves the in-flight question; leaving the admin shell cancels it.

## Reviewed examples for later fine-tuning — 18 November 2026

The user selected memory **plus reviewed fine-tuning examples**. The [review/export workflow](assistant-training.md) is now implemented: choose **Review for training** after an eligible reply, inspect/correct the sanitized input and label, save pending, explicitly approve, then export only approved current-version JSONL. This teaches the intent classifier; no raw chat, answer prose or live game facts are retained. Each admin owns a private queue, with revisions, context-version gating, rejection/removal and bounded exports. Memory-off/Forget remain separate from explicit training-example selection. Migration 004 was applied locally. The full backend suite passed 100 tests (14 new workflow checks), production build and synthetic browser review/download flow passed. No model was trained, imported, activated or uploaded. See the guide for endpoints, data shape, privacy constraints, official format/import references and later training gates.

## System-grounded conversation and private memory — 18 November 2026

Questions no longer need to match fixed social phrases or metric requests. Local Ollama can interpret flexible English/Taglish phrasing about gameplay, QR registration, queue workflow, dashboard/chart meanings, architecture, privacy, results, service limits and the assistant itself. Answers stay strictly within the reviewed public cards in `backend/app/assistant_knowledge.py` or validated analytics. The model selects a schema-bounded topic/card/social act; it still writes no free factual prose and receives no player rows. System-guide replies show their source title. Ordinary exact greetings keep their fast local path while Ollama is loading. Ambiguous or unrelated subjects ask for clarification; stripped unknown words must not silently turn an unrelated question into event statistics. Explicit current subjects override older context.

**Memory improves continuity, not model weights.** Each admin can retain a validated current topic, the last six typed topic/filter contexts, and language/answer-length preferences across logins/API restarts. No raw questions, model answers, names, student IDs, credentials, private tokens, game counts, scores or telemetry are saved in memory or fed back as historical facts. Only allowed enums, source/period selectors, bounded level/top values and booleans are retained. Current numerical questions always reread analytics. Persistent memory is never a trusted instruction source or a way to broaden event/role access. This memory implementation does not fine-tune Ollama or silently train on conversations. The later explicit reviewed-example workflow below can export approved sanitized routing examples, separately from memory.

The UI has **Use private memory** and **Forget saved memory**. Off disables persisted-memory reads/writes for that chat; current-chat typed follow-ups still work. Forget clears visible chat and saved subject/preferences. Clear conversation alone clears visible messages but leaves approved saved memory available. The displayed counter counts saved context updates, not unique retained topics or model-training steps. Requests such as “Please reply in Taglish from now on” and “Keep your answers short” set validated preferences. Wider phrasing uses local topic understanding; it is not unrestricted general-purpose chat.

Storage uses `ai_admin_memory` keyed only by authenticated `staff_user_id`, strict JSON validation, a six-context cap, a bounded JSON read and time-limited fixed SQL. Optimistic revisions prevent older concurrent responses from overwriting newer state; forgetting retains only an empty revision tombstone so an in-flight reply cannot revive forgotten context. A memory failure is shown honestly while ordinary chat can continue. SQL setup remains authoritative in `backend/migrations`; apply existing setup on another machine with `.\backend\.venv\Scripts\python.exe .\backend\setup_local.py` from the project root. The additive migration was applied on this development PC without reading/changing existing player/game records.

Validation: **86 full backend tests passed**, including **75 targeted assistant/memory checks** with disposable MariaDB flows for persistence through a fresh API instance, admin isolation, memory-off, session/CSRF protection, strict JSON rejection and stale-write prevention after forgetting. The Vite production build and changed-file formatting passed. An existing FastAPI/Starlette TestClient dependency deprecation warning remains; no package upgrade was made. Computer-use checks with synthetic data confirmed flexible entry questions, Taglish preference, page-refresh follow-up recovery, current-topic override (XAMPP after registration), memory off, forgetting, unrelated-subject clarification, fresh analytics after a system discussion and the memory explanation. The first entry-question misroute was corrected using explicit reviewed-subject hints before repeating the browser check. Temporary databases/processes were removed. Screenshot: ignored `docs/ui-review/assistant-private-memory.jpg`.

Broader language/model evaluation, account/session abuse tests under load, retention policy beyond user-controlled forgetting, and physical ESP32 integration remain open release work. Reviewed knowledge cards need maintenance when the implemented system changes; arbitrary documents, private configuration and chat claims are never ingested automatically.

## Conversational interaction — 17 November 2026

The default is a short conversation, not a metric report. Complete English/Taglish greetings, thanks, acknowledgements, introductions, help requests and farewells receive curated local replies. For example, `hello` returns “Hi! I'm Stack Intelligence. What would you like to know about your event?” These social turns require the normal admin session/CSRF checks and rate limit, but no Ollama inference or analytics read. They remain usable during model preparation or when inference is disabled. No factual snapshot, numerical claims or fabricated evidence is attached; their response status is `conversation`. Best-effort metadata is still recorded without raw text.

Social matches must cover the complete utterance. Mixed messages such as “Hello, how many players registered?” continue into analytics; greeting-prefixed identity/control requests still meet the privacy/action guard. Casual turns preserve the previous validated analytical topic and filters, so “thanks” followed by “What about yesterday?” continues that topic. Raw conversation history is never forwarded.

For factual answers, typed `context.metrics` selects approved summary measures and `context.detailed` permits an explicitly requested full breakdown. Asking about registrations returns registrations; asking about average score returns that average without a distribution report. Summary counts distinguish all-source registrations from the chosen completed-result cohort. Ordinary queue questions do not automatically include cabinet telemetry. Every factual response retains backend-generated claims, actual scope, source evidence and caveats. The UI shows scope and keeps the longer values/caveats in the expandable **Details & sources** panel. Existing detailed analytics remain available there, and explicit report/breakdown requests can use the fuller templates.

Validation for this update: **63 assistant unit checks passed** and the Vite production build passed. Computer-use checks with a disposable two-round MariaDB fixture confirmed hello during loading, English/Taglish greetings, a brief registration answer, thanks with a preserved yesterday follow-up, a one-sentence average score, and expandable evidence. The fixture was removed after testing; no real player data or physical ESP32 was used. Screenshot: ignored local `docs/ui-review/assistant-conversation.jpg`. These targeted checks extend, rather than replace, the remaining acceptance gates below.

## Source-review corrections — 17 November 2026

Five review findings were corrected in source; these are not runtime verification results:

- One query deadline covers authentication and inference/analytics. Metadata logging no longer delays the response; cancellable thread futures prevent completed answers from waiting on slow database workers.
- Only explicit supported seven-day phrases map to `last_7_days`. Hours/minutes, other day counts, month/year windows and ambiguous calendar-week requests ask for clarification instead of becoming a different period. English today/yesterday and Taglish `ngayong araw`/`kahapon` remain supported.
- Every level now includes pooled retained/attempted-cell accuracy, with N/A for no attempted width. The global scope is never labelled as a single level. Only placement metrics receive the selected level in `metric_scopes`; summary values remain explicitly whole-cohort and have a scope caveat when shown together.
- Empty scores, rankings, levels or trends are assessed using their qualifying result data. Event-wide registrations cannot make an empty selected result cohort appear available. A registration-only summary can still report registrations without completed games.
- Changing either selector clears saved retry/context state. A retry for an old source/window is no longer offered after a filter change; the new draft must be submitted with the current filters.

The targeted checks below now cover these fixes; remaining manual release cases are still open.

## Remaining manual acceptance

Use [prepared English/Taglish cases](../contracts/assistant-review-cases.json) and synthetic/disposable data only. Targeted unit checks in `backend/tests/test_assistant.py` have been run. The broader acceptance cases below are not all complete.

1. Compare equivalent English/Taglish questions and follow-up “What about yesterday?” / “Paano naman kahapon?”. Confirm visible source/window changes and no arbitrary event selection.
2. Use the synthetic two-round fixture definition: one simulator win and one timeout from one player, plus a separate device result. Confirm 2 games, 1 completed player, 50% simulator win rate; device scores must not enter simulator totals.
3. Select an empty window/source; verify N/A averages/rates, no fake top player, and clarification for unsupported questions. Check ties, zero attempted width, small level samples and distinct-player bucket caveats.
4. Compare the Analytics page and chat with identical filters. Review timestamps and evidence, and confirm current queue observations are not labelled historical.
5. Without physical hardware, check simulator labels and unknown/stale physical telemetry. Ask about temperature and confirm no measurement is invented.
6. Check signed-out/player access, expired sessions, missing CSRF, extra request fields, private IDs/credentials, injected instructions and attempted game controls. Never use real student IDs in manual prompts or screenshots.
7. Stop Ollama or choose a missing model; confirm unavailable/retry states, no startup failure and ordinary app functions still working. Review malformed model output, timeouts, rate limit, busy state, clear/cancel and late-response handling.
8. Check keyboard/focus, narrow screens, both themes, draft preservation, sign-out and refresh removing chat history. Confirm no transcript is written to storage/logs.

## Timeout investigation and targeted validation — 17 November 2026

The user authorized testing, including computer use, after seeing the timeout. The original 18-second model call / 20-second question deadline cancelled cold loading before it completed. A direct cold preparation took 58.77 seconds; first-inference GPU preparation also needed warming. Ollama reported qwen3:4b-instruct on the RTX 2060, 100% GPU with 4,096 context. Keep cold preparation separate from the ordinary question deadline; do not simply make every chat request wait two minutes.

Observed checks (synthetic data only):

- **38 assistant unit checks passed**: privacy/action guards, unsupported windows, canonical topic/tool mapping, Taglish hints, safe follow-ups, evidence and scoped metrics, no-data behavior, bounded metadata, single background preparation, failure/retry, preparation timeout/gate release and eviction readiness.
- **Vite production build passed**.
- Direct warm local inference classified English player totals, Taglish queue, level failures and accuracy definitions correctly, taking approximately **0.15–0.72 seconds** per checked routing call. These are sample model-call timings, not an end-to-end latency guarantee or comprehensive language evaluation.
- Computer-use browser checks passed: automatic loading-to-ready state, retained draft, English totals, focused Taglish queue answer, yesterday follow-up, empty device score cohort (N/A, without invented results), private-ID refusal, and unsupported hourly-range clarification. Refusals/clarifications/no-data now have distinct labels instead of being called verified facts. Refusals/clarifications do not offer an unchanged retry.
- Browser fixture: two fake public players, one simulator win (1,500 points) and one simulator zero-overlap loss (375 points). Expected/observed: two rounds, two completed players, 50% win rate, 937.5 average score and 93.8% pooled accuracy. These differ deliberately from the prospective timeout fixture above.
- Preparation API boundaries observed: **401** without a session and **403** with a session but no CSRF token.
- Each browser run used a uniquely named disposable XAMPP/MariaDB database and dedicated API/Vite ports. Test processes were stopped and the temporary databases removed. No real player database, identities or hardware were used. Screenshot evidence: ignored local `docs/ui-review/assistant-local-verified.jpg`.

Broader paraphrase coverage, all prepared acceptance cases, cross-source tie/race/recovery scenarios, simultaneous staff/load tests, long cold-start soak and actual ESP32 behavior remain unverified. Numeric game settings still require play-testing.

References: [Ollama chat API](https://docs.ollama.com/api/chat), [structured outputs](https://docs.ollama.com/capabilities/structured-outputs), [model](https://ollama.com/library/qwen3:4b-instruct), [MariaDB transaction access modes](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/set-commands/set-transaction), [per-statement limits](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/set-commands/set-statement).


## Learning and clarification update — 18 November 2026

[Approved-example retrieval and datasets](assistant-learning-and-datasets.md) extends private typed memory with bounded reuse of current owner-approved routing corrections. Clear questions still answer directly. Supported ambiguous questions offer two interpretations before analytics; choices carry any explicit period/source. The backend keeps all factual and privacy boundaries, and weights remain unchanged. This supersedes descriptions of examples as export-only preparation.


## Common interaction corpus — 18 November 2026

The [learning guide](assistant-learning-and-datasets.md) now includes an original 125-example English/Taglish interaction corpus. Training phrases support whole-utterance social replies and typed system routing; evaluation/boundary cases are kept separate. Friendly replies preserve previous system context and work without Ollama. Mixed greeting-plus-request messages retain their subject and pass the normal privacy/action/domain checks. No unrelated knowledge or new model tools are introduced.


## Compound greetings and behavioral corpus — 18 November 2026

The [behavioral expansion](assistant-behavioral-expansion.md) fixes compound and joined greetings such as `hello goodevening` and `hiiii goodmorning`. It adds 443 original examples and a bounded full-utterance social grammar, while mixed requests keep their subject and pass normal guards. Greeting, identifier/privacy, control and unrelated-subject regressions passed in the full 140-test backend suite, alongside disposable API and local Ollama checks. Model weights remain unchanged.


## Research-guided request grounding and Settings — 18 November 2026

See [research, architecture and validation](nlp-grounding-research.md). The current explicit measure and operation now outrank unrelated history and incompatible examples. Participant score lists, averages, completed-round sums, rankings and distributions have separate contracts. Score lists show public codes with best valid completed scores, source labels and bounded 50-row pagination; “next page” continues the same scope. A new `score_page` field is schema-validated in typed context, and score aggregation definitions are curated.

Model status, automatic-scope information, memory controls/counter and training management now live in **Dashboard Settings** at `/admin/settings`. Per-answer review controls moved there as **Review last eligible answer**. The chat remains focused on questions, replies and evidence. Memory-toggle scope remains the administrator session, and all existing privacy/action/authentication boundaries remain enforced.


## Quality audit update — 19 November 2026

The [cross-system audit](quality-audit.md) corrects language families rather than exact chat phrases: registration/population wording, individual versus aggregate points, public ID-protection questions, architecture explanations and current-measure precedence over history. Unknown subjects now prompt clarification before data access, so an unrelated game question cannot be answered using Stack Moko Baby scores. Language coverage remains bounded; clarification is not a claim that every paraphrase is understood.

Public knowledge now describes Dashboard Settings, Open Sans Variable, command acceptance/review holds and the actual review workflow: Settings → Review last eligible answer / Training examples. Memory and connection controls remain in Settings. An older memory read cannot restore forgotten context; an obsolete connection failure cannot replace a newer ready state.

44 actual local `qwen3:4b-instruct` regression cases passed after fixes. The initial audit set passed 19/28; an independent 16-case follow-up initially passed 15/16 and exposed an unrelated-domain substitution. All 44 now serve as regression cases, not held-out proof of general accuracy. Synthetic public data only; no weights were trained. Existing private examples may need explicit re-review because the normalization/public-context fingerprint changed.
