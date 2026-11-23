# NLP admission repair — 24 November 2026

## Problem

Most assistant failures were not wrong answers. Valid questions were **refused before the model tried to understand them**. In the typed-context v2 regression (146/325 accepted), about 125 of the 179 failures were local holds:

- 83 `unrecognized_context`: one unknown word blocks the whole question.
- 42 `system_scope`: off-topic, from either the local guard or the model's topic check.

Only about 21 were answered with the wrong topic or settings. These are counts from the stored result file; individual held-out questions were not read or used.

The main root cause was the public dictionary builder (v1). It removed a word **entirely** whenever any one of its WordNet senses was a person or instance, or the word was ever capitalised. So everyday words like *head, power, sort, better, contact, add, down* and *far* were "unknown". WordNet also stores only base forms (*ran, meant, goes, oldest* were missing). Common Tagalog forms with the *-ng* linker (*huling, aking*) and words sharing a spelling with a proper name (*iyo*) were missing too.

## Changes

| Change | Where | Safety boundary kept |
|---|---|---|
| **Lexicon v2** (`assistant-language-lexicon-v2.json`, 196,600 forms). A word is kept when at least one sense is ordinary. WordNet irregular forms (4,576) are added. Tagalog words are no longer removed for sharing a spelling with a name. Built offline from the same local WordNet archive and cached Kaikki file, with no NLTK or network: `python backend/build_language_lexicon.py --v2`. | `backend/build_language_lexicon.py` | Words whose every sense is a person, instance or proper name stay out. Title-case Tagalog proper names (e.g. *maria*) stay out even when English has a rare common sense. v2 contains every v1 word. v1 is kept unchanged for replays. |
| Runtime forms: *-es*, superlatives (*oldest, biggest, happiest*) and the Tagalog linker (*huli+ng, akin+g*, root must be a public Tagalog word). | `assistant_language.project_words` | No fuzzy matching. Names such as *ExamplePerson, Juan, ExampleTown* remain unknown (tested). |
| Reviewed chat shorthand (*pls, rn, u, thx, gonna, panu* and similar) and stretched spellings (*pleaseee*). | `assistant_language.SHORTHAND` | Each maps to an ordinary known word; none is a name, value or command. |
| **Contextual follow-ups** skip the model topic check. This applies to a short question with a previous topic, a reference word (*that, it, iyan, yun* and similar), no unknown words and no foreign subject. | `assistant.contextual_follow_up` | Every word must be project, follow-up or reference vocabulary, so a follow-up cannot bring in a new subject (tested with *banana* and *basketball*). |
| **Topic-check examples**: 8 short demonstrations written for this stage (English, Taglish, design, follow-up, social, off-topic). | `assistant.SCOPE_EXAMPLES` | Never copied from evaluation or holdout cases. No retrieved or private examples reach this stage (tested). |
| **One-tap choices instead of dead-end refusals.** When a question is held as unknown wording or off-topic, up to three event topics named by its recognised words are offered as buttons. | `assistant_learning.topic_choices`, `AdminAssistant.jsx` | Nothing is answered until the person taps; every suggested question routes to read-only analytics without the model (tested). An unknown name never reaches the model or analytics (tested). |

## Measured results (development data only)

`backend/measure_admission.py` runs the real local gates plus the live `qwen3:4b-instruct` topic check over the 130 development questions and 60 out-of-scope development questions in `backend/nlp_lab/data/`. The "before" run used the previous commit (8906bb7) from a temporary worktree. These questions were inspected during this work, so this is **development regression, not held-out accuracy**.

| Measure | Before | After |
|---|---:|---:|
| Supported questions admitted (local or model) | 99/120 | **112/120** |
| English supported admitted | 60/76 | 71/76 |
| Taglish supported admitted | 39/44 | 41/44 |
| Unsupported development questions held | 10/10 | 10/10 |
| Out-of-scope family questions held | 58/60 | **59/60** |
| Supported questions admitted before but held after | — | 2 |

Without the model, refusals of supported development questions dropped from 21/120 to 5/120. Artifacts: [before](nlp-evaluation/results/admission-dev-before-20261124.json), [after](nlp-evaluation/results/admission-dev-after-20261124.json).

Admission is only the first step: an admitted question can still be routed to the wrong topic. End-to-end accuracy needs the consumed replay below and, for any new generalization claim, a fresh independently reviewed test set.

## Consumed 325-case replay (regression only)

