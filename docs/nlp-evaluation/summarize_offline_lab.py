"""Publish measured DEVELOPMENT results without changing the frozen experiment."""
import argparse
from collections import Counter
import json
from pathlib import Path

from audit_lab_context import ROOT, open_run
from nlp_lab.run import sha, write

NAMES = ['ollama-v11', 'tfidf-original', 'tfidf-normalized',
         'e5-frozen-linear', 'setfit-multilingual']
TITLES = ['Current Ollama routing adapter', 'TF-IDF original', 'TF-IDF normalized',
          'Frozen multilingual E5 + heads', 'Trained multilingual SetFit + heads']


def primary(label):
    return label.split(':')[0]


def metrics(cases):
    from sklearn.metrics import f1_score
    from nlp_lab.data import TOPICS
    valid = [c for c in cases if primary(c['expected']) != 'unsupported']
    answered = [c for c in valid if c.get('decision', 'answer') == 'answer'
                and primary(c['predicted']) in TOPICS and c['predicted'] != 'unsupported']
    oos = [c for c in cases if c['expected'] == 'unsupported']
    return {
        'n': len(cases),
        'primary_correct': sum(primary(c['expected']) == primary(c['predicted']) for c in cases),
        'exact_correct': sum(c['expected'] == c['predicted'] for c in cases),
        'primary_macro_f1': float(f1_score(
            [primary(c['expected']) for c in cases], [primary(c['predicted']) for c in cases],
            labels=list(TOPICS), average='macro', zero_division=0)),
        'valid_n': len(valid), 'answered_valid_n': len(answered),
        'answered_primary_correct': sum(primary(c['expected']) == primary(c['predicted']) for c in answered),
        'answered_exact_correct': sum(c['expected'] == c['predicted'] for c in answered),
        'oos_n': len(oos),
        'oos_raw_false_accepts': sum(primary(c['predicted']) in TOPICS and c['predicted'] != 'unsupported' for c in oos),
        'oos_policy_false_accepts': sum(c.get('decision', 'answer') == 'answer' and primary(c['predicted']) in TOPICS
                                      and c['predicted'] != 'unsupported' for c in oos),
        'errors': sum(c['predicted'] == 'error' for c in cases),
    }


