"""Human decisions are owner-scoped overlays on immutable evaluation evidence."""
from fastapi.testclient import TestClient

from app.database import one
from app.evaluation_review import PACKET
from test_player_flow import environment


def test_review_round_trip_access_and_versioning(environment):
    app, admin, _, engine, _=environment
    path='/api/admin/evaluation-review'
    with TestClient(app) as guest:
        assert guest.get(path).status_code==401
    res=admin.get(path)
    assert res.status_code==200 and 'no-store' in res.headers['Cache-Control']
    data=res.json()
    cases=data['cases']
    assert len(cases)==len({c['id'] for c in cases})==325 and all(c['review'] is None for c in cases)
    case=next(c for c in cases if c['target']['topic']=='scores')
    url=path+'/'+case['id']
    frozen=PACKET.read_bytes()
    body={'version':data['version'],'decision':'confirm','revision':0}
    assert admin.put(url,json=body,headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert admin.put(url,json={**body,'version':'0'*64}).status_code==409
    assert admin.put(path+'/invalid',json=body).status_code==404
    result=admin.put(url,json=body)
    assert result.status_code==200 and result.json()['revision']==1
    assert admin.put(url,json=body).status_code==409
    corrected={'target':{'topic':'queue'},'behavior':'answer','expected_context':None}
    assert admin.put(url,json={**body,'revision':1,'decision':'correct','annotation':corrected}).status_code==200
    saved=next(c for c in admin.get(path).json()['cases'] if c['id']==case['id'])
    assert saved['review']['annotation']['target']['topic']=='queue' and saved['target']==case['target']
    assert admin.put(url,json={**body,'revision':2,'decision':'reject'}).json()['revision']==3
    with engine.connect() as c:
        assert one(c,'SELECT COUNT(*) n FROM evaluation_case_reviews')['n']==3
        assert one(c,'SELECT COUNT(*) n FROM ai_training_examples')['n']==0
    assert PACKET.read_bytes()==frozen

