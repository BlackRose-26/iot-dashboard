# Conversational behavior expansion

18 November 2026. Implemented for Stack Moko Baby’s local administrator assistant. This fixes the reported `hello goodevening` failure and extends the [common-interaction corpus](assistant-learning-and-datasets.md). These changes do not train or replace Ollama weights.

## Why the previous behavior failed

The earlier social path recognized individual full-utterance patterns and a finite exact-alias table. Combining otherwise valid greetings, or joining “good evening” into one word, could miss both paths and enter the system-only clarification guard. Adding more examples alone would leave that structural limitation in place.

The implementation now canonicalizes only known social spelling variants and parses complete sequences of approved social phrases. Supported forms include `hello goodevening`, `HelloGoodEvening`, `hiiii goodmorning`, `hellooo good evening`, case/punctuation/emoji variations, English/Taglish greetings, greeting-plus-help and thanks-plus-farewell. Day-part responses echo the user’s supplied greeting; they do not infer the time from the host machine. Explicit language preferences keep precedence. Original supported patterns remain available.

## Boundaries and mixed requests

The composition parser must consume every word. It accepts at most 60 words and six social acts, with limited polite connectors and assistant addresses. This is a fixed phrase grammar and narrowly allowed spelling normalization, not arbitrary edit-distance or fuzzy matching of an entire request. Unknown tails pass to the ordinary question pipeline.

A greeting cannot consume “show scores,” student-ID/credential requests, game controls or unrelated subjects. URLs, email addresses and numeric identifiers are rejected by the social fast path before punctuation removal can turn them into innocent-looking words. Repeated greeting/thanks prefaces are removed for the normal request guard, leaving the actual subject or command intact. Social replies preserve the last validated typed context, contain no metric claims/evidence, and work without Ollama. A mixed system request still uses validated routing and fresh read-only analytics. Current all-source/default-period behavior and separate competitive cohorts remain unchanged.

The parser handles supported greeting structures rather than promising perfect understanding of every phrase or typo. Unsupported wording can still request clarification. Domain/privacy/control restrictions remain in force.

## Original synthetic dataset and measured token size

The new `backend/data/assistant-behavioral.json` contains **443** original, reproducibly generated examples:

| Kind | Records | Purpose |
|---|---:|---|
| Social compositions | 267 | Greetings, wellbeing, help, identity, thanks, acknowledgments and farewells, including spacing and elongation variants |
| Mixed greeting/system requests | 76 | Preserve the analytical or system-knowledge subject after a friendly preface |
| Typed follow-ups | 40 | Continue a validated previous subject while respecting named period/source/language changes |
| Boundary checks | 60 | Refuse private/control requests and keep unsupported measurements/unrelated topics outside the answer scope |

There are **343 runtime-training examples** and **100 evaluation-only examples**. The question and behavioral-reference response texts measure **18,977 tokens total**, comprising **14,739 training-text tokens** and **4,238 evaluation-text tokens**. Both the total and training text meet the user’s requested 10,000–30,000-token dataset range. Counts exclude JSON field names, labels, IDs and chat-template special tokens; they are not an estimate based on character count or a claimed number of completed training tokens.

Tokenization used [Qwen’s Qwen3-4B-Instruct-2507 tokenizer](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/blob/main/tokenizer.json) with `tokenizers==0.22.2` in the isolated project tool environment, not a new production dependency. The downloaded tokenizer SHA-256 is `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`. The checked-in `backend/data/assistant-behavioral-report.json` records the dataset checksum, splits, tokenizer and exact counting method. No model weights were downloaded for this measurement.

Expected responses are synthetic behavioral references, not saved live answers. They contain no real player records, identifiers, credentials or claimed live metric values. Production still uses reviewed backend response templates and fresh analytics; only normalized question/context/label demonstrations are retrieved. The entire corpus is never inserted into the model prompt. Existing retrieval caps remain three bounded examples.

Greeting/spelling variants sharing a semantic clause remain in the same split. Reused wording from earlier evaluation records stays evaluation-only. All new boundary records are test-only and never become runtime aliases, vocabulary or demonstrations. This reduces obvious normalized-input leakage, but a template-derived synthetic split is not evidence of real-world generalization or a measured model-accuracy gain.

Together with the earlier 66 routing and 125 interaction examples, the project now has **634 original records**: **473 runtime-training** and **161 evaluation-only**. This supersedes older combined-count and exact-alias-only descriptions. Private approved examples remain separate and owner-scoped. The combined corpus digest and normalizer revision participate in the context fingerprint; existing private examples need re-review after this update.

## Reproduce and run

Rebuild the deterministic original dataset from the project root:

```powershell
.\backend\.venv\Scripts\python.exe .\backend\build_synthetic_interactions.py
```

With the already-installed development tokenizer library and the downloaded tokenizer file, regenerate and remeasure:

```powershell
.\.tools\graphify-py313\Scripts\python.exe .\backend\build_synthetic_interactions.py --tokenizer .\.tools\nlp-datasets\qwen3-4b-instruct-tokenizer.json
```

The builder performs local file operations only, without a database, network or model request. Restart `npm run dev` after changing bundled corpora or backend code. Raw corpora and tool downloads stay outside Graphify inputs; this guide records their public provenance and architecture.

## Checks actually run

- Full backend suite: **140 tests passed**. Checks cover the exact reported phrase, joined spellings, elongated greetings, complete consumption, URLs/emails/identifiers, family splits, current-schema validation, old interaction regressions and system/private boundaries.
- Disposable authenticated API: `hello goodevening` and `hiiii goodmorning` returned conversational replies; a prefixed reset request was refused; a prefixed recipe request asked for system context. These synthetic warm API requests took approximately 0.02–0.03 seconds on this PC, not a service-level guarantee.
- Local Ollama plus disposable database: `hello goodevening, how many players registered?` routed to `get_event_summary` and honestly returned no matching data for the empty synthetic event. The temporary database was removed.
- Dataset generation and Qwen text-token measurement completed with a matching checksum report.

No frontend code was changed for this expansion. Browser/desktop visual acceptance, broad paraphrase accuracy, release load, fine-tuning and physical ESP32 integration were not established by these checks.
