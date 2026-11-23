"""Report the fixed history ablation on consumed development cohorts."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
from experiment_history import BASE, manifest
from nlp_lab.run import sha, write
from summarize_offline_lab import metrics


def publish(directory):
    protocol, base, rows, external = manifest(directory)
    old = json.loads((BASE / 'e5-frozen-linear.json').read_text(encoding='utf-8'))
    old_context = json.loads((BASE / 'context-stress.json').read_text(encoding='utf-8'))
    expected = {row['id']: row['label'] for row in external}
    stress_expected = {key: value for key, value in expected.items() if value != 'follow_up'}
    candidates = {}
    for name in protocol['candidates']:
        result = json.loads((directory / (name + '.json')).read_text(encoding='utf-8'))
        if result['protocol_sha256'] != sha(directory / 'protocol.json'):
            raise ValueError('Candidate protocol mismatch.')
        first = result['reports']['consumed_balanced_development']['cases']
        stress = result['reports']['paired_context_stress']['cases']
        if len(first) != 130 or {c['id']: c['expected'] for c in first} != expected:
            raise ValueError('Development labels or cohort changed.')
        if len(stress) != 120 or {c['id']: c['expected'] for c in stress} != stress_expected:
            raise ValueError('Paired diagnostic labels or cohort changed.')
        candidates[name] = {
            'original': metrics(first), 'context_stress': metrics(stress),
            'by_language': {lang: metrics([c for c in first if c['language'] == lang])
                            for lang in sorted({c['language'] for c in first})},
            'changed_labels_under_unrelated_history': result['changed_labels_under_unrelated_history'],
            'policy': result['policy'], 'calibration': result['calibration'],
            'result_sha256': sha(directory / (name + '.json')), 'cases': first, 'context_cases': stress,
        }
    summary = {
        'run': directory.name, 'status': 'consumed development regression; no production promotion',
        'limits': protocol['limits'], 'new_independent_questions': 0,
        'experiment_protocol_sha256': sha(directory / 'protocol.json'),
        'source_training_n': protocol['original_admitted_train'],
        'augmented_training_n': protocol['augmented_train_rows'],
        'reference_frozen_e5': metrics(old['reports']['balanced_new_development']['cases']),
        'reference_frozen_e5_stress': old_context['candidates']['e5-frozen-linear'],
        'candidates': candidates,
    }
    write(ROOT / 'docs/nlp-evaluation/results/history-lab-20261120.json', summary)
    lines = [
        '# History shortcut: offline representation and training experiment', '',
        '20 November 2026. **Consumed development regression only; no live model replacement.** '
        'This follow-on investigates the shortcut found in the [first experiment](offline-lab-20261120.md). '
        'It preserves that run, the original 325-case benchmark and the live assistant.', '',
        '## Fixed comparison', '',
        f"The original {protocol['original_admitted_train']} admitted training rows yield {protocol['augmented_train_rows']} rows after "
        f"label-preserving history augmentation. These are {protocol['augmented_train_rows'] - protocol['original_admitted_train']} variants of existing training questions, **zero newly independent questions**. "
        'Three different typed prior subjects are added only to original training rows without a previous subject. '
        'Existing contextual/follow-up rows retain their actual subject. Family membership and the original train/calibration boundary remain intact.', '',
        'The encoder remains frozen multilingual E5. All candidates fit balanced hierarchical logistic heads. '
        'One uses augmented history-bearing inputs; one classifies the current question only on the original training rows; '
        'one combines current-question classification with augmentation. Typed state remains available to a separate reducer after classification. '
        'No candidate runs factual tools, changes game data or trains Ollama weights.', '',
        'The protocol, augmentation, code and protected runtime hashes were frozen before these predictions. '
        'Confidence temperature and operating points use only the original calibration set. '
        'The same 130 inspected questions and paired 120-question misleading-history diagnostic are reused explicitly as regression data.', '',
        '| Candidate | Primary / 130 | Exact label / 130 | Context stress primary / 120 | Labels changed under added history / 120 |',
        '|---|---:|---:|---:|---:|',
    ]
    old_m = summary['reference_frozen_e5']; old_s = summary['reference_frozen_e5_stress']
    lines.append(f"| Original frozen E5, first experiment | {old_m['primary_correct']}/130 | {old_m['exact_correct']}/130 | {old_s['primary_correct_after']}/120 | See first experiment |")
    for name, value in candidates.items():
        m = value['original']; s = value['context_stress']
        lines.append(f"| {name} | {m['primary_correct']}/130 | {m['exact_correct']}/130 | {s['primary_correct']}/120 | {value['changed_labels_under_unrelated_history']}/120 |")
    lines += ['', '![Measured history experiment](history-lab-comparison.png)', '',
              '## Coverage, exactness and limitations', '',
              'History augmentation improved the reused context-stress count from 14/120 to 47/120, but ordinary primary matches fell from 63/130 to 61/130. '
              'Question-only classification removed history-induced label changes by construction, while reaching only 60/130 primary matches and answering one supported question under its calibrated policy. None is adequate for promotion.', '',
              'The original frozen development inputs also show 40/120 supported questions blocked before classification. Across all 130 questions, '
              'the recorded gate outcomes are 84 admitted, 31 unrecognized-context, 14 system-scope and one unsupported-measurement. '
              'Even perfect classification of admitted inputs cannot repair those supported refusals. The next design review must separate '
              'privacy/control refusal, unsupported meaning and unfamiliar wording without exposing identifiers or removing guards blindly.', '',
              '| Candidate | Supported answered / 120 | Primary correct among answered | Exact among answered | OOS false accepts: raw / policy (out of 10) |',
              '|---|---:|---:|---:|---:|']
    for name, value in candidates.items():
        m = value['original']; n = m['answered_valid_n']
        prim = f"{m['answered_primary_correct']}/{n}" if n else 'N/A (no answers)'
        exact = f"{m['answered_exact_correct']}/{n}" if n else 'N/A (no answers)'
        lines.append(f"| {name} | {n}/120 | {prim} | {exact} | {m['oos_raw_false_accepts']} / {m['oos_policy_false_accepts']} |")
    lines += ['',
              'Question-only history invariance is an architectural property, not proof of understanding. '
              'A consistently wrong answer is still wrong. Primary topics alone do not validate subtype, filters, resolved context, '
              'tool choice or factual correctness. The prototype has not replaced the live state resolver.', '',
              'Synthetic augmentation assumes the source label survives unrelated history; those assumptions still need review. '
              'It adds no language diversity, missing definition subtypes or independently authored intent families. '
              'Duplicating training rows can also affect regularization; the question-only with/without augmentation comparison exposes that difference. '
              'The small, already inspected regression cohort cannot establish unseen generalization or justify production promotion.', '',
              'The independent 325-slot collection still has zero filled questions. Next: independently reviewed rare-class/new-topic/follow-up families, '
              'new separate development validation and a frozen independent final evaluation before any promotion.', '',
              '## Evidence', '',
              f'- Retained protocol, variants, candidate heads and predictions: `.tools/nlp-lab/{directory.name}/`.',
              '- [Case-level summary and hashes](results/history-lab-20261120.json).',
              '- [Experiment code](../../backend/experiment_history.py), [summary generator](summarize_history_lab.py), [plot source](plot_history_lab.py).',
              '- Four new checks verify partition admission, unchanged labels/families, contextual-example preservation and current-question history invariance; all fourteen offline checks passed.',
              '- [Implementation guide](../nlp-offline-experiment.md) and [label guide](../nlp-label-guide.md).', '']
    with (ROOT / 'docs/nlp-evaluation/history-lab-20261120.md').open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines))
    print(json.dumps({name: {'primary': c['original']['primary_correct'], 'context': c['context_stress']['primary_correct']}
                      for name, c in candidates.items()}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run):
        raise ValueError('Invalid run ID')
    publish(ROOT / '.tools/nlp-lab' / args.run)
