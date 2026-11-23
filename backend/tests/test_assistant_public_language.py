"""Published-word vocabulary and development probes; not an unseen benchmark."""
import json
from types import SimpleNamespace

import pytest

from app.assistant import RoutingPlan, intent_payload, normalize, resolve_routing
from app.assistant_language import LEXICON, lexical_resource
from app.assistant import Assistant
from test_player_flow import environment


# Authored for this repair, not copied from the consumed holdout. They are visible
# development material and must be included in future benchmark overlap audits.
DEVELOPMENT = [
    ('overview','Please recount how the carnival is progressing as a whole.','en'),
    ('overview','How is the event unfolding overall?','en'),
    ('players','Could you enumerate how many competitors have enrolled?','en'),
    ('players','What proportion of completed rounds were victories?','en'),
    ('queue','What is the present state of admissions and the waiting list?','en'),
    ('queue','Can you inspect whether anybody is awaiting their turn?','en'),
    ('machine','Is our cabinet responsive at present?','en'),
    ('machine','How recently did the ESP32 communicate with the server?','en'),
    ('scores','Could you enumerate individual scores for the competitors?','en'),
    ('scores','What is the arithmetic mean of the recorded points?','en'),
    ('levels','At which stage do attempts most frequently fail?','en'),
    ('levels','Compare the recorded difficulty across the stages.','en'),
    ('trend','How does participation fluctuate over time?','en'),
    ('trend','At what hour does game activity culminate?','en'),
    ('top','Which entrant has accumulated the most points?','en'),
    ('top','Who occupies first place in the standings?','en'),
    ('definition:accuracy','Please explain the significance of overlap accuracy.','en'),
    ('definition:total_score','How is the cumulative score computed?','en'),
    ('knowledge:registration','Could you recount the registration procedure?','en'),
    ('knowledge:architecture','How do the server components cooperate?','en'),
    ('social:greeting','Greetings and good afternoon, assistant.','en'),
    ('social:thanks','I appreciate your assistance; thank you.','en'),
    ('social:greeting','Magandang hapon po, hello!','taglish'),
    ('scores','Pakilista ang puntos ng bawat kalahok.','taglish'),
    ('queue','Mayroon bang naghihintay sa pila natin?','taglish'),
    ('knowledge:registration','Maaari mo bang ilahad ang daloy ng pagpaparehistro?','taglish'),
    ('definition:scoring','Paano kinakalkula ang puntos sa laro?','taglish'),
    ('unsupported','What is the score in professional basketball?','en'),
    ('unsupported','How many passengers are in the airport queue?','en'),
    ('unsupported','Which cuisine should I cook for dinner?','en'),
    ('unsupported','How much electricity does the building consume?','en'),
    ('unsupported','Show the player named Example points.','en'),
    ('unsupported','What is the score in basketball?','en'),
    ('unsupported','Ano ang score sa basketball?','taglish'),
]


@pytest.mark.parametrize('target,question,language',DEVELOPMENT)
def test_development_wording_preserves_public_content_or_rejects_locally(target,question,language):
    safe,blocked=normalize(question)
    if target=='unsupported':
        assert blocked or safe['has_unrecognized_words'] or safe['requires_scope_check']
    else:
        assert not blocked and not safe['has_unrecognized_words'],question
        assert safe['language_hint']==language


def test_public_dictionary_is_word_only_filtered_and_content_addressed():
    words,digest=lexical_resource()
    assert len(words)>100000 and len(digest)==64
    assert {'enumerate','significance','basketball'} <= words
    assert not {'exampleperson','exampletown','maria','joseph','76543'} & words
    data=json.loads(LEXICON.read_text(encoding='utf-8'))
    assert not {'examples','questions','targets','glosses','definitions'} & data.keys()


def test_dictionary_membership_cannot_override_an_unsupported_subject():
    safe,blocked=normalize('What is the score in badminton?')
    assert not blocked and not safe['has_unrecognized_words'] and safe['requires_scope_check']
    assert 'badminton' in safe['safe_tokens']
    assert resolve_routing(RoutingPlan(topic='unsupported'),safe).clarify
    payload=intent_payload(SimpleNamespace(ollama_model='synthetic'),safe)
    assert json.loads(payload['messages'][-1]['content'])['request_kind']=='analytics'
    assert 'unsupported' in payload['format']['properties']['topic']['enum']


def test_polysemous_word_does_not_silently_change_a_measure():
    safe,blocked=normalize('What is the peak score?')
    assert not blocked and safe['requires_scope_check']
    assert 'peak' in safe['safe_tokens'] and 'busiest' not in safe['safe_tokens']


def test_scope_rejection_stops_before_router_and_analytics(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    calls=[]
    async def ready(*args,**kwargs): return {'available':True}
    async def scope_only(settings,payload,*args,**kwargs):
        calls.append(payload)
        assert set(payload['format']['properties'])=={'scope'}
        assert len(payload['messages'])==2
        return {'message':{'content':'{"scope":"unsupported"}'}}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',scope_only)
    for question in ('What is the score in badminton?','Ano ang score sa badminton?'):
        reply=admin.post('/api/admin/assistant/query',json={'question':question,'use_memory':False}).json()
        assert reply['reason']=='system_scope' and reply['status']=='needs_clarification'
        assert not reply['claims'] and not reply.get('evidence')
    assert len(calls)==2
