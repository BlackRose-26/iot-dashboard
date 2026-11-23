"""Evaluation preparation checks; no candidate prompts become training fixtures."""
import pytest
from pydantic import ValidationError

from prepare_candidate_holdout import audit, followup


def test_overlap_audit_does_not_ignore_previous_context_or_case():
    rows = [{'id': 'candidate', 'question': 'An exact synthetic fixture sentence.', 'previous': {'source': 'device'}}]
    result = audit(rows, [('seen', 'AN EXACT synthetic fixture sentence!')])
    assert result['exact_raw_or_usable_normalized'] == [{'id': 'candidate', 'reference': 'seen'}]


def test_candidate_internal_duplicates_are_flagged_without_predictions():
    rows = [{'id': 'first', 'question': 'A fabricated evaluation fixture sentence.'},
            {'id': 'second', 'question': 'A fabricated evaluation fixture sentence!'}]
    result = audit(rows, [])
    assert result['within_candidate_duplicates'][0]['id'] == 'second'
    assert result['within_candidate_duplicates'][0]['other'] == 'first'
    assert not result['exact_raw_or_usable_normalized']


def test_missing_context_is_annotated_for_clarification_and_not_invented():
    assert followup('none', 'clarify') == (None, None, 'needs_clarification')


def test_followup_annotation_keeps_subject_and_validates_changed_filters():
    before, after, behavior = followup('accuracy_device_week', 'today')
    assert before['period'] == 'last_7_days' and after['period'] == 'today'
    assert before['tools'] == after['tools'] == ['get_event_summary']
    assert before['source'] == after['source'] == 'device'
    assert before['metrics'] == after['metrics'] == ['accuracy'] and behavior == 'answer'
    with pytest.raises(ValidationError):
        followup('levels_three', 'level_99')
