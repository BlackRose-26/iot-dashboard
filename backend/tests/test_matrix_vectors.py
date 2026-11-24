"""The web game screen's engine (frontend/src/screen/engine.js) is checked against these
same vectors in vitest; here every expected trace must pass the server's replay()."""
import json
from pathlib import Path

from app.game import MATRIX_RULES, replay, rules_hash

VECTORS = json.loads((Path(__file__).resolve().parents[2] / 'contracts' / 'matrix-v1.vectors.json').read_text(encoding='utf-8'))


def test_vectors_use_the_current_matrix_rules():
    assert VECTORS['rules'] == MATRIX_RULES
    assert VECTORS['rulesHash'] == rules_hash(MATRIX_RULES).hex()


def test_every_vector_replays_with_its_score():
    assert len(VECTORS['vectors']) >= 10
    outcomes = {v['expected']['outcome'] for v in VECTORS['vectors']}
    assert outcomes == {'win', 'loss'}
    for vector in VECTORS['vectors']:
        expected = vector['expected']
        result = replay(expected['placements'], expected['durationMs'], expected['outcome'], MATRIX_RULES)
        assert result['score'] == expected['score'], vector['name']
