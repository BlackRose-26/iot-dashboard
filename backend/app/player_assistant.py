"""Stack Intelligence for players: a small, deterministic helper on the scan and ticket pages.

It answers from checked templates filled with live facts (the active rules, the line, today's
aggregate scores and, for a signed-in player, their own ticket and round). No language model,
nothing stored, no other player's data, and it can never change the queue. Questions are not
logged; a question that looks like a student ID is refused without being repeated.
"""
import re
import unicodedata

TAGALOG = {'paano', 'pano', 'ako', 'ba', 'ilan', 'kailan', 'pila', 'laro', 'maglaro', 'salamat', 'ano', 'gaano',
           'katagal', 'mga', 'po', 'ko', 'ang', 'nang', 'naman', 'sumali', 'manalo', 'natalo', 'bakit', 'ulit',
           'kumusta', 'musta', 'tayo', 'dito', 'pwede', 'puwede', 'sino', 'saan', 'yung', 'lang'}
ID_LIKE = re.compile(r'\d{5,}|\d{2,4}\s*[-/]\s*\d{3,}')

# Order matters: personal and specific intents come before general ones.
INTENTS = [
    ('privacy', r'student ?id|id number|\bprivacy\b|\bsafe\b|personal (data|info)|\bdata\b'),
    ('lost', r'where did i (lose|miss)|what happened|why did i (lose|fail)|bakit (ako )?natalo|\bmistake'),
    ('my_result', r'how did i do|my (score|result|round)|ilan (ang )?score ko|kumusta (ang )?laro ko|did i win'),
    ('tips', r'\btips?\b|advice|strategy|\btricks?\b|paano manalo|how (do i|to|can i) win|diskarte|get better|climb higher'),
    ('miss_turn', r'\bmiss\b|\blate\b|not there|wala ako|absent|no.?show|can.?t make it'),
    ('play_again', r'\bagain\b|another (turn|round|game)|\bulit\b|replay|one more|rejoin'),
    ('my_turn', r'my turn|kailan ako|when (am i|is my|do i)|my (place|position|spot)|\bpwesto\b|what do i do now|where do i go'),
    ('top_score', r'\btop\b|\bbest\b|highest|record|leaderboard|pinakamataas|high ?score'),
    ('wait', r'\bwait|how long|\bline\b|queue|\bpila\b|ilang tao|how many (people|players)|gaano katagal|matagal|estimate|busy|is the cabinet|cabinet (ready|working|offline)|\bready\b'),
    ('join', r'how (do i|to|can i) (join|register|sign up|enter)|\bjoin\b|register|sign ?up|\bscan\b|sumali|pano sumali'),
    ('how_to_play', r'\bplay\b|how does (it|this|the game) work|\brules?\b|paano|maglaro|\blaro\b|how to|\bbutton\b|controls|mechanics|\bpoints?\b|levels?|scoring'),
    ('thanks', r'thank|salamat|\bty\b|\btnx\b'),
    ('greeting', r'^(hi|hello|hey|yo|kumusta|musta|good (morning|afternoon|evening))\b'),
]

SUGGESTIONS = {
    'visitor': ['How do I play?', 'How long is the wait?', 'Top score today?', 'Is my student ID safe?'],
    'waiting': ['When is my turn?', 'Tips for my first game', 'What if I miss my turn?', 'Top score today?'],
    'called': ['What do I do now?', 'Tips for my first game', 'What if I miss my turn?'],
    'playing': ['How do I play?', 'Tips for my first game'],
    'completed': ['How did I do?', 'Where did I lose it?', 'Tips for next time', 'Play again?'],
    'closed': ['Play again?', 'How do I play?', 'Top score today?'],
}


def normalize(text):
    text = unicodedata.normalize('NFKC', text or '').lower()
    return re.sub(r'\s+', ' ', re.sub(r"[^\w\s'/-]", ' ', text)).strip()


def is_tagalog(text):
    words = set(text.split())
    return len(words & TAGALOG) >= 1 and not re.search(r'\b(the|is|what|how|when|my)\b', text)


def classify(text):
    for name, pattern in INTENTS:
        if re.search(pattern, text):
            return name
    return 'unknown'


