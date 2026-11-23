"""Validate the frozen-evaluation machinery without running any held-out prediction."""
from collections import Counter
import json

import pytest

import holdout_audit as audit
from holdout_metrics import summarize, wilson
from evaluate_holdout import score
from app.assistant_learning import RUNTIME_CORPORA


def test_inventory_is_balanced_diverse_and_excluded_from_runtime_corpora():
    rows=audit.build_rows()
    assert len(rows)==325
    assert Counter(row['target']['topic'] for row in rows)=={topic:25 for topic in audit.TOPICS}
    assert len({row['id'] for row in rows})==325
    assert min(len({r['family'] for r in rows if r['target']['topic']==topic}) for topic in audit.TOPICS)>=10
    assert set(r['language'] for r in rows)=={'en','taglish'}
    assert all(audit.DIRECTORY not in path.parents for path in RUNTIME_CORPORA)


def test_inventory_has_no_exact_or_high_lexical_overlap_with_seen_examples():
    result=audit.overlap_audit(audit.build_rows())
    assert result['reference_count']>=700
    for key in ('exact_collisions','near_duplicates','within_set_exact','within_set_near'):
        assert result[key]==[],(key,result[key])


def test_freezing_is_immutable_and_detects_runtime_drift(tmp_path,monkeypatch):
    monkeypatch.setattr(audit,'DATASET',tmp_path/'cases.json')
    monkeypatch.setattr(audit,'MANIFEST',tmp_path/'manifest.json')
    audit.freeze()
    assert audit.verify_frozen()[0]['n']==325
    with pytest.raises(ValueError,match='already frozen'): audit.freeze()
    monkeypatch.setattr(audit,'runtime_fingerprint',lambda:{'changed':True})
    with pytest.raises(ValueError,match='fingerprint'): audit.verify_frozen()


def test_refusals_and_provider_errors_remain_in_the_denominator():
    rows=[]
    for topic,result in [('queue',{'status':'needs_clarification'}),('unsupported',{'status':'refused'}),('scores',{'status':'error'})]:
        row={'id':topic,'family':topic,'language':'en','target':{'topic':topic}}
        rows.append(score(row,result,None))
    measured=summarize(rows,('queue','unsupported','scores'))
    assert measured['n']==3 and measured['accepted']==1
    assert measured['accepted_accuracy']==pytest.approx(1/3)
    assert measured['valid_request_clarifications']==1 and measured['unavailable_or_errors']==1
    # The queue false-positive lowers unsupported precision to 1/2: F1=2/3.
    assert measured['macro_f1']==pytest.approx(2/9)
    assert wilson(0,25)[0]==pytest.approx(0,abs=1e-12)
    assert wilson(25,25)[1]==pytest.approx(1,abs=1e-12)


def test_follow_up_scope_must_be_correct_and_equivalents_do_not_inflate_exact_labels():
    row={'id':'synthetic','family':'synthetic','language':'en','target':{'topic':'follow_up'},
         'previous':{'tools':['get_player_scores']},'expected_context':{'source':'device'}}
    result=score(row,{'status':'ok','context':{'source':'simulator'}},{'topic':'follow_up'})
    assert result['exact_label'] and not result['accepted']
    row={'id':'synthetic','family':'synthetic','language':'en','target':{'topic':'social','social':'help'},
         'acceptable_labels':['social:help','knowledge:assistant']}
    result=score(row,{'status':'conversation','context':{}},{'topic':'knowledge','knowledge':'assistant'})
    assert result['accepted'] and not result['exact_label']
