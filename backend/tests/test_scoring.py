import json
from pathlib import Path
import pytest
from app.game import replay, simulated_result, RULES_HASH

@pytest.mark.parametrize('outcome,score,level',[('win',1500,12),('loss',375,3)])
def test_shared_scoring_vectors(outcome,score,level):
    vector=simulated_result(outcome)
    assert vector['rulesHash']==RULES_HASH.hex()
    result=replay(vector['placements'],vector['durationMs'],outcome)
    assert (result['score'],result['level'])==(score,level)

def test_timeout_and_tamper_rejection():
    assert replay([],60000,'loss')['score']==0
    vector=simulated_result('win')
    with pytest.raises(ValueError): replay(vector['placements'],vector['durationMs'],'loss')
    vector['placements'][0]['candidate_x']=3
    with pytest.raises(ValueError): replay(vector['placements'],vector['durationMs'],'win')
