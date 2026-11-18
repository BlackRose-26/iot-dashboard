# NLP request grounding: research, implementation and checks

18 November 2026 · Stack Moko Baby. This update addresses score questions being answered with queue counts, registration counts or an unrelated definition. No screenshot question was added to the runtime corpus, and no model weights were trained.

## Research consulted before completing the redesign

| Primary source | Relevant finding/principle | Project adaptation |
|---|---|---|
| [Ribeiro et al., CheckList, ACL 2020](https://aclanthology.org/2020.acl-main.442/) | Held-out aggregate accuracy can miss capability failures; evaluate linguistic capabilities and behavioral test types. | Minimum-functionality probes, invariance to irrelevant prior subjects, directional changes in requested operations, mixed requests and privacy checks. These are tests of the application pipeline, not additional runtime demonstrations. |
| [Elgohary et al., CANARD, EMNLP 2019](https://aclanthology.org/D19-1605/) | Conversational questions require resolving coreference/ellipsis into a context-independent question. | Resolve only missing typed slots from validated context. An explicit score subject replaces an older queue/definition subject; an operation-only follow-up may inherit a score measure from a validated score context. Unknown stripped subjects are not filled by guessing. This is a constrained engineering adaptation, not a trained CANARD rewrite model. |
| [Amazon Lex: intent slots](https://docs.aws.amazon.com/lexv2/latest/dg/intent-slots.html) | User intent and bounded parameter/slot values are separate concepts and require validation. | Separate the requested measure, operation, population and period/source instead of treating every mention of participants as a count request. Use a local domain schema; Amazon Lex/cloud processing was not added. |
| [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) | Supply JSON Schema and validate the model response with a typed schema. | Keep strict local JSON routing and add semantic checks: a valid JSON label is insufficient if it contradicts the current requested measure. This extra semantic validation is our application policy, not a correctness guarantee provided by JSON Schema. |
| [Google: Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml/) | Test serving infrastructure independently, use observable metrics and evaluate changes rather than assuming a more complex model is better. | Separate SQL/tool/formatter correctness, context handling and model routing; keep privacy-safe features consistent and report targeted measurements without claiming general accuracy. |

These sources support the design principles. The particular domain lexicon, metrics, thresholds and tool choices are engineering decisions for this system, and their limits require continued evaluation. The papers do not prove that this implementation generalizes perfectly.

## Diagnosed failures

1. A `follow_up` label could blindly reuse the previous tool/definition even when a new question named another measure.
2. The formatter’s generic participant fallback could return registrations/completed-player counts because an individual score request had no corresponding metric/tool contract.
3. A coarse `scores` topic previously defaulted to summary/distribution rather than a participant’s score values.
4. Retrieved demonstrations and approved labels could be structurally valid while contradicting the explicit current subject. Synthetic near-duplicates could occupy multiple retrieval positions.
5. Vocabulary normalization could discard operator words before interpretation. The domain’s measure/operator vocabulary now comes from its serving schema rather than depending only on example wording.

The deployed weights were unchanged, so these screenshots do not establish statistical model overfitting. They demonstrate routing, context and answer-contract failures. More generated examples alone would not repair them.

## Current pipeline

Privacy/action/domain guard → normalized domain features → local structured routing with bounded compatible demonstrations → typed subject/operation validation → approved read-only tools → backend values/templates with cited scope.

The domain schema separates individual scores, averages, completed-round sums, extrema, distributions, rankings, registrations, queue state, machine state, levels and trends. Operator aliases are compiled into the normalizer’s approved feature vocabulary. Definition requests remain separate from data requests; “What does score mean?” and “mean score” have different roles. Compound current requests can require multiple tools instead of silently dropping one.

Current explicit measure/operation constraints outrank the model’s proposed topic, historical context and reviewed examples. A bare supported metric is treated as a data request for that metric rather than inheriting an unrelated definition. Context fills omitted slots only when the previous typed subject supports them; missing unknown subjects still require clarification. Named period/source or score-page follow-ups reuse validated scope. A new explicit subject returns to automatic event-to-date/all-source defaults unless the message specifies a narrower scope.

Retrieval excludes labels incompatible with the current domain request and skips duplicate normalized-input/label demonstrations. It remains a bounded lexical lookup, not an embedding retriever or calibrated confidence estimate. At most three bounded examples reach Ollama. The runtime corpus was not expanded with the screenshot questions or evaluation probes. Current schema/prompt/vocabulary changes invalidate old private approvals until re-review.

## Score data contract

`get_player_scores` lists each participant’s **best valid completed score** separately for simulator and physical-device cohorts, using opaque public player codes. It returns a maximum of 50 rows per source per page, a distinct-player total, page number, basis and `has_more`. Ordering is stable by public code. A typed `score_page` is bounded to 1–2,000; “next page” advances the same validated score-list scope. Empty later pages distinguish “no scores on this page” from no recorded results for the period. Registrants with no completed result are not assigned an invented zero score.

Averages and total/minimum/maximum score requests use fixed summary queries for valid completed rounds in the same source/window. A round-score sum is a different basis from summing each participant’s best result, and is labelled accordingly. Rankings retain the existing tie-break rules. Missing averages/extrema remain N/A. Competitive metrics are never pooled across simulator/device cohorts.

All queries retain statement limits, bounded pagination, parameter binding and the shared repeatable-read/READ ONLY snapshot. No identity fields, nicknames, logs or credentials are provided to the model. The ordinary chart API does not fetch participant score pages unless that tool is explicitly requested. No database migration is required: score pagination is an additive field in the existing validated JSON context.

## Dashboard Settings

The authenticated `/admin/settings` page now contains appearance, local-model status/check connection, automatic scope information, private-memory controls, saved-context counter and training-example management. The chat no longer contains those rows or per-answer review buttons. Settings can open the current sanitized eligible candidate with **Review last eligible answer**; selecting/approving remains explicit.

A shared provider keeps Settings and the chat consistent throughout the administrator session. The memory toggle is session-scoped, matching its previous chat-only behavior; it is not a new persisted account preference. Toggling it clears the local restored subject. Forgetting saved memory clears the open chat state and relies on the existing backend revision tombstone. Logout unmounts the provider. Player routes remain outside the authenticated workspace. Theme persistence uses the existing dashboard theme setting.

## Verification and limits

The full backend suite passed 184 tests after the definition/operator refinement, and focused checks cover incomplete-subject clarification. Final verification is recorded in the delivery response. New checks cover eight score paraphrases under four deliberately irrelevant prior contexts and wrong model labels; operation changes; definition/data distinctions; partial-slot inheritance; a 55-player real MariaDB score pagination fixture; and authenticated end-to-end answers. Synthetic result fixtures use the existing scoring replay functions rather than arbitrary score formulas.

Twelve targeted local Ollama probes with deliberately misleading prior context returned the required tool selections and actual synthetic scores. They cover English/Taglish score lists, aggregates, mixed queue/score requests and rankings. Benchmark-only rate buckets were reset to avoid measuring the request limiter; production limits are unchanged. This is not a population accuracy estimate or a before/after model-training benchmark. Broader unseen language, negation and ambiguous referents remain future evaluation work.

The frontend suite passed 27 tests and the production build passed. A separate headless Brave context with a disposable API/database verified Settings navigation, relocated controls and the Taglish score list containing `DEMO-1`/`DEMO-2`. The screenshot was visually inspected at ignored `docs/ui-review/assistant-settings-score-list.png`. Computer Use could not connect after a retry; no desktop Computer Use pass is claimed. Temporary processes/databases were removed, and no real event records were used. No physical ESP32, load or production-wide NLP accuracy guarantee follows from these tests.
