# Stack Intelligence — administrator chat

16 November 2026 · Implemented interface preview; NLP and live analysis are deferred.

## Current interface

The authenticated administrator shell includes **Stack Intelligence**, a fixed bottom chat dock shared by Overview, Analytics, Queue, Sessions and Machine. It is absent from login and player pages. The dock expands into a conversation panel and minimizes without losing the current draft or conversation while the admin shell remains mounted. Signing out or refreshing removes this in-memory preview; no transcript is saved to browser storage or the database.

The panel uses the existing neutral light/dark theme tokens and locally hosted Font Awesome font symbols. It includes a preview badge, event scope, six suggested topics, a scrollable conversation, a labelled multiline composer, character count, send action and clear-conversation control. Suggestions fill the input for editing. Enter submits; Shift+Enter adds a line. Empty messages cannot be submitted; questions are limited to 1,000 characters. Escape minimizes the panel and returns focus to its launcher. Page padding reserves room for the collapsed dock; the expanded panel is a nonmodal overlay beneath menus, dialogs and alerts. Narrow screens use a single-column suggestion list and a viewport-bounded panel.

Submitting adds the question and an explicitly labelled preview reply. It does **not** analyze live data, call a provider, contact the backend or alter any record. At most 20 messages are retained in component memory. The preview never invents a score, player count, cabinet measurement or answer about a real record. Its persistent notice reads “Design preview · Live analysis not connected.” Existing deterministic analytics cards remain separate from this future NLP service.

## Intended analytical coverage

The later assistant should understand ordinary staff questions across the whole authorized event:

| Area | Intended questions and evidence |
|---|---|
| IoT / cabinet | Connection freshness, last observed readiness, pending/review state and available heartbeat fields. Distinguish device and simulator sources; missing telemetry remains unknown. |
| Dashboard | Explain metric definitions, denominators, filters, selected scope and differences between counts. |
| Players | Registration totals, distinct participants and completed-player counts. Resolve permitted public display labels locally; never retrieve student IDs or identity material for AI. |
| Queue | Waiting totals, admissions status, waiting reasons and recorded queue timing, subject to available data. Explain why an operator action is needed without issuing one. |
| Scores / results | Valid score distribution, top results, wins/losses, timeouts and level performance, separated by ruleset and result source. |
| Event trends | Bounded time series, peak activity and cautious comparisons backed by recorded sample sizes. |

“Whole system” means analytical coverage of these areas within server-authorized scope. It does not grant identity access, arbitrary database queries, firmware execution or authority to change the game. The assistant is read-only.

## Deferred integration

1. Add a staff-authenticated backend conversation endpoint with CSRF checks, strict payload validation and the existing event/permission boundary. No endpoint is implemented by this design work.
2. Normalize analytical intent and filters on the server; block or redact student IDs and other private inputs before any provider call. Expose only bounded, prewritten read-only aggregate tools. Never pass database dumps, credentials, identity hashes or unrestricted logs to a model.
3. Add queue and score-distribution aggregate retrieval alongside the planned event/player, score, trend, level and machine summaries. Bind all retrieval to authorized event, time window, ruleset and source cohort. Curate dashboard definitions in application code.
4. Render validated answers with scope, source references, as-of time, denominators and any stale/missing-data caveats. Include loading, cancellation, no-data, unavailable, refusal and retry states. Preserve the draft on failure. Do not label preview replies as real analysis.
5. Select a provider/model and enforce deadlines, request/token/cost limits and the [AI policy](ai-system-rules.md). Persisting conversations or adding retention is a separate explicit design decision; this preview does neither.

The later integration requires authorization, privacy, provider-outage and numerical-evidence checks. This UI change has not run tests, builds, browser checks, database queries or hardware checks, following the user's instruction to test it themselves.
