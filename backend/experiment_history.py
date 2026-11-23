"""Offline history-shortcut experiment on consumed DEVELOPMENT cohorts only.

The previous experiment and runtime remain unchanged. No final holdout inputs
are read, annotated, copied or trained on by this experiment.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'docs/nlp-evaluation'))
from audit_lab_context import open_run
from nlp_lab.run import MODEL, sha, write, protected, evaluate_model, summarize
from nlp_lab.data import text
from nlp_lab.models import DenseModel, fit_temperature, scaled, policy
from app.assistant import Context

BASE = ROOT / '.tools/nlp-lab/intent-lab-20261120-02'


def training_variants(rows):
    """Training-only typed-history augmentation; not new independent questions."""
    contexts = [
        Context(tools=['get_machine_summary'], source='device', period='last_7_days').model_dump(),
        Context(knowledge='architecture').model_dump(),
        Context(tools=['get_top_scores'], period='today', source='all', limit=3).model_dump(),
    ]
    result = []
    for row in rows:
        if row['partition'] != 'train':
            raise ValueError('Only original training rows may be augmented.')
        if row['blocked']:
            continue
        result.append({**row, 'augmentation': 'original'})
        # Existing contextual/follow-up examples keep their actual typed subject.
        # A new, explicit current request must not become a follow-up merely
        # because unrelated history was supplied. Never change its target label.
        if row['previous'] is None and row['label'] != 'follow_up':
            for i, previous in enumerate(contexts):
                result.append({**row, 'id': row['id'] + f':history-variant-{i}',
                               'previous': previous, 'augmentation': 'unrelated-history',
                               'origin_id': row['id']})
    return result, contexts


def question_only(row):
    # Topic/act classification sees only the current admitted question. Typed
    # history remains available for the separate frame reducer after routing.
    return text({**row, 'previous': None})


class QuestionOnly:
    def __init__(self, model):
        self.model = model

    def predict(self, texts):
        suffix = ' [validated previous context: '
        return self.model.predict([value.split(suffix, 1)[0] for value in texts])


def manifest(directory):
    value = json.loads((directory / 'protocol.json').read_text(encoding='utf-8'))
    protocol, rows, external = open_run(BASE)
    if value['experiment_code_sha256'] != sha(Path(__file__)) or value['protected'] != protected():
        raise ValueError('Frozen experiment or runtime changed.')
    if value['base_protocol_sha256'] != sha(BASE / 'protocol.json'):
        raise ValueError('Base protocol changed.')
    if value['prepared_data_sha256'] != sha(directory / 'training.json'):
        raise ValueError('Frozen training variants changed.')
    return value, protocol, rows, external


def prepare(directory):
    protocol, rows, external = open_run(BASE)
    training = [rows[i] for i in protocol['splits']['train']]
    variants, contexts = training_variants(training)
    directory.mkdir(parents=True, exist_ok=False)
    write(directory / 'training.json', variants)
    write(directory / 'protocol.json', {
        'status': 'frozen-development-regression-only',
        'purpose': 'History augmentation and question-only primary classification. No live activation.',
        'base_protocol_sha256': sha(BASE / 'protocol.json'),
        'experiment_code_sha256': sha(Path(__file__)), 'protected': protected(),
        'prepared_data_sha256': sha(directory / 'training.json'),
        'original_admitted_train': sum(not row['blocked'] for row in training),
        'augmented_train_rows': len(variants),
        'new_independent_questions': 0,
        'augmented_counts': dict(Counter(row['target']['topic'] for row in variants)),
        'augmentation_contexts': contexts,
        'cohorts': 'Same original calibration, consumed 130-case development and paired 120-case context stress. No new unseen accuracy.',
        'candidates': ['e5-history-augmented', 'e5-question-only', 'e5-question-only-augmented'],
        'learning': 'Frozen E5 encoder; balanced hierarchical logistic heads only. No encoder/LLM weight updates.',
        'calibration': 'Same calibration-only temperature and operating-point procedure; no diagnostic labels used to select thresholds.',
        'limits': 'Synthetic label-preserving history variants need review. They do not add language diversity or independently authored families. Question-only classification still needs typed context resolution and missing-context handling.',
    })
    print(json.dumps({'directory': str(directory), 'training_rows': len(variants),
                      'new_independent_questions': 0}, indent=2), flush=True)


def run(directory):
    protocol, base, rows, external = manifest(directory)
    import torch
    torch.set_num_threads(4)
    from sentence_transformers import SentenceTransformer
    from nlp_lab.models import Heads
    import joblib
    original = [rows[i] for i in base['splits']['train'] if not rows[i]['blocked']]
    augmented = json.loads((directory / 'training.json').read_text(encoding='utf-8'))
    calibration = [rows[i] for i in base['splits']['calibration'] if not rows[i]['blocked']]
    stress_meta = json.loads((BASE / 'context-stress.protocol.json').read_text(encoding='utf-8'))
    stressed = [{**row, 'previous': stress_meta['contexts'][i % 3]}
                for i, row in enumerate(row for row in external if row['label'] != 'follow_up')]
    encoder = SentenceTransformer(str(MODEL), device='cpu', local_files_only=True, trust_remote_code=False)
    encoder.max_seq_length = 256
    for name in protocol['candidates']:
        if (directory / (name + '.json')).exists():
            raise ValueError('Candidate result exists; preserve it and use a new run.')
        began = time.perf_counter()
        source = original if name == 'e5-question-only' else augmented
        without_history = 'question-only' in name
        input_text = question_only if without_history else text
        core = DenseModel(encoder)
        features = core.encode([input_text(row) for row in source])
        core.heads = Heads().fit(features, source)
        candidate = QuestionOnly(core) if without_history else core
        labels, probabilities = candidate.predict([text(row) for row in calibration])
        truth = [row['target']['topic'] for row in calibration]
        temperature = fit_temperature(probabilities, truth, core.heads.primary.classes_)
        operating = policy(scaled(probabilities, temperature['temperature']), truth, core.heads.primary.classes_)
        reports = {}
        for label, cohort in [('consumed_balanced_development', external), ('paired_context_stress', stressed)]:
            cases = evaluate_model(candidate, cohort, 'original', operating, temperature['temperature'])
            reports[label] = {'counts': summarize(cases), 'cases': cases}
        # For the question-only architecture every non-follow-up question must
        # have identical primary/subtype decisions under changed typed history.
        lookup = {c['id']: c for c in reports['consumed_balanced_development']['cases']}
        changes = sum(lookup[c['id']]['predicted'] != c['predicted']
                      for c in reports['paired_context_stress']['cases'])
        if without_history and changes:
            raise ValueError('Question-only history-invariance contract failed.')
        joblib.dump(core.heads, directory / (name + '-heads.joblib'))
        manifest(directory)
        value = {'candidate': name, 'scope': protocol['cohorts'], 'training_rows': len(source),
                 'training_seconds': time.perf_counter() - began,
                 'calibration': temperature, 'policy': operating, 'changed_labels_under_unrelated_history': changes,
                 'protocol_sha256': sha(directory / 'protocol.json'), 'reports': reports}
        write(directory / (name + '.json'), value)
        print(json.dumps({'candidate': name, 'balanced': reports['consumed_balanced_development']['counts'],
                          'context': reports['paired_context_stress']['counts'], 'changed_labels': changes}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'run'])
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run):
        raise ValueError('Invalid run ID')
    target = ROOT / '.tools/nlp-lab' / args.run
    (prepare if args.stage == 'prepare' else run)(target)
