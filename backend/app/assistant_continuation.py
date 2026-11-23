"""Resolve complete, public filter edits against validated conversation state."""
import re

from .assistant_language import linguistic_text


# Consume slot expressions before checking the rest of the utterance. Unmatched
# content stays visible so an unrelated subject cannot inherit an event query.
SLOTS = {
    'period': {
        'today': r"today(?:'s)?|ngayong araw|ngayon",
        'yesterday': r"yesterday(?:'s)?|kahapon|previous day|preceding day|day before today",
        'last_7_days': r"(?:past|last|previous) (?:7|seven) days|(?:nakaraang|huling) (?:7|pitong) araw",
        'event_to_date': r"event to date|(?:whole|entire|full) event|buong event",
    },
    'source': {
        'all': r"(?:all|both|parehong) (?:result )?sources|simulator and (?:physical )?device",
        'simulator': r"simulated(?: games?)?|simulation|simulator",
        'device': r"physical(?: (?:device|controller|cabinet))?|device",
    },
    'detailed': {
        False: r"shorter|short|brief|concise|condense|shorten|paikliin",
        True: r"more detail(?:s|ed)?|more fully|more about|more on|a little more|tell me more|detailed|elaborate|expand|dagdagan|pahabain",
    },
    'language': {'en':r'english', 'taglish':r'taglish|tagalog|filipino'},
}
SLOT_PATTERNS = [(key, value, re.compile(r"\b(?:"+pattern+r")\b")) for key, choices in SLOTS.items()
                 for value, pattern in choices.items()]
NUMBERS = "zero one two three four five six seven eight nine ten eleven twelve".split()
TAGALOG = "sero isa dalawa tatlo apat lima anim pito walo siyam sampu".split()
NUMERAL = {word:n for names in (NUMBERS,TAGALOG) for n,word in enumerate(names)}
NUMBER = re.compile(r"\b(?:\d+|"+"|".join(NUMERAL)+r")\b")
REFERENCE = set("that this those it same again previous preceding following next previous last iyon iyan yan yun parehong pareho ganoon dating nasabing".split())
FILLER = set("""
a an the and but for from in of on to with as by at into onto over within instead still too now just only
what how about could can would we you me please kindly show see give tell explain make use keep switch change
set repeat continue extend narrow widen include take do look apply go back bring redo using want let's lets
request question answer view version window period range time source sources cohort result results list listing
report detail details explanation breakdown measure filter filters analysis page number size length little more
pa paki po naman lang lamang muna ngayon ang ng sa ay para pero din rin ko mo natin na pa ring iyong yung
tanong sagot tingnan gamitin gawing gawin mong ulitin ipakita pakita ituloy palitan balik naman dati ulit
""".split())
SUBJECTS = {
    'get_player_scores': {'score','scores','puntos'},
    'get_top_scores': {'ranking','rankings','leaders','leaderboard','top'},
    'get_play_trend': {'trend','timeline'},
    'get_level_statistics': {'level','levels','antas'},
    'get_queue_summary': {'queue','pila'},
    'get_machine_summary': {'machine','cabinet'},
}
PAGE = re.compile(r"\b(?:next|following|previous|preceding|kasunod|susunod|nakaraan)(?: na| nitong)? (?:score )?page\b")
def continuation(question, previous):
    """Return (matched, updated Context). A matched edit without a subject clarifies."""
    text = linguistic_text(question).strip()
    if not re.fullmatch(r"[a-z0-9\s'?,.!-]+",text):
        return False, None
    text = ' '.join(re.sub(r"[?,.!-]",' ',text).split())
    words = set(text.split())
    updates = {}
    conflicting = False
    page = PAGE.search(text)
    if page:
        direction = -1 if page[0].startswith(('previous','preceding','nakaraan')) else 1
        updates['score_page'] = (previous.score_page if previous else 1) + direction
        text = PAGE.sub(' ',text,count=1)
    for key, value, pattern in SLOT_PATTERNS:
        if pattern.search(text):
            if key in updates and updates[key] != value:
                conflicting = True
            updates[key] = value
            text = pattern.sub(' ',text)
    subject_words = set(text.split())
    subjects = {tool for tool, names in SUBJECTS.items() if subject_words & names}
    number = NUMBER.search(text)
    if number:
        if subjects == {'get_level_statistics'}:
            field, upper = 'level', 15
        elif subjects == {'get_top_scores'} or (previous and previous.tools==['get_top_scores'] and 'list' in subject_words):
            field, upper = 'limit', 10
        else:
            return False, None
        n = int(number[0]) if number[0].isdigit() else NUMERAL[number[0]]
        if not 1 <= n <= upper:
            return True, None
        updates[field] = n
        text = text[:number.start()]+' '+text[number.end():]
    residue = set(text.split()) - REFERENCE - FILLER
    for tool in subjects:
        residue -= SUBJECTS[tool]
    if residue == {'or'} and updates:
        return True, None
    if residue:
        return False, None
    if not updates:
        # A bare demonstrative has no executable operation or recoverable subject.
        if words & REFERENCE and words <= REFERENCE | {'please','po','naman','the','one','other','option','yung','ang','sa','pa'}:
            return True, None
        return False, None
    if subjects and not (words & REFERENCE or page):
        return False, None
    if subjects and previous and not subjects <= set(previous.tools):
        return False, None
    if conflicting:
        return True, None
    if not previous or not (previous.tools or previous.definition or previous.knowledge):
        return True, None
    if 'score_page' in updates and ('get_player_scores' not in previous.tools or not 1 <= updates['score_page'] <= 2000):
        return True, None
    if not previous.tools and updates.keys() & {'period','source','limit','level','score_page'}:
        return True, None
    return True, previous.model_copy(update=updates)

