# Stack Intelligence local classifier experiment

20 November 2026. The offline comparison is implemented and ran locally. **Keep the current live router.** Experimental models are not imported by the API, installed in the application environment or selected by Settings. No database migration, frontend change or server restart is needed.

The subsequent [history-shortcut experiment](nlp-evaluation/history-lab-20261120.md) adds 792 training-only history variants and compares augmentation with current-question-only classification. It reduces misleading-history errors but does not improve overall correctness or answer-policy coverage; no candidate is promoted. The same frozen development cohort has 40/120 supported inputs blocked before classification, so input admission needs a separate privacy-preserving review. Four additional integrity checks bring the offline total to fourteen passed checks.

Read the [measured report and graph](nlp-evaluation/offline-lab-20261120.md) and [annotation guide](nlp-label-guide.md). This implements the authorized comparison and data audit; it does not close the independent NLP quality gate.

## Implementation

`backend/nlp_lab/` contains an isolated data audit, family grouping, deterministic train/calibration/comparison split, hierarchical classifiers, confidence calibration, abstention policy, local Ollama adapter, SetFit training and typed conversation-state prototype. `scripts/nlp-lab.cmd` runs that environment without changing application startup.

Candidates include word/character TF-IDF with balanced logistic heads on original versus normalized text, frozen multilingual E5 embeddings with the same heads, and genuinely adapted multilingual SetFit embeddings with hierarchical heads. The Ollama baseline exercises current routing with train-only retrieval and no-data renderers, without MariaDB, private memory or real factual answers. Existing static prompt/social priors predate the split; the source comparison is seen development for that baseline.

The frozen baseline adapter maps both refusal and clarification to `unsupported`; its stored rows do not retain separate status counts. Baseline label metrics measure guard-aware routing, while learned-model argmax labels are measured after admission guards and reported with a separate confidence policy. This limits direct bare-model comparisons. Do not retrospectively modify the frozen adapter or its results to hide that distinction.

The lab adds sixty public synthetic negative development examples, 130 balanced developer-labelled development questions and twenty public wording probes. None enter runtime retrieval or the original holdout. The typed frame prototype separates mode, domain, operation, dialogue act and validated filters. It merges follow-up filters and resets the old subject for explicit new topics, but it is not a trained slot extractor or live conversation fix.

The [candidate evaluation packet](nlp-evaluation/candidate-v2-preparation.md) now contains 325 AI-authored questions and proposed labels, with automated overlap checks completed and independent review pending. Its validator requires completed questions, valid labels, family/language information and separate author/reviewer attestations. It cannot verify human independence, detect every private value or replace the full overlap/freeze process. Assistant-generated labels cannot be represented as independently reviewed human gold.

## Measured decision

On the same 130 development cases, the current Ollama adapter and frozen E5 each got 63 primary topics correct; trained SetFit got 61. Exact-label counts were 60, 60 and 59. No experimental classifier demonstrated an improvement sufficient for promotion.

Calibration exposed a coverage cost: TF-IDF abstained on all supported questions, frozen E5 answered 8/120 and SetFit answered 29/120. High routing precision on a small accepted subset is not overall answer accuracy. Raw errors, refusals and unsupported false acceptances remain in the report.

A post-hoc paired diagnostic added unrelated typed history to the same 120 non-follow-up questions. SetFit's primary-correct count fell from 52 to 8; it labelled 73 as follow-ups. The pool has 33 context-bearing follow-ups and zero context-bearing explicit new-topic examples. This supports a dataset-shortcut diagnosis and blocks promotion. It does not prove all SetFit recipes or multilingual encoders are unsuitable.

The saved tokenizer emitted an upstream regex warning. Base and saved XLM-R tokenizers produced identical encodings on all 250 balanced/context input strings. No Mistral-specific patch was applied. This verifies those inputs, not every string or upstream library behavior.

## Frozen protocol

- Only explicit `train` rows from four public corpora enter the pool, plus the lab-only negative supplement. No private chat exports or final evaluation prompts enter training.
- Duplicate copies are removed and normalized conflicts quarantined. Raw/normalized equality, source family and high lexical near duplicates are grouped before splitting. The recorded near rule is Jaccard ≥ .75 and character similarity ≥ .88 with the same typed previous context. This does not establish semantic independence.
- Splits contain 295 training, 98 calibration and 101 comparison rows. Vocabulary, embeddings, classifier heads and SetFit adaptation fit training rows only; temperature and operating points fit calibration rows only. The 130 balanced questions and twenty wording probes are separate inspected development diagnostics.
- Protocol/input/code hashes are frozen before predictions. Changed lab code or data requires a new run ID; output files use exclusive creation. Do not overwrite poor results, tune on comparison questions and continue calling them unseen, or rewrite historical labels.
- Protected runtime assistant files, corpora, lexical assets, original evaluation files and retained original results are checked against the manifest. Models, lab inputs and review packets are excluded from Graphify. The final evaluator/scorer stays separate from this development scorer.
- The original 325-case benchmark remains consumed regression evidence. The new 130-case set has ten per intent and no independent adjudication. Counts from different cohorts must not be combined or substituted.

## Local environment and reproduction

