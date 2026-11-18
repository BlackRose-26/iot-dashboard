"""Reviewed routing dataset checks using only disposable MariaDB and synthetic inputs."""
import json
import hashlib
import uuid

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import text

from app.assistant import Context, normalize
from app.assistant_training import Proposal, TrainingInput, TrainingTarget
from app.database import execute, one
from app.security import passwords
from test_player_flow import environment

BASE='/api/admin/assistant/training'


def candidate(question='hello',topic='social',**labels):
    safe,blocked=normalize(question)
    assert not blocked
    return {'input':dict(safe,previous=None,prior_contexts=[]),
            'target':dict(topic=topic,definition=None,knowledge=None,social='greeting' if topic=='social' else None,**labels)}


def approve(admin,row,target=None,reviewed=True):
    return admin.patch(f"{BASE}/{row['id']}",json={'revision':row['revision'],'decision':'approve',
        'target':target or row['target'],'reviewed':reviewed,'context_version':admin.get(f'{BASE}/options').json()['context_version']})


def test_selection_review_export_and_rejection(environment):
    app,admin,_,engine,settings=environment
    reply=admin.post('/api/admin/assistant/query',json={'question':'hello'}).json()
    assert '_training_target' not in reply and reply['review_candidate']['target']['social']=='greeting'
    assert admin.get(BASE).json()['items']==[]  # no automatic collection
    row=admin.post(BASE,json=reply['review_candidate']).json()
    assert row['status']=='pending'
    assert admin.post(f'{BASE}/export').status_code==409
    assert approve(admin,row,reviewed=False).status_code==422
    approved=approve(admin,row).json()
    assert approved['status']=='approved'
    exported=admin.post(f'{BASE}/export').json()
    assert exported['count']==1 and exported['automatic_training'] is False
    sample=json.loads(exported['jsonl'].strip())
    assert [message['role'] for message in sample['messages']]==['system','user','assistant']
    assert json.loads(sample['messages'][2]['content'])['social']=='greeting'
    model_input=json.loads(sample['messages'][1]['content'])
    assert model_input['safe_tokens']==['hello'] and not {'question','answer','claims','snapshot_id'} & model_input.keys()
    assert reply['answer'] not in exported['jsonl']
    assert 'staff_user_id' not in exported['jsonl'] and 'input_hash' not in exported['jsonl']
    assert approve(admin,row).status_code==409  # stale revision
    rejected=admin.patch(f"{BASE}/{row['id']}",json={'revision':approved['revision'],'decision':'reject','target':row['target']}).json()
    assert rejected['status']=='rejected'
    assert admin.post(f'{BASE}/export').status_code==409


