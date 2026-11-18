# Reviewed examples for later local fine-tuning

18 November 2026 · Review/export workflow implemented. Private per-admin memory remains separate. No model training, artifact import, activation or cloud upload is performed.

## What the examples teach

The current local model interprets normalized questions and emits a strict routing plan. Numerical answers and system explanations still come from validated backend analytics and reviewed cards. The dataset therefore teaches **intent routing**, not live scores, player facts or unrestricted answer prose. It can capture English/Taglish phrasing and corrected topic/knowledge/social/definition labels while preserving the existing system-only boundary.

Raw chat history was never retained, so this feature does not scrape past transcripts. Select the most recent eligible current/future reply explicitly in Dashboard Settings. User-approved memory can supply only typed context hints, not old answer text or metric values.

## Operator workflow

1. Ask a question in Stack Intelligence. Open **Dashboard Settings → Review last eligible answer** after an eligible reply. Private/control-blocked or otherwise unrepresentable inputs have no candidate.
2. Inspect **Sanitized input** and **Typed context included**. Unknown words were discarded by the ordinary privacy/vocabulary normalization. If words were lost, approve only if the visible input still expresses the intended question; otherwise reject/remove it. Do not enter identifiers or credentials to recover missing words.
3. Correct the routing topic and its matching knowledge/social/definition label, then **Save pending example**. This is an explicit opt-in write. No automatic collection occurs, and proposing does not approve.
4. In **Training examples**, select the pending example, inspect its input/labels and check the review confirmation. **Approve example** makes it eligible for the current context. **Save as pending** removes approval when revising; **Reject example** excludes it; **Remove example** deletes the selected owner-scoped row from future exports.
5. Choose **Export approved JSONL**. Only this admin’s approved, valid examples matching the current prompt/normalizer/schema/knowledge/vocabulary version are exported. Reopen/review if context changed. A changed context or stale row revision cannot be silently approved from an older open dialog. Increment the public normalizer revision when changing normalization/subject-hint semantics; it is included in the context fingerprint.

The review form accepts controlled labels rather than free-form answer text. Examples are private to the signed-in admin. Memory-off does not auto-select examples, but a separate explicit review action can still create one. **Forget saved memory** clears topic/preferences memory; separately selected training examples are managed in their own review queue. Removing/rejecting cannot revoke a file already downloaded; exports remain under the operator’s filesystem control.

## Stored data and limits

Migration [004_assistant_training.sql](../backend/migrations/004_assistant_training.sql) adds `ai_training_examples`. It holds an owner FK, random example UUID, hash of the sanitized input for deduplication, bounded typed input JSON, strict target JSON, pending/approved/rejected status, optimistic revision, public context/policy version and creation/review timestamps. The input fingerprint is not an identity lookup hash and is not included in dataset records. Duplicate proposals return the existing row without overwriting its reviewed label.

No raw question, response prose, student ID, nickname, credentials, player row, score, game count, snapshot or telemetry is stored. Tokens must belong to the approved vocabulary and pass the ordinary private/control guard again. Context is the existing strict enum/boolean/level/top structure, with at most six recent contexts. Input text is bounded to the runtime question limit. Targets cannot contain arbitrary fields, facts or executable commands. Follow-up labels require an actual previous subject; knowledge labels cannot contradict explicit reviewed subject hints.

The queue is capped at 1,000 records per admin. Account-row locking serializes quota checks. List pages return at most 25 examples; export returns at most 1,000 approved current-version records. Every query is owner-scoped, parameterized and statement-time-limited. A corrupted/stale-schema row is excluded rather than exporting raw database content. Training endpoints are separate from the read-only chat tool set: the model cannot call them, approve labels or train itself.

## API contract

- `GET /api/admin/assistant/training/options`: authenticated label choices and current public context version.
- `GET /api/admin/assistant/training?before=<cursor>`: authenticated current-owner queue, current/stale flags and pagination cursor.
- `POST /api/admin/assistant/training`: CSRF-protected strict `{input, target}` proposal, always pending when newly created. See [synthetic request contract](../contracts/assistant-training.example.json).
- `PATCH /api/admin/assistant/training/{example_uuid}`: CSRF-protected `revision`, `decision` (`revise`, `approve`, `reject`), `target`, review confirmation and current `context_version` for approval. Revision/context conflicts return 409; missing confirmation is rejected.
- `DELETE /api/admin/assistant/training/{example_uuid}`: CSRF-protected owner-only removal; other owners receive 404.
- `POST /api/admin/assistant/training/export`: CSRF-protected export response with JSONL content, count, filename, public context version and `automatic_training: false`. No approved current rows returns 409.

