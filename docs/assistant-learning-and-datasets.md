# Stack Intelligence learning and clarification

18 November 2026. Implemented locally with the existing Ollama router, FastAPI and XAMPP MariaDB. This extends the [review/export workflow](assistant-training.md); the model weights remain unchanged.

## Learning from past chat

The existing private per-admin memory remembers typed subjects, periods, sources, language and reply-length preferences. The application never retained raw historical chat, so it cannot recover old discarded messages. Current and future sanitized corrections can be selected with **Review for training**, corrected and explicitly approved in **Training examples**. These current-version, owner-approved examples are now reused during question interpretation rather than only being exportable.

With memory enabled, the application reads at most 1,000 approved examples for the signed-in admin and current public context fingerprint. Pending, rejected, stale, invalid and other administrators’ rows are excluded. A matching approved correction can route directly; otherwise a bounded token-similarity lookup supplies at most three sanitized demonstrations to local Ollama. Demonstrations remove recent history, cap tokens/meaning hints, and each serialized demonstration is at most 2,000 characters. Conflicting exact corrections request clarification. There are no raw database facts, player identifiers, nicknames, scores or historical answers in these examples. The ordinary privacy/action guard still runs first, and current explicit subjects retain precedence.

**Memory off** disables owner-example reuse, while the public project corpus remains available. Approved examples remain separately manageable in their review queue. Deleting/rejecting an example removes it from future retrieval; exported files remain separate. Changing prompts, normalization, schemas, reviewed cards or the project corpus invalidates prior approvals until re-review. No automatic approval, transcript scraping, fine-tuning, model import or cloud upload occurs.

Results are always recomputed from current read-only analytics after routing. Remembered conversations never become evidence for current counts, scores or hardware connectivity.

## Two interpretations only when needed

Clear greetings, factual requests and metric definitions keep the direct conversational path. Supported ambiguous questions can return exactly two fixed, system-grounded interpretations before querying analytics. Initial cases cover unspecified accuracy (overall versus by level), ambiguous player performance (participation versus results), and unsupported system-performance wording that could mean event results versus cabinet readiness. This is a bounded ambiguity detector, not a calibrated confidence score or a guarantee to detect every difficult question.

For example, “What is our accuracy?” offers **Overall game accuracy** and **Accuracy by level**. Choosing one sends its safe canonical question through the normal authenticated endpoint. Explicit named periods and sources in the original question are included in both options. The assistant does not claim either answer is correct before that choice. Private/control requests cannot use choices to bypass the guard. Unrelated questions stay within the existing system-only boundary. There are no mandatory Period/Results controls.

## Collected datasets

