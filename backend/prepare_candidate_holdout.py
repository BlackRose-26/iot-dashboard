"""Authoring/overlap audit only. Never runs predictions or approves its own labels."""
import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
from collections import Counter
import ast
import csv
from difflib import SequenceMatcher
import json
from pathlib import Path
import re

from app.assistant import Context
from app.assistant_training import TrainingTarget
from holdout_audit import STOP, feature_key, reference_questions, runtime_fingerprint, text_key
from nlp_lab.data import ROOT, TOPICS, sha

DIRECTORY = ROOT / '.tools/nlp-lab/review'
SOURCE = DIRECTORY / 'candidate-authoring-v2.json'

CONTEXTS = {
    'scores_today': Context(tools=['get_player_scores'], period='today'),
    'wins_week': Context(tools=['get_event_summary'], metrics=['wins'], period='last_7_days'),
    'trend_today': Context(tools=['get_play_trend'], period='today'),
    'scores_all': Context(tools=['get_player_scores']),
    'top_device': Context(tools=['get_top_scores'], source='device'),
    'summary_device': Context(tools=['get_event_summary'], source='device'),
    'distribution_yesterday': Context(tools=['get_score_distribution'], period='yesterday'),
    'scores_page_two': Context(tools=['get_player_scores'], score_page=2),
    'scores_page_four': Context(tools=['get_player_scores'], score_page=4),
    'knowledge_registration': Context(knowledge='registration'),
    'knowledge_privacy_detail': Context(knowledge='privacy', detailed=True),
    'summary_today': Context(tools=['get_event_summary'], period='today'),
    'levels_eight': Context(tools=['get_level_statistics'], level=8),
    'levels_three': Context(tools=['get_level_statistics'], level=3),
    'top_two': Context(tools=['get_top_scores'], limit=2),
    'top_three': Context(tools=['get_top_scores'], limit=3),
    'scores_sim_today': Context(tools=['get_player_scores'], source='simulator', period='today'),
    'accuracy_device_week': Context(tools=['get_event_summary'], metrics=['accuracy'], source='device', period='last_7_days'),
    'definition_total': Context(definition='total_score'),
    'knowledge_queue': Context(knowledge='queue_flow'),
    'duration_today': Context(tools=['get_event_summary'], metrics=['average_duration'], period='today'),
    'timeouts_all': Context(tools=['get_event_summary'], metrics=['timeouts']),
    'summary_detail': Context(tools=['get_event_summary'], detailed=True),
}


def followup(previous_key, update):
    if previous_key == 'none':
        return None, None, 'needs_clarification'
    previous = CONTEXTS[previous_key].model_dump()
    expected = dict(previous)
    if update in ('today', 'yesterday', 'last_7_days', 'event_to_date'):
        expected['period'] = update
    elif update in ('all', 'device', 'simulator'):
        expected['source'] = update
    elif update == 'next_page':
        expected['score_page'] += 1
    elif update in ('detailed', 'brief'):
        expected['detailed'] = update == 'detailed'
    elif update.startswith('level_'):
        expected['level'] = int(update.split('_')[1])
    elif update.startswith('limit_'):
        expected['limit'] = int(update.split('_')[1])
    else:
        raise ValueError('Unknown annotated follow-up update.')
    return previous, Context.model_validate(expected).model_dump(), 'answer'


