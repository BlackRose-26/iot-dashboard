"""Admission repair (24 Nov 2026): lexicon v2, shorthand, follow-ups and one-tap choices.

Development checks only. They never read holdout or evaluation cases.
"""
import json

import pytest

from app.assistant import Assistant, Context, contextual_follow_up, constraints, normalize
from app.assistant_language import LEXICON, lexical_resource
from app.assistant_learning import TOPIC_CHOICES, topic_choices
from test_player_flow import environment  # noqa: F401  (disposable XAMPP fixture)


def test_lexicon_v2_keeps_everyday_words_and_still_excludes_names():
    words,digest=lexical_resource()
    assert LEXICON.name=='assistant-language-lexicon-v2.json' and len(digest)==64
    assert {'far','add','down','head','power','sort','better','contact','ran','meant','goes','iyo'} <= words
    assert not {'maria','joseph','exampleperson','exampletown','76543'} & words
    v1=json.loads((LEXICON.parent/'assistant-language-lexicon.json').read_text(encoding='utf-8'))
    assert set(v1['english'])|set(v1['tagalog']) <= words, 'v2 must never drop a word v1 accepted'
    data=json.loads(LEXICON.read_text(encoding='utf-8'))
    assert data['version']==2 and not {'examples','questions','targets','glosses','definitions'} & data.keys()


@pytest.mark.parametrize('question',[
    'Who has the oldest score pls',             # superlative + shorthand
    'pleaseee show the queue rn',               # stretched spelling + shorthand
    'Ano ang huling score?',                    # Tagalog linker: huli + ng
    'Pakita ang aking pila',                    # Tagalog linker: akin + g
    'How far did players get in the stack?',    # previously missing everyday word
])
def test_everyday_wording_is_no_longer_unknown(question):
    safe,blocked=normalize(question)
    assert blocked is None and not safe['has_unrecognized_words'],question


@pytest.mark.parametrize('question',[
    "Show ExamplePerson's points.",
    'What is the score of maria?',
    'Ano ang score ni Juan?',
    'How many players in ExampleTown?',
])
def test_possible_names_stay_unknown(question):
    safe,blocked=normalize(question)
    assert blocked or safe['has_unrecognized_words'],question


def test_contextual_follow_up_needs_previous_context_and_no_new_subject():
    previous=Context(tools=['get_queue_summary'],language='en')
    safe,_=normalize('What about that one instead?')
    assert contextual_follow_up(safe,previous)
    assert not contextual_follow_up(safe,None)
    new_subject,_=normalize('What about that banana one?')
    assert not contextual_follow_up(new_subject,previous), 'a dictionary-only new subject is not a follow-up'
    foreign,_=normalize('What about that basketball one?')
    assert not foreign or not contextual_follow_up(foreign,previous)


def test_every_topic_choice_routes_to_read_only_analytics_without_the_model():
    for _,label,question in TOPIC_CHOICES:
        safe,blocked=normalize(question)
        assert blocked is None and not safe['has_unrecognized_words'] and not safe['requires_scope_check'],label
        assert constraints(safe) is not None,label


def test_choices_only_name_topics_that_the_question_mentions():
    safe,_=normalize("Show ExamplePerson's points.")
    assert [c['label'] for c in topic_choices(safe)]==['Scores']
    safe,_=normalize('Tell me about the quux queue and cabinet')
    assert {c['label'] for c in topic_choices(safe)}=={'Queue','Cabinet status'}
    assert topic_choices(None)==[]


def test_unknown_name_gets_one_tap_choices_but_no_answer(environment,monkeypatch):
    app,admin,_,engine,settings=environment
    async def ready(*args,**kwargs): return {'available':True}
    monkeypatch.setattr(Assistant,'status',ready)
    monkeypatch.setattr('app.assistant.model_json',lambda *a,**k:pytest.fail('An unknown name never reaches the model'))
    monkeypatch.setattr('app.assistant.collect_all',lambda *a,**k:pytest.fail('No analytics before the person chooses'))
    reply=admin.post('/api/admin/assistant/query',json={'question':"Show ExamplePerson's points.",'use_memory':False}).json()
    assert reply['status']=='needs_clarification' and reply['reason']=='unrecognized_context'
    assert reply['interpretations']==[{'label':'Scores','question':'Show the score summary.'}]
    assert not reply['claims'] and reply['context']['tools']==[]