The isolated environment is `.tools/nlp-lab-venv`. Resolved packages are saved in `.tools/nlp-lab/intent-lab-20261120-02/environment.txt`: CPU Torch 2.9.1, SetFit 1.1.3, sentence-transformers 3.4.1, Transformers 4.57.6, datasets 3.6.0 and scikit-learn 1.9.1. Training and inference are local; initial public package/model downloads were required.

To recreate the environment from the project root using a compatible Python:

```powershell
python -m venv .tools/nlp-lab-venv
.\.tools\nlp-lab-venv\Scripts\python.exe -m pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
.\.tools\nlp-lab-venv\Scripts\python.exe -m pip install -r backend/nlp_lab/requirements.txt
```

The reviewed public model is `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, cached in `.tools/hf-public/`. It was downloaded anonymously using `huggingface_hub.snapshot_download` with that exact revision, `cache_dir='.tools/hf-public'` and `allow_patterns=['*.json', '*.txt', '*.model', '*.safetensors']`. Loading uses local files and `trust_remote_code=False`; telemetry and implicit account-token use are disabled. The model is MIT licensed. Model weights stay out of Git.

The retained successful run is `intent-lab-20261120-02`. The earlier prepare-only attempt failed before predictions because NumPy split indices were not JSON serializable; it is preserved. For another development experiment, intentionally version changes, choose a new ID and run stages sequentially. Ollama is needed for the baseline stage; MariaDB is not used.

```powershell
.\scripts\nlp-lab.cmd prepare --run intent-lab-new-id
.\scripts\nlp-lab.cmd sparse --run intent-lab-new-id
.\scripts\nlp-lab.cmd encoder --run intent-lab-new-id
.\scripts\nlp-lab.cmd setfit --run intent-lab-new-id
.\scripts\nlp-lab.cmd ollama --run intent-lab-new-id
```

SetFit ran forty contrastive steps with seed 20261120, batch eight, three sampling iterations, maximum length 256 and four CPU threads. Encoder training capped each primary class at sixteen rows (123 total); final heads fit all admitted training rows. This small fixed recipe is not exhaustive tuning or proof of language balance.

`docs/nlp-evaluation/audit_lab_context.py --run <id>` records a separate post-hoc diagnostic without retraining. `summarize_offline_lab.py --run <id>` publishes retained counts after checking frozen byte hashes and matching candidate cohorts. Its canonical path check handles Windows `scripts/../backend` versus `backend` spellings without weakening hash checks. The summary uses dated output names and refuses overwriting; choose new versioned outputs for later reports. `plot_offline_lab.py` reads the measured summary in the separate documentation plotting environment.

The separate follow-on code `backend/experiment_history.py` preserves all frozen `nlp_lab` source bytes. Its retained run is `history-lab-20261120-01`; commands use `.tools/nlp-lab-venv/Scripts/python.exe backend/experiment_history.py prepare --run <new-id>`, then the same command with `run` instead of `prepare`. Augmentation draws only from the first run's training partition, without resplitting or copying calibration/comparison/diagnostic questions. Original family/group membership remains attached to every variant. This does not create new linguistic families. `summarize_history_lab.py` and `plot_history_lab.py` publish the separate consumed-regression report.

Plotting now has a stable isolated `.tools/nlp-plot-venv` using the installed Python 3.13 interpreter and Matplotlib 3.11.2; the earlier temporary plotting environment referred to a removed app-bundled interpreter. Run `.\.tools\nlp-plot-venv\Scripts\python.exe docs/nlp-evaluation/plot_history_lab.py` to regenerate that plot, or `plot_offline_lab.py` for the first comparison. No packages were added to the application or model-training environments for this plotting repair.

## Verification and next work

Ten targeted checks passed for train-only source selection, split isolation, input admission, typed state, abstention/metric denominators, empty-review rejection and a no-database baseline adapter. Restricted Ruff checks passed. Protected hashes remained unchanged. Actual local baseline inference, frozen encoder inference and SetFit adaptation ran. No browser, MariaDB, ESP32 or full application regression pass is claimed for this offline-only addition.

Next development iteration: collect distinct reviewed rare-class and missing-subtype training families; include both genuine follow-ups and explicit new topics with matched prior contexts; record English/Tagalog/Taglish support; evaluate learning curves and context behavior on separate development material. Do not copy the 130 diagnostics or consumed 325-case questions into training to repair their scores.

In parallel, collect new final questions and independently review labels and expected typed state. Before first use, audit overlap against all seen corpora, lab inputs and consumed tests; freeze the chosen predictor, language assets, decoder, scorer and acceptance policy. Only then report fresh unseen results with failures, coverage, uncertainty and language/family breakdowns. The current live limitations remain visible until evidence supports promotion.

## Primary research

[SetFit's two-stage method](https://huggingface.co/docs/setfit/v1.1.3/en/conceptual_guides/setfit) motivates comparing adapted embeddings with frozen encoders and simple heads. The [multilingual E5 model card](https://huggingface.co/intfloat/multilingual-e5-small) documents the `query:` prefix and multilingual limitations. [Scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) motivates disjoint calibration and confidence reporting. [Out-of-scope intent research](https://aclanthology.org/D19-1131/) motivates negatives and false-acceptance measurements. [Schema-Guided Dialogue](https://github.com/google-research-datasets/dstc8-schema-guided-dialogue) motivates explicit state annotations; its data was not imported as evidence of project accuracy.
