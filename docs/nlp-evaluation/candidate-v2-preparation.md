# Candidate evaluation collection — authoring completed

**Subsequent first use, 20 November 2026.** Codex reviewed all 325 questions blind to proposed labels and predictions. The review agreed with 323 proposals and adjudicated two differences before freezing the scoring rules. The [reviewed CSV](../../.tools/nlp-lab/review/holdout-v2-ai-reviewed.csv) records AI provenance. The live service met the frozen routing and behavior criteria on **130/325** in the disposable-database evaluation. The [case results and metrics](results/holdout-v2-ai-first-use.json) retain all failures and family-grouped uncertainty. Any future use of these questions is regression. The authoring record below describes the earlier preparation stage.

20 November 2026. The previously empty collection now contains **325 AI-authored questions with proposed labels: 25 per primary intent**. Authoring and automated overlap checks are complete. Independent semantic/privacy review, final gold/scorer freezing and first-use evaluation remain pending. No accuracy is claimed for this packet and no experimental model was deployed.

Leaving every slot blank while waiting for review was an execution gap. Independent review is a separate acceptance step; it does not prevent preparing candidate questions. Historical experiment reports retain their measured results and record the collection status at their original run time.

## Files for review

- [Review CSV](../../.tools/nlp-lab/review/holdout-v2-review.csv) — questions, proposed labels, typed prior context, expected behavior/state and blank reviewer/correction columns.
- [Structured collection](../../.tools/nlp-lab/review/holdout-v2-collection.json) — full 325-case candidate packet; every review decision remains pending.
- [Automated audit](../../.tools/nlp-lab/review/candidate-authoring-v2.audit.json) — counts, overlap checks and hashes; contains no model predictions.
- [Pre-authoring protocol](../../.tools/nlp-lab/review/candidate-authoring-v2.protocol.json) — records the runtime predictor and existing scorer fingerprints before question authoring. The existing scorer is a reference, not an assertion that it already handles the new packet's acceptance rules.
- Original empty template: `.tools/nlp-lab/review/holdout-v2-collection.blank-template.json`. The frozen experimental datasets and reports were not rewritten.

These local evaluation files are outside Git, Graphify, runtime retrieval and training sources. They are not private chat exports or real player data. Do not copy their prompts into training examples, aliases or few-shot demonstrations.

## What was actually checked

| Check | Recorded result |
|---|---:|
| Filled questions | 325 |
| Primary categories | 13, with 25 questions each |
| English / Taglish annotations | 176 / 149 |
| Questions with typed prior context | 119 |
| Prior reference entries checked | 2,291 |
| Exact raw or usable-normalized reference collisions | 0 |
| High lexical near-reference matches | 0 |
| Exact/usable-normalized or high lexical near duplicates inside packet | 0 |
| Independently approved labels | 0 |
| Candidate predictions run | 0 |

Reference entries include public runtime corpora, validation inputs, consumed v1 questions, prior lab negatives/development/wording probes, public check scripts, test literals and static assistant wording. The reference count includes repeated entries; it is not a count of unique independent questions. Reference text is compared locally and is never sent to a model or printed in audit output.

The lexical threshold is fixed at content-word Jaccard ≥ .70 **and** character similarity ≥ .84. Two initial candidates collided with prior material and were replaced before prediction. No threshold was relaxed to hide overlaps. These automated checks do not prove semantic independence.

Language pairs share declared families rather than being represented as independent concepts. The packet records thirteen families in each ordinary analytics category, nine definition families, eleven knowledge families, seven social acts and twenty-five follow-up/unsupported scenarios each. These are author annotations awaiting review, not a claim of 325 independent semantic families. Avoid ordinary binomial uncertainty claims that ignore related families.

## Review and final evaluation

Review questions and proposed labels without seeing model predictions. Confirm whether each asks for an observation, a definition, system knowledge, social interaction, a genuine follow-up or an unsupported task. Check explicit new topics against unrelated prior state. Resolve ambiguous metric/knowledge labels and social help versus assistant-capability explanations before selecting acceptable-label rules.

Follow-ups include annotated context/filter continuity and two deliberately missing-subject cases requiring clarification. Validate these expected states and ensure the final scorer treats an appropriate clarification separately from a wrong answer. Do not silently apply the old scorer if it lacks those semantics. Freeze the final labels, acceptable outputs, predictor, language assets, decoder and scorer before first-use inference; record a consumption ledger and keep every failure afterward.

All reviewer codes, privacy approvals and independent-review statuses remain unset. An AI-authored label or a successful schema check is not independent human adjudication. The existing collection validator deliberately rejects approval of this pending packet. Corrections should use anonymous reviewer codes and explicit decisions; the preparer refuses overwriting approved entries. The CSV is a review artifact, not an automatic approval/import mechanism.

The current assistant remains unchanged because the [offline models](offline-lab-20261120.md) and [history experiment](history-lab-20261120.md) did not demonstrate sufficient overall correctness or useful answer coverage. The separate finding that 40 supported development questions were blocked upstream still requires a privacy-preserving input-admission design. Filling this collection does not fix that live behavior or establish a new accuracy score.

Verification: all eighteen offline checks passed, including four new tests for overlap detection, internal duplicates, missing-context clarification and validated follow-up-state annotations. Restricted Ruff checks passed. The existing approval validator correctly rejects the filled-but-unreviewed packet. Original experiment hashes, live predictor files and original evaluation evidence remain unchanged. No database, browser or physical-hardware validation is claimed for this preparation-only milestone.
