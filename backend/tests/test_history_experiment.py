"""Offline augmentation boundaries and current-question representation."""
import pytest

from app.assistant import Context
from experiment_history import QuestionOnly, question_only, training_variants
from nlp_lab.data import prepare, text


def training_row():
    rows, _ = prepare()
    row = next(r for r in rows if r['label'] == 'scores' and not r['blocked'] and not r['previous'])
    return {**row, 'partition': 'train'}


def test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows():
    row = training_row()
    for partition in ('calibration', 'comparison', 'validation', 'test'):
        with pytest.raises(ValueError, match='training'):
            training_variants([{**row, 'partition': partition}])
    assert training_variants([{**row, 'blocked': 'refused'}])[0] == []


def test_history_variants_keep_original_question_target_and_family():
    row = training_row()
    variants, contexts = training_variants([row])
    assert len(variants) == 4 and len(contexts) == 3
    assert {r['question'] for r in variants} == {row['question']}
    assert all(r['label'] == row['label'] and r['target'] == row['target'] for r in variants)
    assert all(r['family'] == row['family'] and r['partition'] == 'train' for r in variants)
    assert len({r['id'] for r in variants}) == 4
    assert {r['origin_id'] for r in variants[1:]} == {row['id']}


def test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject():
    row = training_row()
    previous = Context(tools=['get_queue_summary']).model_dump()
    for label in ('scores', 'follow_up'):
        original = {**row, 'label': label, 'previous': previous}
        variants, _ = training_variants([original])
        assert len(variants) == 1 and variants[0]['previous'] == previous


def test_question_only_features_do_not_change_with_any_validated_prior_subject():
    row = training_row()
    variants, _ = training_variants([row])
    assert len({text(r) for r in variants}) == 4
    assert len({question_only(r) for r in variants}) == 1
    captured = []
    class Capture:
        def predict(self, values):
            captured.extend(values)
            return None
    QuestionOnly(Capture()).predict([text(r) for r in variants])
    assert captured == [question_only(row)] * 4
    with pytest.raises(ValueError):
        question_only({**row, 'blocked': 'refused'})