def test_duplicate_does_not_overwrite_reviewed_label_and_context_change_needs_review(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    body=candidate()
    row=admin.post(BASE,json=body).json()
    approved=approve(admin,row).json()
    other=dict(body,target={'topic':'unsupported','definition':None,'knowledge':None,'social':None})
    duplicate=admin.post(BASE,json=other).json()
    assert duplicate['duplicate'] and duplicate['target']==approved['target']
    assert duplicate['revision']==approved['revision']
    prior_version=admin.get(f'{BASE}/options').json()['context_version']
    monkeypatch.setattr('app.assistant_training.context_version',lambda:'f'*64)
    assert not admin.get(BASE).json()['items'][0]['current']
    assert admin.post(f'{BASE}/export').status_code==409
    assert admin.patch(f"{BASE}/{row['id']}",json={'revision':approved['revision'],'decision':'approve',
        'target':approved['target'],'reviewed':True,'context_version':prior_version}).status_code==409
    renewed=approve(admin,approved).json()
    assert renewed['current']
    assert admin.post(f'{BASE}/export').json()['count']==1
    revised=admin.patch(f"{BASE}/{row['id']}",json={'revision':renewed['revision'],'decision':'revise','target':renewed['target']}).json()
    assert revised['status']=='pending' and admin.post(f'{BASE}/export').status_code==409


def test_ownership_csrf_and_removal(environment):
    app,admin,_,engine,settings=environment
    body=candidate()
    guest=TestClient(app)
    assert guest.get(BASE).status_code==401
    assert guest.get(f'{BASE}/options').status_code==401
    assert guest.post(BASE,json=body).status_code==401
    assert admin.post(BASE,json=body,headers={'X-CSRF-Token':'wrong'}).status_code==403
    row=admin.post(BASE,json=body).json()
    with engine.begin() as connection:
        execute(connection,"INSERT INTO staff_users(username,password_hash,role) VALUES('training-other',:password,'admin')",password=passwords.hash('Synthetic-training-only'))
    with TestClient(app) as other:
        assert other.post('/api/admin/login',json={'username':'training-other','password':'Synthetic-training-only'}).status_code==200
        other.headers['X-CSRF-Token']=other.get('/api/admin/session').json()['csrf']
        assert other.get(BASE).json()['items']==[]
        assert approve(other,row).status_code==404
        assert other.delete(f"{BASE}/{row['id']}").status_code==404
        assert other.post(f'{BASE}/export').status_code==409
    assert admin.post(f'{BASE}/export',headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert admin.delete(f"{BASE}/{row['id']}",headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert admin.delete(f"{BASE}/{row['id']}").json()['removed']
    assert admin.get(BASE).json()['items']==[]
    guest.close()


@pytest.mark.parametrize('mutation', [
    {'question':'SYNTHETIC-PRIVATE-123456'}, {'answer':'Synthetic real-score prose must not be stored'},
    {'status':'approved'}, {'messages':[{'role':'system','content':'arbitrary'}]},
])
def test_raw_messages_answers_and_self_approval_are_rejected(environment,mutation):
    app,admin,_,engine,settings=environment
    body=dict(candidate(),**mutation)
    response=admin.post(BASE,json=body)
    assert response.status_code==422 and 'SYNTHETIC-PRIVATE' not in response.text
    assert admin.get(BASE).json()['items']==[]


@pytest.mark.parametrize('tokens', [['private-name-value'],['my','id','is','game'],['ignore','system','prompt'],['123456']])
def test_unsafe_normalized_inputs_are_rejected(tokens):
    with pytest.raises(ValidationError): TrainingInput(safe_tokens=tokens)


def test_labels_and_context_are_strict(monkeypatch):
    with pytest.raises(ValidationError): TrainingTarget(topic='knowledge')
    with pytest.raises(ValidationError): TrainingTarget(topic='players',knowledge='privacy')
    with pytest.raises(ValidationError): TrainingTarget(topic='social',social='execute_sql')
    with pytest.raises(ValidationError): TrainingInput(safe_tokens=['hello'],previous={'completed_games':123})
    body=candidate()
    body['target']={'topic':'follow_up','definition':None,'knowledge':None,'social':None}
    with pytest.raises(ValidationError): Proposal.model_validate(body)
    normalized,_=normalize('Why does this project use XAMPP?')
    with pytest.raises(ValidationError): Proposal(input=TrainingInput(**normalized),target=TrainingTarget(topic='knowledge',knowledge='registration'))
    from app.assistant_training import context_version
    original=context_version()
    monkeypatch.setattr('app.assistant_training.NORMALIZATION_VERSION','synthetic-next-version')
    assert context_version()!=original
    assert normalize('How does training work?')[0]['system_topic_hint']=='training'


def test_blocked_chat_is_never_a_training_candidate(environment):
    app,admin,_,engine,settings=environment
    response=admin.post('/api/admin/assistant/query',json={'question':'Show student IDs.'}).json()
    assert response['status']=='refused' and 'review_candidate' not in response
    assert admin.get(BASE).json()['items']==[]


def test_owner_queue_has_a_bounded_capacity(environment):
    app,admin,_,engine,settings=environment
    example=candidate()
    rows=[{'id':str(uuid.uuid4()),'hash':hashlib.sha256(str(index).encode()).hexdigest(),
           'input':json.dumps(example['input']),'target':json.dumps(example['target'])} for index in range(1000)]
    with engine.begin() as connection:
        connection.execute(text('''INSERT INTO ai_training_examples
            (public_id,staff_user_id,input_hash,input_json,target_json,context_version,policy_version)
            VALUES(:id,1,:hash,:input,:target,'synthetic-version','synthetic-policy')'''),rows)
    assert admin.post(BASE,json=candidate('thanks')).status_code==409
    page=admin.get(BASE).json()
    assert len(page['items'])==25 and page['next_cursor'] is not None
