"""Offline experiment integrity; does not train models or access the database."""
import asyncio
import json

import numpy as np
import pytest
from pydantic import ValidationError

from app.assistant import Context,normalize
from nlp_lab.data import prepare,partitions,text,balanced_cases,TOPICS
from nlp_lab.frame import Frame,frame
from nlp_lab.models import policy,scaled,fit_temperature
from nlp_lab.review import collection,validate
from nlp_lab.run import summarize


def test_data_sources_never_include_holdout_private_exports_or_existing_test_rows():
    rows,audit=prepare()
    assert audit['original_training_n']==515
    assert audit['original_topics']['social']==315 and audit['original_topics']['definition']==8
    assert 'unsupported' not in audit['original_topics']
    assert all('/evaluation/' not in path and '/exports/' not in path for path in audit['sources'])
    assert all(row['split']=='train' for row in rows)
    assert len({r['key'] for r in rows})==len(rows)


def test_grouped_partitions_keep_exact_normalized_and_family_components_together():
    rows,_=prepare();split,metadata=partitions(rows)
    json.dumps({'split':split,'metadata':metadata})
    for name,indices in split.items():
        for other,other_indices in split.items():
            if name==other: continue
            assert not {rows[i]['group'] for i in indices}&{rows[i]['group'] for i in other_indices}
            assert not {rows[i]['normalized_key'] for i in indices}&{rows[i]['normalized_key'] for i in other_indices}


def test_guarded_input_can_never_reach_either_classifier_view():
    row={'blocked':'refused','question':'private placeholder'}
    for view in ('original','normalized'):
        with pytest.raises(ValueError): text(row,view)


def test_balanced_development_counts_are_not_independent_holdout_claims():
    rows=balanced_cases()
    assert len(rows)==130 and len({r['id'] for r in rows})==130
    assert all(sum(r['target']['topic']==t for r in rows)==10 for t in TOPICS)


def test_followup_merges_filters_while_new_subject_resets_old_state():
    previous=Context(tools=['get_player_scores'],source='simulator',period='today',score_page=2).model_dump()
    continued=frame('follow_up',normalize('What about yesterday?')[0],previous)
    assert continued.domain=='scores' and continued.period=='yesterday' and continued.source=='simulator'
    new=frame('queue',normalize('Show the queue.')[0],previous)
    assert new.domain=='queue' and new.period=='event_to_date' and new.source=='all'
    assert frame('follow_up',normalize('What about yesterday?')[0]).mode=='clarify'
    assert frame('follow_up',normalize('Next page.')[0],previous).score_page==3


def test_frame_has_no_raw_history_metrics_or_private_identifier_fields():
    with pytest.raises(ValidationError): Frame(mode='analytics',student_id='SYNTHETIC')
    assert not {'answer','history','score','student_id','nickname'}&Frame.model_fields.keys()


def test_thresholds_use_calibration_and_abstain_when_no_safe_point_exists():
    probabilities=np.array([[.9,.1],[.9,.1]])
    setting=policy(probabilities,['scores','unsupported'],['scores','unsupported'])
    assert setting['confidence']>1
    np.testing.assert_allclose(scaled(probabilities,1).sum(axis=1),1)
    fitted=fit_temperature(probabilities,['scores','unsupported'],['scores','unsupported'])
    assert .25<=fitted['temperature']<=5


def test_metrics_keep_refusals_errors_and_foreign_acceptances_in_denominator():
    rows=[{'expected':'scores','predicted':'unsupported'},
          {'expected':'queue','predicted':'error'},
          {'expected':'unsupported','predicted':'scores','decision':'clarify'}]
    result=summarize(rows)
    assert result['n']==3 and result['primary_correct']==0 and result['errors']==1
    assert result['oos_false_classifications']==1 and result['oos_false_answers']==0


def test_empty_collection_is_325_slots_and_zero_test_cases(tmp_path):
    path=tmp_path/'collection.json'
    assert collection(path)['filled']==0
    with pytest.raises(ValueError,match='filled'): validate(json.loads(path.read_text()))
    with pytest.raises(FileExistsError): collection(path)


def test_offline_ollama_adapter_can_route_explicit_question_without_model_or_database(monkeypatch):
    from nlp_lab.baseline import Observer,predict
    async def ready(*args,**kwargs): return {'available':True,'reason':None}
    async def forbidden(*args,**kwargs): pytest.fail('No inference for explicit scores')
    monkeypatch.setattr(Observer,'prepare',ready)
    monkeypatch.setattr('app.assistant.model_json',forbidden)
    row={'id':'probe','question':'Show scores.','label':'scores','previous':None}
    cases=asyncio.run(predict([row],[]))
    assert cases[0]['predicted']=='scores' and cases[0]['error'] is None