| Dataset | Local content | Intended use | Licence/source |
|---|---|---|---|
| Stack Moko Baby routing v1 | 66 original synthetic English/Taglish questions: 45 runtime examples, 21 evaluation-only questions | Relevant game, queue, registration, IoT, results, knowledge and definition routing | Project-authored; no real chat or records; `backend/data/assistant-routing.json` |
| Stack Moko Baby interactions v1 | 125 original examples: 91 social, 8 follow-up, 10 mixed system requests, 16 boundary checks; 85 runtime-training and 40 evaluation-only records | Common English/Taglish interaction with whole-utterance social replies and system-only routing | Project-authored; no scraped chats; `backend/data/assistant-interactions.json` |
| MASSIVE 1.1 | 19,521 English and 19,521 Tagalog utterances; original train/dev/test partitions retained | Language/reference material for later reviewed adaptation; Tagalog is not a mixed Taglish gold set | [Amazon MASSIVE](https://github.com/alexa/massive), [dataset notice](https://github.com/alexa/massive/blob/main/NOTICE.md), CC BY 4.0; cite FitzGerald et al. (2022) and Bastianelli et al. (2020) |
| CLINC150 | 23,700 English intent/OOS examples, preserving upstream splits | Unrelated-request and intent-boundary evaluation after project-specific relabelling/review | [Original repository](https://github.com/clinc/oos-eval), [upstream licence](https://github.com/clinc/oos-eval/blob/master/LICENSE), CC BY 3.0; cite Larson et al. (2019) |

The external data is reference material, not Stack Moko Baby knowledge and not runtime demonstrations. Its original banking/travel/device-command labels must not become game tools. CLINC’s upstream “in-scope” labels refer to its own benchmark, not our system; even its out-of-scope records require project review before being used as negative labels. Preserve the evaluation split and group related paraphrases before later training; the small project test split only checks examples not loaded at runtime and is not evidence of a measured generalization gain.

Raw downloads, two selected MASSIVE locale files, licences and the download manifest are stored under ignored `.tools/nlp-datasets/`. The selected locale copies drop worker identifiers, judgments and annotation metadata. No application database or private export is opened by the downloader. The fetcher streams fixed official public URLs with byte limits and reads allowlisted tar members without extracting paths. The CLINC download uses resolved commit `828f8093932c8fe6ca7936c3d2e52903b1c523de`; observed SHA-256 `36923c3705a59e08fe9c3883d8bc2dd966ef93e22cb78ac41171782a698d56e0`. MASSIVE 1.1 archive observed SHA-256 `4cba5faa11c71437928e17cb1b9b3d8b8e727e7ea363a3a9a8045e19c0491577`. The manifest records source URLs, sizes, licence provenance and counts. These are download integrity records, not a claim of a preverified publisher signature.

To download again from the project root:

```powershell
.\backend\.venv\Scripts\python.exe .\backend\fetch_nlp_datasets.py
```

The downloader writes public files only to its fixed ignored directory and never uploads data. External files and private examples are excluded from Graphify; this document records public provenance and architecture instead.

## Verification and limits

Targeted synthetic MariaDB tests cover owner isolation, pending/stale exclusion, memory-off, reuse of approved corrections without a provider inference, fresh analytics after routing and no analytics before a clarification choice. Unit checks validate all project labels, separation of runtime/evaluation records, exactly two scoped choices for supported ambiguities and direct answers for clear questions. React component tests check rendering and choosing an interpretation. The external downloads completed with partition counts and hashes recorded. These checks do not establish an Ollama accuracy improvement, a trained model, physical ESP32 connectivity or full browser/desktop acceptance. A held-out baseline-versus-candidate routing and latency benchmark remains required before claiming an accuracy gain or activating any future fine-tuned model.


## Common interaction dataset — 18 November 2026

The new original interaction corpus adds greetings, wellbeing checks, thanks, identity/help, acknowledgments/apologies, farewells, typed follow-ups and greetings combined with real system questions. Only its training split contributes aliases, approved vocabulary and runtime routing demonstrations. Across both original corpora there are 191 records: 130 runtime-training examples and 61 evaluation-only cases. The new corpus has 72 runtime social phrases, six typed follow-ups and seven mixed system examples. Its held-out text and all 16 boundary checks remain outside production aliases/vocabulary/demonstrations.

Social matching requires the complete normalized utterance; it does not use keyword or fuzzy matching. Matching punctuation/case variants receive fixed English/Taglish responses tied to Stack Moko Baby, without Ollama, analytics, fabricated metrics or changes to the last validated topic. The original social patterns are retained. Social acts map to the existing strict response labels, and do not gain new tools or unrelated general-knowledge answers. Small-talk prefaces such as good morning, thanks and salamat are removed before the ordinary guard checks the remaining request, so “Thanks, reset the cabinet” remains refused. Mixed system questions continue to the normal classifier; a greeting never consumes their analytical subject. Named language preferences still take precedence.

Boundary fixtures cover private identifiers/credentials, game-control commands, prompt overrides, unsupported physical measurements and unrelated topics. They are authored test questions, with no actual private identifiers or records. Held-out positive wording can still require clarification when it contains unseen vocabulary; no held-out generalization or trained-weight improvement is claimed. Restart the application after editing the bundled corpora. Their combined digest is part of the approval fingerprint, so earlier private examples need re-review after this context update.


## Behavioral expansion update — 18 November 2026

[The conversational behavior expansion](assistant-behavioral-expansion.md) supersedes the earlier exact-alias-only limitation. A complete-utterance phrase grammar now handles combined greetings and known spacing/elongation variants, including `hello goodevening`. A new 443-record synthetic corpus adds 18,977 measured question/response text tokens (343 training, 100 evaluation records); all three original corpora total 634 records (473 training, 161 evaluation). Privacy/domain guards and bounded normalized retrieval remain active; dataset size is not a claim of model weight training or a measured accuracy gain.