def build(payload):
    if set(payload['groups']) != set(TOPICS):
        raise ValueError('Exactly thirteen intent groups are required.')
    rows = []
    translation_map = {
        'overview': [2, 0, 4, 5, 3, 8, 11, 9, 10, 12, 0, 4],
        'players': [0, 1, 11, 3, 4, 5, 6, 7, 8, 10, 2, 12],
        'queue': [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12],
        'machine': list(range(12)),
        'scores': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
        'levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
        'trend': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
        'top': list(range(12)),
    }
    for topic in TOPICS:
        lines = payload['groups'][topic]
        if len(lines) != 25:
            raise ValueError(f'{topic}: expected25, got{len(lines)}')
        for index, line in enumerate(lines):
            parts = line.split('|')
            scenario, language, question = parts[:3]
            target = {'topic': topic}
            family = scenario
            if topic in ('definition', 'knowledge', 'social'):
                target[topic] = parts[3]
                family = parts[3]
            elif topic in translation_map and index >= 13:
                family = lines[translation_map[topic][index-13]].split('|')[0]
            target = TrainingTarget.model_validate(target).model_dump(exclude_none=True)
            if language not in ('en', 'taglish') or not question.strip():
                raise ValueError('Question/language annotation missing.')
            if re.search(r'\d{4,}|[\w.+-]+@[\w.-]+|https?://|-----BEGIN', question, re.I):
                raise ValueError('Private-looking candidate values are forbidden.')
            previous, expected, status = None, None, 'refused' if topic == 'unsupported' else 'answer'
            if topic == 'follow_up':
                previous, expected, status = followup(parts[3], parts[4])
            elif index % 3 == 1:
                candidates = [Context(knowledge='offline'), Context(tools=['get_queue_summary']),
                              Context(tools=['get_player_scores'], source='device', period='yesterday')]
                previous = candidates[(index // 3) % 3].model_dump()
            rows.append({
                'id': f'fresh-{topic}-{index+1:02d}', 'quota_topic': topic,
                'question': question, 'target': target, 'previous': previous,
                'expected_context': expected, 'expected_behavior': status,
                'language': language, 'family': topic + '/' + family, 'scenario': scenario,
                'author_code': 'ai-author-v2', 'reviewer_code': '',
                'privacy_checked': False, 'review_status': 'pending',
                'label_provenance': 'AI-authored proposed label; not independent gold',
                'review_notes': 'Check semantic label, privacy, scope and expected state without consulting predictions.',
            })
    assert len(rows) == 325 and len({r['id'] for r in rows}) == 325
    return rows


def references():
    # Locally compare evaluation text; never return it to a model, runtime
    # corpus, graph input or log. Frozen old prompts stay evaluation-only.
    result = reference_questions()
    old = ROOT / 'backend/evaluation/holdout-v1.json'
    value = json.loads(old.read_text(encoding='utf-8'))
    result += [('consumed-v1/' + r['id'], r['question']) for r in value['examples']]
    lab = ROOT / 'backend/nlp_lab/data'
    negatives = json.loads((lab / 'ood-development.json').read_text(encoding='utf-8'))
    result += [('lab-negatives/' + name + '/' + str(i), q)
               for name, questions in negatives['families'].items() for i, q in enumerate(questions)]
    balanced = json.loads((lab / 'balanced-development.json').read_text(encoding='utf-8'))
    result += [('consumed-balanced/' + str(i), line.split('|', 3)[3]) for i, line in enumerate(balanced['cases'])]
    probes = json.loads((lab / 'public-diagnostics.json').read_text(encoding='utf-8'))
    result += [('public-wording/' + r['id'], r['question']) for r in probes['examples']]
    # Include newer public probe scripts, test literals and static assistant
    # prompt/example wording that postdate the original v1 reference collector.
    paths = set((ROOT / 'backend/tests').glob('*.py'))
    paths.update((ROOT / 'backend').glob('check_*.py'))
    paths.update((ROOT / 'backend/app').glob('assistant*.py'))
    for path in sorted(paths):
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value.split()) >= 3:
                result.append((path.relative_to(ROOT).as_posix() + '/L' + str(node.lineno), node.value))
    return result


def audit(rows, refs):
    exact = {text_key(q): identity for identity, q in refs}
    normalized = {key: identity for identity, q in refs if (key := feature_key(q))}
    prepared = [(identity, text_key(q), set(text_key(q).split()) - STOP) for identity, q in refs]
    collisions, near, within = [], [], []
    seen, seen_features = {}, {}
    for row in rows:
        value = text_key(row['question']); words = set(value.split()) - STOP
        features = feature_key(row['question'])
        match = exact.get(value) or (normalized.get(features) if features else None)
        if match:
            collisions.append({'id': row['id'], 'reference': match})
        if value in seen or (features and features in seen_features):
            within.append({'id': row['id'], 'other': seen.get(value) or seen_features[features]})
        seen[value] = row['id']
        if features:
            seen_features[features] = row['id']
        for identity, prior, prior_words in prepared:
            overlap = len(words & prior_words) / len(words | prior_words) if words | prior_words else 0
            if len(value) >= 24 and overlap >= .7 and SequenceMatcher(None, value, prior, autojunk=False).ratio() >= .84:
                near.append({'id': row['id'], 'reference': identity})
    for i, row in enumerate(rows):
        value = text_key(row['question']); words = set(value.split()) - STOP
        for other in rows[i+1:]:
            prior = text_key(other['question']); prior_words = set(prior.split()) - STOP
            overlap = len(words & prior_words) / len(words | prior_words) if words | prior_words else 0
            if len(value) >= 24 and overlap >= .7 and SequenceMatcher(None, value, prior, autojunk=False).ratio() >= .84:
                within.append({'id': row['id'], 'other': other['id'], 'kind': 'lexical-near'})
    return {'reference_count': len(refs), 'exact_raw_or_usable_normalized': collisions,
            'high_lexical_near': near, 'within_candidate_duplicates': within,
            'policy': 'Raw/usable-normalized equality; lexical near: content Jaccard>=.70 AND character similarity>=.84. No threshold tuning against predictions.',
            'semantic_review': 'Pending; automated non-overlap does not establish human-reviewed semantic independence.'}


def main():
    before = json.loads((DIRECTORY / 'candidate-authoring-v2.protocol.json').read_text(encoding='utf-8'))
    if runtime_fingerprint() != before['predictor_before_candidate_authoring']:
        raise ValueError('Predictor changed during candidate preparation.')
    rows = build(json.loads(SOURCE.read_text(encoding='utf-8')))
    result = audit(rows, references())
    flagged = {v['id'] for key in ('exact_raw_or_usable_normalized', 'high_lexical_near', 'within_candidate_duplicates') for v in result[key]}
    for row in rows:
        row['overlap_status'] = 'needs_replacement_or_adjudication' if row['id'] in flagged else 'automated_checks_clear'
    packet = {'status': 'filled_ai_authored_review_pending', 'required_filled_cases': 325,
              'instructions': 'All325 questions/labels are AI-authored candidates. Review blind to predictions; do not attest independent human review unless it actually occurs. Do not train on these questions.',
              'authoring_source_sha256': sha(SOURCE), 'entries': rows}
    target = DIRECTORY / 'holdout-v2-collection.json'
    current = json.loads(target.read_text(encoding='utf-8'))
    if any(r['review_status'] == 'approved' for r in current['entries']):
        raise ValueError('Cannot replace independently approved entries.')
    backup = DIRECTORY / 'holdout-v2-collection.blank-template.json'
    if not backup.exists():
        if any(r['question'].strip() for r in current['entries']):
            raise ValueError('Blank template backup missing for existing filled collection.')
        with backup.open('x', encoding='utf-8') as stream:
            json.dump(current, stream, indent=2)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding='utf-8')
    with (DIRECTORY / 'holdout-v2-review.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = ['id', 'language', 'family', 'question', 'proposed_target', 'previous',
                  'expected_behavior', 'expected_context', 'overlap_status',
                  'reviewer_code', 'review_decision', 'corrected_target', 'review_notes']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                **{key: row[key] for key in ('id', 'language', 'family', 'question', 'expected_behavior', 'overlap_status')},
                'proposed_target': json.dumps(row['target'], ensure_ascii=False),
                'previous': json.dumps(row['previous'], ensure_ascii=False),
                'expected_context': json.dumps(row['expected_context'], ensure_ascii=False),
                'reviewer_code': '', 'review_decision': '', 'corrected_target': '',
                'review_notes': row['review_notes'],
            })
    result.update(filled=325, independently_approved=0, predictions_run=0,
                  per_primary=dict(Counter(r['target']['topic'] for r in rows)),
                  per_language=dict(Counter(r['language'] for r in rows)),
                  families_per_primary={topic: len({r['family'] for r in rows if r['target']['topic'] == topic}) for topic in TOPICS},
                  with_previous=sum(r['previous'] is not None for r in rows),
                  packet_sha256=sha(target), source_sha256=sha(SOURCE), flagged_candidate_n=len(flagged))
    (DIRECTORY / 'candidate-authoring-v2.audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
