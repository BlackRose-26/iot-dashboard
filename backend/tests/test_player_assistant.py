"""Stack Intelligence for players (24 Nov 2026): deterministic answers, privacy and limits."""
from fastapi.testclient import TestClient

from app.player_assistant import answer
from test_player_flow import environment, join, post  # noqa: F401

RULES = {'levels': 15, 'round_limit_ms': 60000}


def facts(**extra):
    base = {'rules': RULES, 'admissionsOpen': True, 'inLine': 4, 'cabinet': 'ready', 'roundSeconds': 90.0,
            'bestToday': 15, 'topCount': 3, 'ticket': None, 'round': None}
    return base | extra


def test_rules_line_and_scores_for_a_visitor():
    play = answer('How do I play?', facts())
    assert play['intent'] == 'how_to_play' and '15 levels within 60 seconds' in play['answer'] and play['source'] == 'Game rules'
    assert 'Is my student ID safe?' in play['suggestions']
    wait = answer('How long is the wait?', facts())
    assert '4 players in line' in wait['answer'] and 'about 6 minutes' in wait['answer']
    assert 'paused' in answer('how long is the line', facts(admissionsOpen=False))['answer']
    assert 'reconnecting' in answer('is the cabinet ready', facts(cabinet='offline'))['answer']
    top = answer('Top score today?', facts())
    assert top['answer'] == 'The best score today is 15 of 15. 3 players reached the top so far.'
    assert 'No rounds have finished today' in answer('best score?', facts(bestToday=None))['answer']
    assert 'not in line yet' in answer('When is my turn?', facts())['answer']


def test_taglish_and_unknown_questions():
    tl = answer('Paano maglaro?', facts())
    assert tl['intent'] == 'how_to_play' and 'Pindutin' in tl['answer']
    assert 'minuto' in answer('gaano katagal ang pila?', facts())['answer']
    unknown = answer('what is the capital of France', facts())
    assert unknown['intent'] == 'unknown' and unknown['source'] == '' and 'only help with the game' in unknown['answer']


def test_student_id_like_text_is_refused_and_never_repeated():
    for text in ('my id is 2021-12345', 'is 202112345 ok?', '21/0045 student'):
        reply = answer(text, facts())
        assert reply['intent'] == 'privacy' and 'don’t share your student ID' in reply['answer']
        assert not any(part in reply['answer'] for part in ('2021', '12345', '0045'))
    assert 'encrypted' in answer('Is my student ID safe?', facts())['answer']


def test_answers_follow_the_players_own_ticket():
    waiting = facts(ticket={'status': 'waiting', 'position': 3})
    turn = answer('When is my turn?', waiting)
    assert turn['answer'].startswith('You’re #3 with 2 players ahead') and turn['source'] == 'Your ticket · live'
    assert 'What if I miss my turn?' in turn['suggestions']
    assert answer('when is my turn', facts(ticket={'status': 'waiting', 'position': 1}))['answer'].startswith('You’re next')
    assert 'go to cabinet 01' in answer('What do I do now?', facts(ticket={'status': 'called'}))['answer'].lower()
    assert '3 minutes' in answer('What if I miss my turn?', waiting)['answer']

    done = facts(ticket={'status': 'completed'}, round={'won': False, 'score': 11, 'level': 12, 'reason': 'zero_overlap',
                                                        'higherToday': 5, 'roundsToday': 23,
                                                        'firstLoss': {'level': 4, 'kept': 5, 'width': 6}})
    result = answer('How did I do?', done)
    assert result['answer'] == 'You kept 11 of 15 rows. 5 of 23 rounds today scored higher.'
    assert result['suggestions'][0] == 'How did I do?'
    lost = answer('Where did I lose it?', done)
    assert 'first lost width at level 4, keeping 5 of 6' in lost['answer'] and 'missed the stack completely' in lost['answer']
    assert 'after your round' in answer('How did I do?', facts(ticket={'status': 'waiting', 'position': 2}))['answer']


def test_endpoints_use_live_data_and_are_limited(environment):
    app, admin, token, engine, settings = environment
    levels = TestClient(app).get('/api/player/context').json()['game']['levels']
    visitor = TestClient(app)
    play = visitor.post('/api/player/assistant', json={'question': 'How do I play?'})
    assert play.status_code == 200 and f'{levels} levels' in play.json()['answer']
    assert visitor.get('/api/player/lobby').json() == {'inLine': 0, 'cabinet': 'offline', 'admissionsOpen': True, 'waitMinutes': 0}

    first, second = join(app, token, 1), join(app, token, 2)
    lobby = visitor.get('/api/player/lobby').json()
    assert lobby['inLine'] == 2 and lobby['waitMinutes'] == 3
    assert second.post('/api/player/assistant', json={'question': 'When is my turn?'}).json()['answer'].startswith('You’re #2 with 1 player ahead')

    # First player plays a simulator round, then asks about it.
    assert admin.post('/api/admin/simulator/ready').status_code == 200
    assert post(admin, '/api/admin/queue/call-next').status_code == 200
    assert 'Go to Cabinet 01' in first.post('/api/player/assistant', json={'question': 'What do I do now?'}).json()['answer']
    assert admin.post('/api/admin/simulator/start').status_code == 200
    assert admin.post('/api/admin/simulator/loss').status_code == 200
    mine = first.post('/api/player/assistant', json={'question': 'How did I do?'}).json()
    assert mine['intent'] == 'my_result' and f'of {levels} rows' in mine['answer'] and 'best score of 1 rounds today' in mine['answer']
    assert 'The round ended at level' in first.post('/api/player/assistant', json={'question': 'Where did I lose it?'}).json()['answer']
    assert visitor.post('/api/player/assistant', json={'question': 'top score?'}).json()['source'] == 'Today’s scores'

    # Bad input, foreign sites and floods are refused.
    assert visitor.post('/api/player/assistant', json={'question': ''}).status_code == 422
    assert visitor.post('/api/player/assistant', json={'question': 'x' * 301}).status_code == 422
    assert visitor.post('/api/player/assistant', json={'question': 'hi', 'role': 'admin'}).status_code == 422
    assert visitor.post('/api/player/assistant', json={'question': 'hi'}, headers={'Origin': 'https://evil.example'}).status_code == 403
    flood = TestClient(app, client=('127.0.0.1', 50001))
    stranger = {'CF-Connecting-IP': '203.0.113.9'}
    codes = [flood.post('/api/player/assistant', json={'question': 'hi'}, headers=stranger).status_code for _ in range(21)]
    assert codes[:20] == [200] * 20 and codes[20] == 429
    other = {'CF-Connecting-IP': '198.51.100.30'}
    assert flood.post('/api/player/assistant', json={'question': 'hi'}, headers=other).status_code == 200, 'limit is per visitor'
