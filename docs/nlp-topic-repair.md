# Wrong-topic answers and generic replies — 24 November 2026

## Problem

After the [admission repair](nlp-admission-repair.md), the largest answered-but-wrong groups were:

- **Wrong-topic answers:** the wrong metric or tool.
- **Generic replies:** a system explanation card (`system_context`) where the person asked for live data.

The causes were diagnosed on the 130-question **development** split only, using `.tools/nlp-lab/check_topics_dev.py`. That checker runs the live pipeline offline, with only training-partition examples retrievable, and records each reply's status, reason, topic and tools. No holdout or evaluation question was read.

| Development cause | Example (development wording) |
|---|---|
| The model filed live-state questions under an explanation card | "how is our carnival event doing", "status of the physical controller", "where do players most often miss" |
| A declined explanation still produced a definition | "the observed average score, with no explanation of its formula" |
| "How are results chosen for the leaderboard" was answered with the leaderboard | — |
| "Kanino/whose … highest" was not read as the leader | — |
| Thanks and greetings with courtesy endings were labelled as help | "Salamat po sa inyong pagtulong sa akin", "Good evening to you" |
| Hyphenated compounds of known words were unknown | "hour-by-hour", "perfect-placement" |

## Changes

| Change | Where | Boundary |
|---|---|---|
| **Live-state retry.** If the model chooses an explanation or definition card but the wording asks about the current state, routing is retried **once** with only the live-data topics plus `unsupported`. Live-state wording includes *now, current, status, last, recent, most often, whose, kasalukuyan, huling*. | `assistant.asks_live_state`, `LIVE_CUES`, `DESIGN_CUES`, `_ask` | A design cue keeps the card: *why, explain, rules, how it works, privacy, memory, architecture*. One extra local model call at most, within the existing deadline. |
| **Declined explanations.** "no / without / walang … explanation / formula / paliwanag" removes the explanation words before routing. | `assistant_semantics.explanation_declined` | "Explain the … formula" still gives the definition (tested). |
| Leaderboard-qualification questions give the results explanation; *whose/kanino … highest* gives the leaderboard. | `reviewed_explanation`, `constraints` | Counts ("how many results…") are still measured. |
| Courtesy endings are allowed in social phrases. | `assistant_interactions.composed_social` | The whole utterance must still be social; any extra request is routed normally. |
| Hyphenated compounds are split when **every** part is a known word. | `assistant_language.project_words` | A compound containing a name ("Jean-ExamplePerson") stays unknown (tested). |
| Tagalog *kanino → whose*, *napipili/pinipili/napili → chosen*. | `QUERY_FORMS` | — |

## Measured results

**Development (130 questions, inspected; development regression):**

| Outcome | Before | After |
|---|---:|---:|
| Correct (supported, of 120) | 95 | **109** |
| Wrong-topic answers | 7 | 3 |
| Generic replies | 11 | 4 |
| Supported questions held | 7 | 4 |
| Unsupported held (of 10) | 10 | 10 |
| Correct before, wrong after | — | **0** |

Artifacts: [before](nlp-evaluation/results/topics-dev-before-20261124.json), [after](nlp-evaluation/results/topics-dev-after-20261124.json).

**Consumed replays (regression only; nothing was tuned against them):**

| Set | Before this repair | After | Paired change |
|---|---:|---:|---|
| v1, 325 ([v13](nlp-evaluation/results/holdout-v1-regression-v13.json)) | 191 (58.77%) | **209 (64.31%)** | +20 / −2 |
| v2, 325 human-confirmed ([result](nlp-evaluation/results/human-reviewed-v2-regression-20261124b.json)) | 173 (53.23%) | **198 (60.92%)** | +25 / −0 |

- **v1 detail:** exact topic/subtype 208, macro F1 0.6779, valid clarifications 73 → 48, unsupported false acceptances unchanged at 3.
- **v2 by language:** English 121/176, Taglish 77/149.
- **v2 per intent (of 25), before → after:**

| Levels | Cabinet | Top | Trend | Knowledge | Definition | Players | Scores | Queue |
|---|---|---|---|---|---|---|---|---|
| 14→17 | 9→13 | 13→17 | 12→16 | 7→10 | 9→11 | 19→21 | 19→21 | 15→16 |

Overview (9), social (18), follow-up (7) and unsupported (22) were unchanged.

## Still open

- **v2 remaining failures (127):** 37 unknown wording, 33 answered with the wrong label, 21 generic replies, 16 off-topic holds, 11 unsupported-question holds. More questions are now admitted, so the absolute count of wrong-label answers rose (27 → 33) even though accepted answers rose by 25 with no paired losses.
- **v1:** 2 cases that were correct before are now wrong. They were not inspected or tuned against.
- **Not improved:** follow-ups (7/25) and overview (9/25) on v2.
- Any claim of accuracy on unseen questions still needs a fresh, never-run, independently reviewed set.

## Verification

- Backend: **477 passed**, including 16 new tests in `tests/test_assistant_topics_v2.py`. These cover the live/design distinction, declined explanations, qualification vs count, whose-highest, courtesy endings, hyphen/name handling, and an API-level check that the retry offers only live-data topics.
- Both consumed replays use their frozen scorers and integrity checks. The v2 run requires all 325 human decisions to agree with the scored gold.
