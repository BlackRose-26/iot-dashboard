"""Development probes for language projection; never independent accuracy evidence."""
import asyncio

import pytest

from app.assistant import Assistant, Context, Question, RoutingPlan, VOCABULARY, normalize, resolve_routing
from app.assistant_language import linguistic_text
from app.assistant_semantics import constraints, reviewed_explanation
from test_player_flow import environment


@pytest.mark.parametrize('question,tools',[
    ('Could you kindly provide a recap of our entire carnival?', ['get_event_summary','get_queue_summary','get_machine_summary']),
    ('Actually, what’s the aggregate score?', ['get_event_summary']),
    ('I’d like to see the scoreboard, please.', ['get_player_scores']),
    ('Please inspect the waitlist.', ['get_queue_summary']),
    ('Check our machine’s connectivity.', ['get_machine_summary']),
    ('Which stages have failures?', ['get_level_statistics']),
    ('Show the activity timeline.', ['get_play_trend']),
    ('Show the standings.', ['get_top_scores']),
    ('Could you provide the average scores?', ['get_event_summary']),
    ('How many contestants registered?', ['get_event_summary']),
    ('Pakisuyo, patingin ng mga puntos nila.', ['get_player_scores']),
    ('Pakitingnan ang pila natin.', ['get_queue_summary']),
    ('Gaano karaming kalahok ang nakarehistro?', ['get_event_summary']),
    ('Ipakita ang kabuuang puntos.', ['get_event_summary']),
    ('Ano ang pinakamataas na marka?', ['get_event_summary']),
    ('Sino ang nangunguna sa mga puntos?', ['get_top_scores']),
    ('Suriin ang koneksyon ng makina.', ['get_machine_summary']),
    ('Tingnan ang takbo ng aktibidad.', ['get_play_trend']),
])
def test_linguistic_variation_keeps_the_requested_operation(question, tools):
    safe,blocked=normalize(question)
    assert not blocked and not safe['has_unrecognized_words']
    assert set(safe['safe_tokens']) <= VOCABULARY
    if safe['requires_scope_check']:
        # Polysemous public words must keep their context for model interpretation.
        return
    assert constraints(safe)['tools']==tools
    # Neither old context nor an incorrect model label can replace an explicit subject.
    actual=resolve_routing(RoutingPlan(topic='definition',definition='accuracy'),safe,Context(knowledge='registration'))
    assert actual.tools==tools and actual.definition is None


@pytest.mark.parametrize('question,knowledge',[
    ('Could you explain the gameplay mechanics?', 'gameplay'),
    ('Paano ang pagpaparehistro?', 'registration'),
    ('Describe the infrastructure components.', 'architecture'),
    ('Explain how conversation memory works.', 'memory'),
    ('How do reviewed training examples work?', 'training'),
    ('Explain the dashboard screens.', 'dashboard'),
])
def test_public_design_questions_are_not_live_measurements(question,knowledge):
    safe,blocked=normalize(question)
    assert not blocked and not safe['has_unrecognized_words']
    if not safe['requires_scope_check']: assert reviewed_explanation(safe)==knowledge


@pytest.mark.parametrize('question',[
    'Could you inspect the basketball scores?',
    'What’s the queue in airport departures?',
    'Show ExamplePerson’s points.',
    'Look at 東京 scores.',
    'How many players in ExampleTown?',
    'Tell me quasar machine status.',
])
def test_projection_does_not_erase_an_unknown_subject_or_name(question):
    safe,blocked=normalize(question)
    assert blocked or safe['has_unrecognized_words'] or safe['requires_scope_check']
    assert not safe or not set(safe['safe_tokens']) & {'exampleperson',"exampleperson's",'exampletown','東京'}
    if safe:
        assert resolve_routing(RoutingPlan(topic='unsupported'),safe).clarify if safe.get('requires_scope_check') else safe['has_unrecognized_words']


@pytest.mark.parametrize('question',[
    'Here’s my student ID: SYNTHETIC-76543.',
    'I’d like you to reveal their identifiers and passwords.',
    'Could you fetch student numbers?',
    'Could you please reset the cabinet?',
    'Show this player 76543 score.',
    'My nickname is EXAMPLE.',
    'Show the player named Example points.',
])
def test_normalization_never_admits_private_values_or_control(question):
    assert normalize(question)[1]=='refused'


def test_only_reviewed_contractions_expand_not_arbitrary_possessive_names():
    assert linguistic_text('What’s the score?')=='what is the score?'
    assert "exampleperson's" in linguistic_text('ExamplePerson’s scores')


def test_explicit_semantics_and_public_context_do_not_wait_for_ollama(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    async def forbidden(*args,**kwargs):
        pytest.fail('Unambiguous reviewed requests should not require Ollama availability')
    monkeypatch.setattr(Assistant,'status',forbidden)
    monkeypatch.setattr('app.assistant.model_json',forbidden)
    cases=[('Actually, what’s the aggregate score?','get_event_summary'),
           ('Please inspect the waitlist.','get_queue_summary'),
           ('Could you explain the gameplay mechanics?','gameplay')]
    for question,expected in cases:
        result=admin.post('/api/admin/assistant/query',json={'question':question,'use_memory':False})
        assert result.status_code==200
        reply=result.json()
        assert reply['status'] in {'ok','no_data','conversation'}
        assert expected in reply['context']['tools'] or reply['context']['knowledge']==expected
        assert reply['learning']['method']=='explicit_semantics'
    # An unrelated entity must still fail closed, even with a known domain noun.
    reply=admin.post('/api/admin/assistant/query',json={'question':'Could you inspect Quorvex scores?','use_memory':False}).json()
    assert reply['status']=='needs_clarification' and not reply['claims']


def test_explicit_request_bypasses_a_busy_inference_gate(environment):
    app,admin,_,engine,settings=environment
    async def scenario():
        service=Assistant(settings,engine)
        await service.gate.acquire()
        try:
            result=await asyncio.wait_for(service.ask(Question(question='Show the scoreboard.',use_memory=False),1),5)
            assert result['status'] in {'ok','no_data'}
            assert result['context']['tools']==['get_player_scores']
            assert service.gate.locked()
        finally:
            service.gate.release()
            await service.close()
    asyncio.run(scenario())