`backend/replay_consumed_holdout.py` reran the already-consumed v1 holdout end-to-end, with the same dataset, gold labels, original scorer and model. This is **regression evidence on reused data, not unseen accuracy**. No predictor change was made after seeing these results. [Result](nlp-evaluation/results/holdout-v1-regression-v12b.json).

| Measurement | v11 (20 Nov) | v12b (24 Nov) |
|---|---:|---:|
| Accepted intent/context matches | 135/325 (41.54%) | **191/325 (58.77%)** |
| Exact topic/subtype | 134 | 190 |
| Primary intent / macro F1 | 145 / 0.4730 | 198 / 0.6320 |
| Valid requests clarified | 135/300 | **73/300** |
| Unsupported correctly held | 24/25 | **22/25** (3 false acceptances) |
| Service errors | 0 | 0 |

The Wilson interval is 53.35–63.99%, assuming independent cases; the cases are correlated and consumed. Per intent (out of 25), v11 → v12b:

| Overview | Players | Queue | Cabinet | Scores | Levels | Trend | Top | Definition | Knowledge | Social | Follow-up | Unsupported |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7→13 | 15→20 | 14→17 | 14→18 | 12→16 | 5→11 | 8→12 | 6→11 | 5→9 | 7→12 | 16→22 | 2→8 | 24→22 |

**Trade-off:** off-topic false acceptances rose from 1 to 3, because more questions now reach the model's topic check. Those cases were not inspected or tuned against. Reducing them needs fresh development data, not this consumed set.

The first replay attempt finished all 325 cases but rejected itself. The runner's final integrity check hard-coded the v1 lexicon filename, so with v2 active it always failed, even though the frozen predictor and lexicon were unchanged. The check now uses the file the app actually loads. The invalidated attempt is kept outside the docs in `.tools/evaluations/invalidated/`.

## Human-confirmed v2 replay (regression only)

After the owner's complete human review of the v2 packet (325 confirm, 0 corrections), the current assistant was replayed once on it with the unchanged `score_v2` scorer. The runner is `.tools/nlp-lab/review/replay_human_reviewed_v2.py`. It requires every case to have a latest human decision that agrees with the scored gold, and freezes the predictor, lexicon, scorer and first-use artifacts.

| v2 set | First use (20 Nov) | Typed-context (21 Nov) | Now (24 Nov) |
|---|---:|---:|---:|
| Accepted | 130 (40.0%) | 146 (44.9%) | **173 (53.2%)** |
| Paired vs now | 43 gained / 0 lost | 27 gained / 0 lost | — |
| Unsupported held | — | 19/25 | 22/25 |

Per intent (of 25), typed-context → now:

| Overview | Players | Queue | Cabinet | Scores | Levels | Trend | Top | Definition | Knowledge | Social | Follow-up | Unsupported |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3→9 | 17→19 | 12→15 | 8→9 | 18→19 | 10→14 | 11→12 | 11→13 | 8→9 | 7→7 | 15→18 | 7→7 | 19→22 |

English 106/176 and Taglish 67/149 were accepted.

The remaining 152 failures are still mostly holds before understanding: 55 `unrecognized_context` and 29 `system_scope`. There are also 27 answered with the wrong label and 23 generic `system_context` replies. Knowledge and follow-up did not improve. Result: [human-reviewed-v2-regression-20261124.json](nlp-evaluation/results/human-reviewed-v2-regression-20261124.json). This is regression evidence on a consumed set, not unseen accuracy.

## Verification

- Backend: **457 passed** (443 existing + 14 new in `tests/test_assistant_admission_v2.py`), against disposable XAMPP databases. One existing test now allows the fixed scope demonstrations, still forbidding retrieved or private examples.
- Frontend: 48 unit tests passed; the choice buttons now render for 1–3 options.
- **Line-ending repair:** Git's `core.autocrlf` had rewritten the four frozen scorer files with CRLF, so the consumed-set replay refused to run. Their LF bytes were restored (hashes now match the frozen manifest exactly). `.gitattributes` now marks the frozen evaluation files `-text` so this cannot recur.

## Still open

- A fresh, independently reviewed test set (100–300+ cases, 20–50 per intent) is required before claiming improved unseen accuracy. Both 325-case sets are consumed.
- Wrong-topic answers and generic system replies (about a quarter of the remaining failures) were not addressed here.
- The model topic check now sees more questions; its decisions remain a model judgement, not proof of scope.