def stage(facts):
    ticket = facts.get('ticket')
    if not ticket:
        return 'visitor'
    status = ticket['status']
    if status in ('waiting', 'called', 'playing', 'completed'):
        return status
    if status == 'review':
        return 'playing'
    return 'closed'


def minutes(seconds):
    value = max(1, round(seconds / 60))
    return f'about {value} minute' + ('' if value == 1 else 's')


def line_sentence(facts, tl=False):
    count, cabinet = facts['inLine'], facts['cabinet']
    if not facts['admissionsOpen']:
        return ('Naka-pause muna ang pila. Ang mga nasa pila na ay may hawak pa ring pwesto.' if tl else
                'The line is paused for a moment. Players already in line keep their place.')
    if cabinet == 'offline':
        return ('Nagre-reconnect ang cabinet. Pwede ka pa ring sumali; naka-save ang pwesto mo.' if tl else
                'The cabinet is reconnecting. You can still join and your place is saved.')
    people = 'nobody' if count == 0 else ('1 player' if count == 1 else f'{count} players')
    wait = minutes(facts['roundSeconds'] * count) if count else 'no wait'
    if tl:
        return (f'{count} ang nasa pila ngayon, mga {max(1, round(facts["roundSeconds"] * count / 60))} minuto ang hintay.'
                if count else 'Walang nakapila ngayon. Pwede kang maglaro agad pag tinawag ka ng operator.')
    state = 'The cabinet is ready.' if cabinet == 'ready' else 'A round is in progress.'
    return f'{state} {people.capitalize()} in line right now, so {wait}.' if count else f'{state} Nobody is in line, so you can play as soon as the operator calls you.'


