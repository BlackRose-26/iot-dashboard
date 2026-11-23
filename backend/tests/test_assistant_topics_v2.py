"""Wrong-topic and generic-reply repair (24 Nov 2026). Development checks only; no holdout text."""
import json

import pytest

from app.assistant import Assistant, asks_live_state, constraints, normalize, reviewed_explanation
from app.assistant_interactions import composed_social
from app.assistant_language import linguistic_text
from app.assistant_semantics import explanation_declined, semantic_words
from test_player_flow import environment  # noqa: F401  (disposable XAMPP fixture)


@pytest.mark.parametrize('question,live', [
    ('How is the event doing right now?', True),
    ('When did the cabinet last report in?', True),
    ('Which stack row do players miss most often?', True),
    ('How does the queue work?', False),
    ('Why are student identifiers encrypted?', False),
    ('Explain the rules of the game.', False),
])
def test_live_state_wording_is_told_apart_from_design_questions(question, live):
    safe, blocked = normalize(question)
    assert blocked is None and asks_live_state(safe) is live, question


def test_a_declined_explanation_does_not_become_a_definition():
    safe, _ = normalize('Show the average score without any explanation of the formula.')
    assert explanation_declined(safe['safe_tokens']) and not {'formula', 'explanation'} & semantic_words(safe)
    assert constraints(safe)['definition'] is None and constraints(safe)['tools']
    asked, _ = normalize('Explain the average score formula.')
    assert constraints(asked)['definition'] == 'average_score'


def test_how_results_qualify_is_explained_but_a_count_is_measured():
    safe, _ = normalize('How are valid results chosen for the leaderboard?')
    assert reviewed_explanation(safe) == 'results'
    count, _ = normalize('How many results are on the leaderboard?')
    assert reviewed_explanation(count) is None and constraints(count)['tools'] == ['get_top_scores']


@pytest.mark.parametrize('question', ['Whose round has the highest score?', 'Kanino ang pinakamataas na resulta ng laro?'])
def test_whose_highest_asks_for_the_leader(question):
    safe, _ = normalize(question)
    assert constraints(safe)['tools'] == ['get_top_scores']


@pytest.mark.parametrize('text,act', [
    ('good evening to you', 'greeting'),
    ('thank you for your help', 'thanks'),
    ('salamat po sa inyong pagtulong sa akin', 'thanks'),
    ('can you help me', 'help'),
])
def test_courtesy_endings_keep_the_social_act(text, act):
    assert composed_social(linguistic_text(text))[0] == act


def test_hyphenated_compounds_of_known_words_are_understood_but_names_stay_unknown():
    safe, _ = normalize('Show an hour-by-hour view of game activity.')
    assert not safe['has_unrecognized_words']
    name, _ = normalize("Show Jean-ExamplePerson's points.")
    assert name['has_unrecognized_words']


def test_explanation_card_for_a_live_request_is_rerouted_to_live_topics(environment, monkeypatch):
    app, admin, _, engine, settings = environment
    calls = []
    async def ready(*args, **kwargs): return {'available': True}
    async def model(settings, payload, *args, **kwargs):
        calls.append(payload)
        enum = payload['format']['properties']
        if set(enum) == {'scope'}: return {'message': {'content': '{"scope":"system"}'}}
        topics = enum['topic']['enum']
        if 'knowledge' in topics: return {'message': {'content': json.dumps({'topic': 'knowledge', 'knowledge': 'offline'})}}
        assert 'knowledge' not in topics and 'definition' not in topics, 'the retry offers live-data topics only'
        return {'message': {'content': json.dumps({'topic': 'machine'})}}
    monkeypatch.setattr(Assistant, 'status', ready)
    monkeypatch.setattr('app.assistant.model_json', model)
    reply = admin.post('/api/admin/assistant/query', json={'question': 'How recent is the newest signal from the physical controller?',
                                                           'use_memory': False}).json()
    assert reply['context']['tools'] == ['get_machine_summary'], reply
    assert any('knowledge' not in c['format']['properties'].get('topic', {}).get('enum', ['knowledge']) for c in calls)
