"""Disposable MariaDB checks for private structured memory and grounded conversation."""
import asyncio
import json
import os

os.environ['STACK_SKIP_DEFAULT_APP']='1'

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.assistant import Assistant, Context, SavedMemory, RoutingPlan, normalize, resolve_routing
from app.assistant_memory import MemoryStore
from app.database import execute, one
from app.main import create_app
from app.security import passwords
from test_player_flow import environment


@pytest.fixture
def routing(monkeypatch):
    calls = []
    async def ready(self):
        return {'enabled': True, 'available': True, 'installed': True, 'loaded': True, 'reason': 'ready'}
    async def classify(settings, payload, path='/api/chat', timeout=18):
        body = json.loads(payload['messages'][-1]['content'])
        calls.append(body)
        words = set(body['safe_tokens'])
        result = {'topic': 'follow_up'} if words & {'more', 'shorter', 'yesterday'} else {'topic':'knowledge','knowledge':'architecture'}
        return {'message': {'content': json.dumps(result)}}
    monkeypatch.setattr(Assistant, 'status', ready)
    monkeypatch.setattr('app.assistant.model_json', classify)
    return calls


def test_persistent_memory_restores_subject_without_storing_messages(environment, routing):
    app, admin, _, engine, settings = environment
    question = 'Could you describe which technologies this project uses?'
    response = admin.post('/api/admin/assistant/query', json={'question':question}).json()
    assert response['reason']=='system_context' and response['context']['knowledge']=='architecture'
    assert response['memory']['remembered']==1
    with engine.connect() as connection:
        saved = one(connection, 'SELECT state_json FROM ai_admin_memory WHERE staff_user_id=1')['state_json']
    assert question not in saved and 'React' not in saved and 'answer' not in json.loads(saved)
    # Fresh API instance and login session, same synthetic admin: memory survives restart.
    fresh_app = create_app(settings)
    with TestClient(fresh_app) as fresh:
        fresh.cookies.update(admin.cookies)
        fresh.headers['X-CSRF-Token'] = fresh.get('/api/admin/session').json()['csrf']
        assert fresh.get('/api/admin/assistant/memory').json()['context']['knowledge']=='architecture'
        followup = fresh.post('/api/admin/assistant/query', json={'question':'Could you explain more about that?'}).json()
        assert followup['context']['knowledge']=='architecture'
    fresh_app.state.engine.dispose()
    assert followup['context']['detailed'] and len(followup['knowledge_sources'])==2
    assert response['answer'] in followup['answer'] and len(followup['answer'])>len(response['answer'])
    assert not routing  # The restored typed subject resolves this edit without external inference.
    assert 'staff_user_id' not in str(routing) and question not in str(routing)


def test_preferences_are_private_and_memory_can_be_disabled(environment, routing):
    app, admin, _, engine, settings = environment
    response = admin.post('/api/admin/assistant/query', json={'question':'Please reply in Taglish from now on.'}).json()
    assert response['memory']['preferences']['language']=='taglish'
    hello = admin.post('/api/admin/assistant/query', json={'question':'hello'}).json()
    assert 'Hello po!' in hello['answer']
    offline_memory = admin.post('/api/admin/assistant/query', json={'question':'hello','use_memory':False}).json()
    assert "Hi! I'm" in offline_memory['answer']
    assert not offline_memory['memory']['enabled']
    with engine.begin() as connection:
        execute(connection, "INSERT INTO staff_users(username,password_hash,role) VALUES('memory-other',:password,'admin')", password=passwords.hash('Synthetic-memory-only'))
    with TestClient(app) as other:
        assert other.post('/api/admin/login',json={'username':'memory-other','password':'Synthetic-memory-only'}).status_code==200
        state=other.get('/api/admin/assistant/memory').json()
        assert state['context'] is None and state['remembered']==0
        assert state['preferences']['language'] is None
    assert not routing  # preferences and exact greetings need no inference


def test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning(environment):
    app, admin, _, engine, settings = environment
    store=MemoryStore(engine,SavedMemory)
    state, revision, available=store.load(1)
    assert available
    state.context=Context(knowledge='registration')
    state.remembered=1
    assert store.save(1,state,revision)
    old_state, old_revision, _=store.load(1)
    assert admin.delete('/api/admin/assistant/memory',headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert admin.delete('/api/admin/assistant/memory').json()['remembered']==0
    assert not store.save(1,old_state,old_revision)
    assert admin.get('/api/admin/assistant/memory').json()['context'] is None
    guest=TestClient(app)
    assert guest.get('/api/admin/assistant/memory').status_code==401
    assert guest.delete('/api/admin/assistant/memory').status_code==401
    guest.close()


def test_memory_schema_has_no_place_for_raw_text_or_invented_metrics():
    with pytest.raises(ValidationError): SavedMemory(messages=[{'role':'user','content':'private'}])
    with pytest.raises(ValidationError): SavedMemory(context={'student_id':'SYNTHETIC-NOT-REAL'})
    with pytest.raises(ValidationError): SavedMemory(context={'completed_games':123})
    with pytest.raises(ValidationError): SavedMemory(context={'knowledge':'private-files'})
    with pytest.raises(ValidationError): SavedMemory(recent=[Context()]*7)


@pytest.mark.parametrize('question,topic', [
    ('Could you walk me through how visitors get into the game?', 'registration'),
    ('Can we talk about why the project uses XAMPP?', 'architecture'),
    ('I want to understand what the dashboard charts mean.', 'dashboard'),
    ('How is my student ID encrypted?', 'privacy'),
    ('What does conversation memory mean?', 'memory'),
])
def test_explicit_system_subject_beats_an_older_conversation(question,topic):
    normalized,reason=normalize(question)
    assert reason is None and normalized['system_topic_hint']==topic
    previous=Context(knowledge='results')
    assert resolve_routing(RoutingPlan(topic='knowledge',knowledge='results'),normalized,previous).knowledge==topic
    assert resolve_routing(RoutingPlan(topic='follow_up'),normalized,previous).knowledge==topic


@pytest.mark.parametrize('question', ['Who won the world cup?', 'Tell me a joke about politics.'])
def test_missing_unrelated_subject_is_not_silently_replaced_with_event_facts(question):
    safe,blocked=normalize(question)
    assert blocked=='system_scope' or safe['has_unrecognized_words'] or safe['requires_scope_check']
    assert resolve_routing(RoutingPlan(topic='unsupported'),safe).clarify if safe else blocked


def test_explaining_privacy_does_not_allow_identity_retrieval():
    assert normalize('How can I get private student IDs?')[1]=='refused'
    assert normalize('My ID is GAME.')[1]=='refused'