def answer(question, facts):
    """Return {'answer', 'source', 'intent', 'suggestions'} for one question."""
    text = normalize(question)
    where = stage(facts)
    suggestions = SUGGESTIONS[where]
    if ID_LIKE.search(question or ''):
        return {'intent': 'privacy', 'source': 'Privacy', 'suggestions': suggestions,
                'answer': 'Please don’t share your student ID here. I don’t need it, and nobody can see your ID on the ticket or the leaderboard.'}
    tl = is_tagalog(text)
    intent = classify(text)
    rules, ticket = facts['rules'], facts.get('ticket')
    levels, seconds = rules['levels'], rules['round_limit_ms'] // 1000

    def reply(body, source):
        return {'intent': intent, 'answer': body, 'source': source, 'suggestions': suggestions}

    if intent == 'how_to_play':
        if tl:
            return reply(f'Pindutin ang malaking button para ibagsak ang gumagalaw na row sa stack. Napuputol ang sobra kaya kumikitid ang row. '
                         f'Abutin ang {levels} levels sa loob ng {seconds} segundo para manalo; 1 point bawat level.', 'Game rules')
        return reply(f'Press the big button to drop the moving row onto the stack. Any part hanging over the edge is cut off, so the row gets narrower. '
                     f'Reach all {levels} levels within {seconds} seconds to win. You get 1 point per level.', 'Game rules')
    if intent == 'tips':
        return reply('Watch the rhythm and press as the row lines up with the stack. Rows move a little faster as you climb, '
                     'so keep the stack wide in the early levels: every cell you lose stays lost.', 'Game rules')
    if intent == 'privacy':
        return reply('Your student ID is encrypted and only used so each student holds one place in line. It never appears on your ticket, '
                     'the leaderboard or in this chat, and it is deleted after the event.', 'Privacy')
    if intent == 'join':
        if ticket and where in ('waiting', 'called', 'playing'):
            return reply('You’re already in line. Keep this page open; it updates by itself.', 'Your ticket')
        return reply('Scan the QR on the screen beside Cabinet 01 with your phone camera, then pick a nickname. Your ticket keeps your place.', 'Event rules')
    if intent == 'miss_turn':
        return reply('When you’re called you have about 3 minutes to reach Cabinet 01 and press the button. If you can’t make it, '
                     'tell the operator; your turn may be released so the next player can go.', 'Event rules')
    if intent == 'play_again':
        if where in ('waiting', 'called', 'playing'):
            return reply('Finish this round first. Afterwards, scan the QR at Cabinet 01 again to rejoin the end of the line.', 'Event rules')
        return reply('Scan the QR at Cabinet 01 again to rejoin the end of the line.', 'Event rules')
    if intent == 'top_score':
        best = facts.get('bestToday')
        if best is None:
            return reply('No rounds have finished today yet. You could set the first score!', 'Today’s scores')
        # Scores are points (Matrix v1: one per level; Classic v1 scored differently), so "the top"
        # is counted by the highest level reached, never by comparing a score with the level count.
        top = facts.get('topCount', 0)
        tail = (f' {top} player{"" if top == 1 else "s"} reached all {levels} levels so far.' if top
                else f' Nobody has reached all {levels} levels yet today.')
        return reply(f'The best score today is {best} point{"" if best == 1 else "s"}.{tail}', 'Today’s scores')
    if intent in ('my_turn', 'wait') and ticket and where == 'waiting':
        position = ticket.get('position') or 1
        ahead = position - 1
        if not facts['admissionsOpen']:
            return reply(f'You’re #{position}. The line is paused for a moment, but your place is saved.', 'Your ticket · live')
        if tl:
            return reply(f'Ikaw ang #{position}. Mga {max(1, round(facts["roundSeconds"] * position / 60))} minuto pa bago ka tawagin.', 'Your ticket · live')
        if ahead == 0:
            return reply('You’re next! The operator calls you as soon as the cabinet is ready.', 'Your ticket · live')
        return reply(f'You’re #{position} with {ahead} player{"" if ahead == 1 else "s"} ahead, so {minutes(facts["roundSeconds"] * position)}. '
                     'Your phone tells you when it’s your turn.', 'Your ticket · live')
    if intent == 'my_turn' and ticket and where == 'called':
        return reply('It’s your turn now! Go to Cabinet 01 and press the big button within about 3 minutes to start.', 'Your ticket · live')
    if intent == 'my_turn' and ticket and where == 'playing':
        return reply('Your round is running at the cabinet. Your result will appear here automatically.', 'Your ticket · live')
    if intent in ('my_turn', 'wait'):
        if intent == 'my_turn' and not ticket:
            return reply('You’re not in line yet. Scan the QR at Cabinet 01 to join. ' + line_sentence(facts), 'Live line · just now')
        return reply(line_sentence(facts, tl), 'Live line · just now')
    if intent in ('my_result', 'lost'):
        result = facts.get('round')
        if not result:
            return reply('Your result appears here after your round. Ask me again once you’ve played!', 'Your ticket')
        if intent == 'my_result':
            outcome = 'You reached the top!' if result['won'] else f'You kept {result["score"]} of {levels} rows.'
            higher, total = result.get('higherToday', 0), result.get('roundsToday', 0)
            standing = (f' {higher} of {total} rounds today scored higher.' if higher else f' That’s the best score of {total} rounds today!') if total else ''
            return reply(outcome + standing, 'Your round · today’s scores')
        if result['won']:
            return reply(f'You didn’t lose it: you cleared all {levels} levels. Try to beat your time next round!', 'Your round')
        first = result.get('firstLoss')
        ended = {'zero_overlap': 'the row missed the stack completely', 'timeout': 'the 60-second timer ran out'}.get(result.get('reason'), 'the round ended')
        lost_part = (f'You first lost width at level {first["level"]}, keeping {first["kept"]} of {first["width"]} cells. '
                     if first else 'You kept full width the whole way. ')
        return reply(f'{lost_part}The round ended at level {result["level"]} because {ended}.', 'Your round')
    if intent == 'thanks':
        return reply('Walang anuman! Good luck sa stack.' if tl else 'You’re welcome. Good luck with your stack!', 'Stack Intelligence')
    if intent == 'greeting':
        return reply('Hello! Tanong ka lang tungkol sa laro, sa pila o sa scores.' if tl else
                     'Hi! Ask me how to play, how long the line is, or about today’s scores.', 'Stack Intelligence')
    return {'intent': 'unknown', 'source': '', 'suggestions': suggestions,
            'answer': ('Tungkol lang sa laro ang kaya kong sagutin: paano maglaro, ang pila, at ang scores ngayon.' if tl else
                       'I can only help with the game: how to play, the line and today’s scores. Try one of the suggestions.')}