def publish(directory, output):
    protocol, rows, external = open_run(directory)
    context = json.loads((directory / 'context-stress.json').read_text(encoding='utf-8'))
    tokenizer = json.loads((directory / 'tokenizer-context-verification.json').read_text(encoding='utf-8'))
    training = json.loads((directory / 'setfit-training.json').read_text(encoding='utf-8'))
    expected = {r['id']: r['label'] for r in external}
    candidates = {}
    files = ['protocol', 'data', 'context-stress', 'context-stress.protocol',
             'tokenizer-context-verification', 'setfit-training']
    for name, title in zip(NAMES, TITLES):
        result = json.loads((directory / (name + '.json')).read_text(encoding='utf-8'))
        reports = result['reports']
        cases = reports['balanced_new_development']['cases']
        if len(cases) != len(expected) or {c['id']: c['expected'] for c in cases} != expected:
            raise ValueError('Candidate cohort or gold labels differ.')
        measured = metrics(cases)
        stored = reports['balanced_new_development']['argmax']
        if measured['primary_correct'] != stored['primary_correct'] or measured['exact_correct'] != stored['exact_label_correct']:
            raise ValueError('Stored counts differ from retained predictions.')
        language = {lang: metrics([c for c in cases if c['id'] in {r['id'] for r in external if r['language'] == lang}])
                    for lang in sorted({r['language'] for r in external})}
        diagnostic = {key: metrics(value['cases']) for key, value in reports.items() if 'wording' in key}
        candidates[name] = {
            'title': title, 'balanced_development': measured, 'by_language': language,
            'grouped_source_seen_development': metrics(reports['grouped_source_development']['cases']),
            'wording_diagnostics': diagnostic,
            'policy': result.get('policy'), 'calibration': result.get('calibration'),
            'context_stress': context['candidates'][name],
            'cases': cases,
        }
        files.append(name)
    packet = json.loads((ROOT / '.tools/nlp-lab/review/holdout-v2-collection.json').read_text(encoding='utf-8'))
    filled = sum(bool(row['question'].strip()) for row in packet['entries'])
    if filled:
        raise ValueError('Collection changed; update review accounting before publishing.')
    summary = {
        'status': 'development-only; no candidate promoted', 'run': directory.name,
        'limits': '130 developer-labelled synthetic development cases; 10 per primary intent. No independent human gold, factual-answer evaluation or fresh unseen accuracy claim.',
        'baseline_label_mapping': 'Guard-aware routing outcomes: both refused and needs_clarification map to unsupported. Stored baseline rows cannot separate those statuses; baseline is not unconstrained Ollama argmax.',
        'original_consumed_325_preserved': True,
        'evidence_sha256': {name + '.json': sha(directory / (name + '.json')) for name in files},
        'audit': protocol['audit'], 'grouping': protocol['grouping'],
        'split_rows': {k: len(v) for k, v in protocol['splits'].items()},
        'history_training_confound': dict(Counter(
            'follow_up_with_previous' if r['label'] == 'follow_up' else 'other_with_previous'
            for r in rows if r['previous'])),
        'setfit_training': training, 'tokenizer_verification': tokenizer,
        'independent_review': {'required': 325, 'filled': filled, 'approved': 0, 'status': 'pending'},
        'candidates': candidates,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, summary)
    lines = [
        '# Local NLP comparison — measured development results', '',
        '20 November 2026. **Decision: retain the current live router. No experimental model is activated.**', '',
        'All five candidates ran locally. These are routing labels on 130 new developer-labelled synthetic development questions '
        '(ten per primary intent), not independently reviewed unseen test accuracy or factual-answer correctness. '
        'The old 325-case benchmark remains consumed regression evidence and was not used as training data.', '',
        'The baseline adapter maps both refusal and clarification to `unsupported`; stored baseline rows cannot distinguish those statuses. '
        'Its label counts are guard-aware routing outcomes, whereas the learned-model label counts use argmax after admission guards. '
        'This is a pipeline feasibility comparison, not a controlled claim that one bare model is more accurate.', '',
        '| Candidate | Primary correct / 130 | Exact label / 130 | Primary macro F1 |',
        '|---|---:|---:|---:|',
    ]
    for name in NAMES:
        c = candidates[name]; m = c['balanced_development']
        lines.append(f"| {c['title']} | {m['primary_correct']}/130 ({m['primary_correct']/1.3:.2f}%) | {m['exact_correct']}/130 | {m['primary_macro_f1']:.3f} |")
    lines += ['', 'Primary accuracy checks the topic; exact labels additionally require a knowledge/social/definition subtype. '
              'All guards, refusals and errors remain in the denominator. Ten cases per intent cannot establish reliable per-intent performance. '
              'The two-case difference between SetFit and the router is not evidence of a statistically established ranking.', '',
              '![Measured development comparison](offline-lab-comparison.png)', '',
              '## Coverage and abstention', '',
              'The learned models select confidence/margin thresholds using calibration data only, targeting at least 90% primary-routing '
              'precision and zero calibration out-of-scope false answers. This is an experimental selection target, not a proven safety guarantee. '
              'The current Ollama adapter retains its existing guard policy. These policies are different; report coverage alongside precision.', '',
              '| Candidate | Supported questions answered / 120 | Correct primary among answered | Exact among answered | OOS false accepts: raw / policy (out of 10) |',
              '|---|---:|---:|---:|---:|']
    for name in NAMES:
        c = candidates[name]; m = c['balanced_development']; n = m['answered_valid_n']
        prim = f"{m['answered_primary_correct']}/{n}" if n else 'N/A (no answers)'
        exact = f"{m['answered_exact_correct']}/{n}" if n else 'N/A (no answers)'
        lines.append(f"| {c['title']} | {n}/120 | {prim} | {exact} | {m['oos_raw_false_accepts']} / {m['oos_policy_false_accepts']} |")
    lines += ['', 'TF-IDF found no feasible calibration operating point and abstained on every supported question. '
              'Frozen E5 answered only eight supported questions. Neither zero false answers nor high precision on a small accepted subset '
              'establishes a useful assistant. No metric here evaluates the truth of an answer or database/tool correctness. '
              'All five runs recorded zero service errors.', '',
              '## Misleading-history diagnostic', '',
              'This post-hoc diagnostic reuses the same 120 non-follow-up questions with unrelated typed prior context. '
              'It is not 120 additional independent test cases. Model weights, labels and operating points were not changed.', '',
              '| Candidate | Primary correct before → after / 120 | Originally correct → wrong | Incorrect follow-up predictions after / 120 |',
              '|---|---:|---:|---:|']
    for name in NAMES:
        c = candidates[name]; m = c['context_stress']
        lines.append(f"| {c['title']} | {m['primary_correct_before']} → {m['primary_correct_after']} | {m['originally_correct_became_wrong']} | {m['predicted_follow_up_after']} |")
    lines += ['', 'The source pool contains 33 context-bearing follow-ups and **zero context-bearing explicit new topics** after deduplication. '
              'SetFit predicted follow-up for 73 unrelated new requests; 44 formerly correct primary predictions became wrong. '
              'This is a deployment blocker. Add matched explicit-topic-change and genuine-follow-up training families, keeping development and final evaluation separate.', '',
              '## Data and implementation audit', '',
              '- Original training material: 515 rows, including 315 social examples, only eight definitions and no unsupported class. Several metric-definition subtypes are absent.',
              '- Sixty lab-only synthetic negative examples were added. The lab removed 76 duplicate copies and quarantined five rows involved in three normalized conflicting pairs; it did not relabel the old benchmark.',
              '- Usable pool: 494 rows across 154 families/groups. Splits: 295 training, 98 calibration, 101 comparison. Of 494 rows, 472 pass current wording guards; blocked rows remain in comparisons.',
              '- The 130 new development inputs have zero exact or high lexical near matches against the source pool under the recorded audit rules. Semantic independence has not been human-adjudicated.',
              '- SetFit genuinely changed encoder weights: 40 contrastive steps on a capped 123-row training subset, then hierarchical heads on admitted training rows. This did not outperform the current router.',
              '- Baseline uses the actual routing path with no-data renderers and train-only retrieval; existing static prompt/social priors predate the split. Its 101 source-comparison cases are seen development. No database or private messages were used.',
              '- The saved XLM-R tokenizer emitted an upstream regex warning. Original and saved tokenizers produced identical encodings on all 250 actual balanced/context input strings. No model-specific regex patch was applied.', '',
              '## Unknown-word diagnostic', '',
              'Twenty fixed public synthetic wording probes were checked separately. Original-text counterfactuals bypass only wording gates '
              'for these reviewed public probes; privacy/control refusals cannot be bypassed. These rows are not training/calibration or independent evaluation.', '',
              '| Candidate | Current gate: primary / 20 | Reviewed original-text counterfactual: primary / 20 |',
              '|---|---:|---:|']
    for name in NAMES[1:]:
        c = candidates[name]; diagnostic = c['wording_diagnostics']
        gated = diagnostic['public_wording_gated']['primary_correct']
        counter = diagnostic.get('public_wording_reviewed_text_counterfactual')
        value = str(counter['primary_correct']) + '/20' if counter else 'Not run for normalized tokens'
        lines.append(f"| {c['title']} | {gated}/20 | {value} |")
    lines += ['', 'The counterfactual shows a wording-gate bottleneck and remaining model error; it does not authorize raw runtime inputs or removal of privacy guards.', '',
              '## Independent evaluation remains pending', '',
              'The collection packet contains **325 blank slots, zero questions and zero independently approved labels**. '
              'It is not a new test dataset. Collect and independently review twenty to fifty diverse cases per intent, '
              'audit all previously seen inputs for overlap, and freeze labels, predictor, decoder and scorer before first-use evaluation. '
              'The assistant cannot attest that its own generated labels received independent human review.', '',
              '## Evidence and reproduction', '',
              f'- Frozen local run: `.tools/nlp-lab/{directory.name}/`; model artifacts stay local and excluded from Graphify.',
              '- [Case-level measured summary](results/offline-lab-20261120.json) includes all predictions, language breakdowns, source-comparison results, fingerprints and calibration metadata.',
              '- [Offline implementation and commands](../nlp-offline-experiment.md) and [annotation guide](../nlp-label-guide.md).',
              '- [Summary generator](summarize_offline_lab.py), [plot source](plot_offline_lab.py), [paired context diagnostic](audit_lab_context.py).',
              '', '## Research applied', '',
              '[SetFit](https://huggingface.co/docs/setfit/v1.1.3/en/conceptual_guides/setfit) separates encoder adaptation from classifier training. '
              '[Multilingual E5](https://huggingface.co/intfloat/multilingual-e5-small) documents the query prefix used here. '
              '[Scikit-learn calibration guidance](https://scikit-learn.org/stable/modules/calibration.html) motivates disjoint calibration and transparent confidence reporting. '
              'Our results do not establish that this limited training recipe exhausts those approaches.', '']
    target = output.parent.parent / 'offline-lab-20261120.md'
    with target.open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines))
    print(json.dumps({'report': str(target), 'summary': str(output), 'runtime_hashes_unchanged': True,
                      'independent_cases_filled': filled}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run):
        raise ValueError('Invalid run ID')
    publish(ROOT / '.tools/nlp-lab' / args.run,
            ROOT / 'docs/nlp-evaluation/results/offline-lab-20261120.json')
