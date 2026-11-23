# Stack Intelligence label guide and review requirements

20 November 2026. This is the codebook for the offline experiment, not a claim of independent human review. Existing runtime routing and the original 325-case gold labels remain unchanged.

## Annotation unit

Label the current public question together with its validated prior topic/filter state when supplied. Do not infer a player's identity, a current metric value or a physical hardware condition from a message. Annotate the requested task, not the SQL function that happens to calculate it.

The offline comparison preserves the existing thirteen primary labels for traceability. A score average remains a `scores` request even if the backend uses an event-summary query. A genuine follow-up is a dialogue act; it is not a replacement for an explicitly stated new subject.

| Legacy primary label | Meaning and boundary |
|---|---|
| overview | Broad update across the current event; not a catch-all for unclear questions. |
| players | Registrations, distinct completed participants, completed games, outcome counts/rates or overall duration/accuracy. Separate enrollment from completion. |
| queue | Current waiting/assigned/admissions observations. A design explanation uses `knowledge:queue_flow`. |
| machine | Recorded cabinet/ESP32 state, contact freshness, signal or firmware. Simulator evidence does not establish physical health. |
| scores | Individual points, score aggregates and score distribution. Asking who leads uses `top`. |
| levels | Per-level attempts, failures, placement performance or difficulty. |
| trend | Activity across supported time buckets, busy/quiet periods and participation over time. |
| top | Ranked players or the leader by valid result; the highest numeric value alone remains `scores`. |
| definition | Meaning or formula of a metric, with its required subtype. An unqualified request for a current value is analytics. |
| knowledge | Explanation from an approved system card, with its required subtype. It is not proof of current database/device state. |
| social | A full greeting, acknowledgement, thanks, identity/help question, farewell or wellbeing interaction. A greeting followed by a score question requests scores. |
| follow_up | Omitted subject inherited from typed context, source/date changes or elaboration of that same topic. Missing required context must clarify; a new explicit domain overrides history. |
| unsupported | Another system/game, unrecorded measurement, private identity/control request or an otherwise unsupported task. Distinguish unfamiliar wording from unrelated meaning. |

Knowledge subtypes: gameplay, registration, queue_flow, architecture, dashboard, privacy, offline, results, assistant, memory, training. Social subtypes: greeting, thanks, identity, help, acknowledge, farewell, wellbeing. Metric definitions include accuracy, win_rate, scoring, average_score, total_score, highest_score and lowest_score; legacy queue/privacy definitions require a separately reviewed compatibility policy if a future schema replaces them with knowledge cards. Do not rewrite historical scores to hide that distinction.

## Proposed factorized state

`backend/nlp_lab/frame.py` prototypes a separate mode/domain/operation/dialogue-act state plus validated period, source, level, ranking limit and score page. It is not imported by the application and does not run tools. A follow-up merges only explicit validated filters with the old subject. A new explicit subject starts a new frame. No raw history, old score values, student IDs, names, credentials or arbitrary SQL belong in the frame.

The current model experiment trains legacy primary classes plus conditional subtype heads, not a fully supervised slot extractor. Frame reducer unit checks are implementation checks; they do not establish multi-turn model accuracy. The final test needs independently annotated expected domain, operation and filter/context outcomes, including missing context and explicit topic changes.

## Review rules

1. Check the current question's meaning before looking at a model prediction. Do not let the existing keyword router supply the gold label.
2. Use English, Tagalog and naturally mixed phrasing, different levels of formality, short fragments and spelling variation. Record language; do not count repeated prefixes/date substitutions as diverse families.
3. Include minimal semantic contrasts: meaning versus current value; enrollment versus completed people; maximum value versus leading player; queue state versus assignment workflow; device observations versus simulator limits.
4. Supply previous context for both genuine follow-ups and explicit new requests. Otherwise the classifier can learn that the presence of history always means follow-up. Add incompatible previous queue/score/knowledge subjects deliberately.
5. Use anonymous author/reviewer codes. A second person should independently review labels and resolve disagreement before final test freezing. The collection validator checks attestations, not the identity or independence of a real human reviewer.
6. Include near-topic negatives (another game's scores, another venue's queue, other machines) and clearly unrelated tasks. Privacy probes use placeholders, never real IDs or credentials.
7. Group a conversation and related paraphrase/template families before splitting. Detect raw, normalized and lexical near duplicates. Keep training, calibration/development and final evaluation separate.
8. Corrections to past chats require explicit owner approval and privacy review. Do not train automatically on raw chat or the assistant's own answers. Version and review any later model promotion separately.

## Dataset gaps discovered

The existing 515 training rows contain 315 social examples, only eight definitions and no unsupported class. Several definition subtypes have no examples at all. The lab adds sixty public synthetic negative development examples, deduplicates copies and quarantines conflicting normalized inputs without relabelling them. These additions are not human-adjudicated final test data.

The original source data also couples previous context with follow-up labels. Strong scores on a context-bearing question can therefore reflect a shortcut. Report paired misleading-history diagnostics separately from ordinary classification scores; do not count those variants as additional unseen cases.

Before production training, collect genuinely distinct reviewed examples for rare classes and missing subtypes, and balance language/family coverage. Thirty to fifty initial training examples per business intent is a proposed starting point, not a guarantee. Use learning curves and separate validation to decide whether more data helps.

## Independent final collection

The local file `.tools/nlp-lab/review/holdout-v2-collection.json` now contains **325 AI-authored questions and proposed labels**, 25 per primary intent. The [preparation audit](nlp-evaluation/candidate-v2-preparation.md) records language/family coverage, prior contexts and zero automated reference collisions. Every independent review remains pending. Authoring and auditing candidate cases can proceed before human review; do not leave slots blank merely because labels still need adjudication. Never represent the assistant’s own labels as independently reviewed human gold.

No final test is frozen, scored or called unseen until collection and review are complete, overlaps with all previously seen project/lab/consumed inputs are audited, and the selected predictor, lexical assets, decoder, scorer and acceptance rules are frozen. The initial collection validator is not the complete final-evaluation protocol. Preserve v1 as regression evidence; a changed schema/scorer must have a new version and separate report.