Eligible chat replies may include a volatile `review_candidate` with sanitized input/labels. It is not written by the query route and contains no raw answer. The UI review queue persists only after explicit proposal. Candidates are suggestions, not ground truth: approval remains a separate reviewed action.

## Export format and later training

Each JSONL record has a `messages` list: the trusted current routing system prompt, the normalized typed input as the user message, and the approved routing JSON as the assistant message. Owner IDs, example UUIDs, fingerprints and database row metadata are omitted. This follows the conversational role/content pattern documented by [Hugging Face TRL](https://huggingface.co/docs/trl/dataset_formats). This application does not implement native function-call SFT; labels are the existing classifier JSON.

Save private dataset files outside the checkout. JSONL files, training-data/artifact folders and common model-weight files are excluded from Git and Graphify. Never paste real exports, records or backups into model context or graph inputs. No server dataset files are written or uploaded by this workflow.

Later, before any actual training:

1. Build enough diverse reviewed examples, including English/Taglish paraphrases, ambiguous questions and follow-ups. Split training/evaluation by related input/context groups to avoid near-duplicate leakage. No minimum corpus quality or model improvement is established by this implementation.
2. Choose a trainer, exact base checkpoint/tokenizer and resource budget. Validate chat templates, context lengths and assistant-target loss handling. Keep the current app policy and output schemas unchanged.
3. Train locally in a separate reviewed job, then compare a held-out routing/policy suite against the unchanged baseline. Do not memorize event facts or use actual identities as samples.
4. Validate export/import compatibility for the exact chosen model architecture and artifacts. Ollama’s official [model-import guide](https://docs.ollama.com/import) documents importing prepared Safetensors or GGUF models; it does not establish compatibility for an untested future checkpoint.
5. Use a separate local candidate model tag, replay privacy/role/metric cases and measure cold/warm latency before deciding to activate it. No training library, weights, new model tag or deployment was installed/changed by the review/export feature.

## Validation — 18 November 2026

The full backend suite passed **100 tests**; the new training workflow has **14 focused tests**. Checks cover explicit opt-in/no automatic collection, strict privacy/input/target validation, pending export rejection, mandatory review confirmation, approval/export/rejection/revision, duplicate safety, stale-context approval invalidation, owner isolation, CSRF, removal, queue limit and pagination. Existing memory/player/scoring checks remain passing. The Vite production build passed. The existing FastAPI/Starlette TestClient dependency deprecation warning remains.

Computer-use checks used a disposable synthetic database: hello → inspect sanitized tokens/context → pending → approval disabled before confirmation → approve → export. The browser emitted a successful download event; exported contents were not opened through the computer-use tool. The UI confirmed the active model was unchanged. Temporary test processes/databases were removed; no existing player/game records were used. Migration 004 was applied additively to the development database. Screenshot: ignored local `docs/ui-review/assistant-training-approved.jpg`.

Actual fine-tuning, model import/activation, training quality, held-out improvement, hardware integration and release load/retention policy checks remain unverified. Do not label dataset preparation as a trained or improved model.


## Runtime reuse update — 18 November 2026

Current approved owner examples now help route future questions when memory is enabled. See [learning and datasets](assistant-learning-and-datasets.md) for the exact retrieval rules, two-interpretation behavior, original corpus and collected public references. Pending/stale/unapproved rows remain excluded. Review/export APIs and explicit approval remain unchanged; no weight training occurs. This update supersedes earlier statements implying approved examples are only used by a later training stage.


## Controls relocated — 18 November 2026

Review management now lives in `/admin/settings`. Use **Review last eligible answer** to inspect the current volatile sanitized candidate, then save pending and approve separately in **Training examples**. Chat no longer contains per-answer review buttons. Reloading the workspace can discard an unselected candidate; persisted pending/approved examples remain in the owner’s review queue. See [request grounding and Settings](nlp-grounding-research.md).
