"""Domain-level request constraints. Explicit subjects outrank history and examples."""

import re


# Public foreign subjects cannot be reinterpreted as this event's queue or scores.
FOREIGN_SUBJECTS = frozenset("""
football basketball tennis volleyball cricket bowling baseball golf hockey darts chess pinball
airport supermarket restaurant bangko passengers printer elevator refrigerator
""".split())
FOREIGN_VENUE = re.compile(
    r"\b(?:another|different|other|ibang) (?:[a-z]+ ){0,2}(?:arena|arcade|venue|booth|event|game|tournament)\b")


def outside_event(text):
    return bool(set(re.findall(r"[a-z]+", text)) & FOREIGN_SUBJECTS or FOREIGN_VENUE.search(text))


SCORE = {'score','scores','scored','puntos','points'}
QUEUE = {'queue','queued','queuing','pila','nakapila','waiting','admissions'}
MACHINE = {'cabinet','machine','esp32','heartbeat','rssi','firmware','wifi','wi-fi','connectivity','connection','connected'}
REGISTRATION = {'registered','registration','registrations','joined','rehistrado','nagregister','rehistro'}
COMPLETED = {'completed','finished','played','naglaro','nakatapos','natapos'}
OPERATORS={'average':{'average','avg','mean'},'total':{'total','sum','combined','cumulative','aggregate','kabuuan','kabuuang'},
           'highest':{'highest','max','maximum','pinakamataas'},'lowest':{'lowest','min','minimum','pinakamababa'}}
SEMANTIC_VOCAB=SCORE|QUEUE|MACHINE|REGISTRATION|COMPLETED|set().union(*OPERATORS.values())|set('define definition meaning means calculate calculated kinukwenta ibig sabihin histogram distribution distributed spread buckets leaderboard top ranking rank leading nangunguna who sino bawat nila sila lahat next page everyone everybody anyone anybody altogether arithmetic reachable require requires kept privately font family typeface long'.split())


def semantic_words(normalized):
    words=set(normalized['safe_tokens']) | {word for hint in normalized.get('meaning_hints',[]) for word in hint.split()}
    tokens=normalized['safe_tokens']
    # "mean by the total score" uses a verb, whereas "mean score" and
    # "mean of the scores" name an arithmetic measure. Looking several words
    # ahead accidentally turned every definition containing "mean by" into average.
    mean_noun=any(token=='mean' and index+1<len(tokens) and tokens[index+1] in SCORE|{'of','value'}
                  for index,token in enumerate(tokens))
    aliases_to_ignore={'mean'} if words&{'do','does','did'} and not mean_noun else set()
    return words|{name for name,aliases in OPERATORS.items() if words&(aliases-aliases_to_ignore)}
REFERENCE_WORDS=set('what how about and the for in on please kindly paki naman po instead same now today yesterday kahapon ngayon ngayong last seven days araw nakaraang pitong source sources simulator simulation simulated physical device results all both only it them those next page could would can you show check just actually again'.split())


def refers_to_previous(normalized):
    words=semantic_words(normalized)
    return bool(words) and words<=REFERENCE_WORDS and bool(normalized['requested_period'] or normalized['requested_source'] or {'next','page'}<=words)


def reviewed_explanation(normalized):
    """Distinguish reviewed design explanations from measurements of live services."""
    words=semantic_words(normalized)
    topic=normalized.get('system_topic_hint')
    simulation=bool(words & {'simulator','simulated','simulation'})
    physical=bool(words & {'device','physical','real','esp','esp32','cabinet'})
    if simulation and physical and words & {'prove','proof','verify','verified','confirm','confirms','validate'}:
        return 'offline'
    if simulation and physical and words & {'results','scores','ranking','rankings'} and words & {'separate','separated','separation','mix','mixed'} and words & {'how','why','do','does','are','explain','stay','kept'} and not words & {'many','count','number','show','list'}:
        return 'results'
    queue_subject=bool(words & QUEUE or {'next','player'} <= words)
    workflow=bool(words & {'work','works','workflow','assignment','role'} or
                  ('who' in words and words & {'calls','assigns','operator'}) or
                  ('how' in words and words & {'calls','assigns','assign'}))
    if queue_subject and words & {'who','how','explain','describe'} and workflow:
        return 'queue_flow'
    if words & {'privacy','private','encrypted','encryption'} and words & {'why','how','explain','bakit','paano'} and words & {'identifiers','identity','registration','id','ids'}:
        return 'privacy'
    if topic=='privacy': return topic
    if topic=='architecture' and words & {'how','why','explain','describe','roles','architecture','uses','use'}:
        return topic
    if topic=='dashboard' and words & {'font','typeface'}: return topic
    # Curated system explanations need no model inference. Do not confuse a
    # recorded value/state request with documentation about that same subsystem.
    design = bool(words & {'how','why','explain','describe','work','works','workflow','purpose','rules','guide','instructions','procedure','process','flow','journey','mechanics','role','roles','daloy'})
    live = bool(words & {'count','many','number','currently','current','today','yesterday','now','status','connected','readiness'})
    if design and not live and topic in {'gameplay','registration','architecture','dashboard','memory','training','offline'}:
        return topic
    if topic in {'memory','training'} and words & {'what','can','does','do'} and not live:
        return topic
    return None


def constraints(normalized):
    words=semantic_words(normalized)
    if reviewed_explanation(normalized): return None
    operational = words & {'update','handover','overview','briefing','snapshot','status','summary','lagay'}
    if operational and words & {'event','carnival','booth'} and not words & (SCORE|QUEUE|MACHINE|REGISTRATION|{'levels','level','players','wins','losses','accuracy','time','period','source','dashboard','architecture'}):
        return {'tools':['get_event_summary','get_queue_summary','get_machine_summary'],'definition':None}
    if words & QUEUE and words & {'stuck','nakahinto'}:
        return {'tools':['get_queue_summary','get_machine_summary'],'definition':None}
    if words & {'overview','summary','summarize','buod'} and words & {'event','carnival','whole','entire','system','game','games'} and not words & (SCORE|QUEUE|MACHINE|REGISTRATION|{'level','levels','accuracy','wins','losses'}):
        return {'tools':['get_event_summary','get_queue_summary','get_machine_summary'],'definition':None}
    definition=bool(words & {'define','definition','meaning','means','formula','significance'} or {'ibig','sabihin'}<=words or
                    (words & {'how','paano'} and words & {'scoring','calculate','calculated','kinukwenta','award','awards','awarded'}) or ('mean' in words and words&{'do','does','did'}) or
                    ('metric' in words and words & {'represent','represents','denominator','numerator'}) or
                    ('what' in words and {'meant','by'} <= words))
    explanation=bool(words & {'explain','describe','work','works','workflow','rules','architecture','protect','protected','encrypted'} or definition)
    explicit_measure = bool(words & (SCORE|QUEUE|MACHINE|REGISTRATION|{'level','levels','accuracy','wins','losses'}))
    general_state = bool(words & {'event','carnival'} and words & {'overall','whole','entire','general'} and
                         words & {'doing','going','progress','progressing','unfold','unfolding','running','happening','status','now','today','currently'})
    if general_state and not explicit_measure and not explanation:
        return {'tools':['get_event_summary','get_queue_summary','get_machine_summary'],'definition':None}
    if definition or ('explain' in words and words & (SCORE|{'accuracy','win_rate','scoring'})):
        metric='scoring' if words & (SCORE|{'scoring'}) else 'accuracy' if 'accuracy' in words else 'win_rate' if words & {'win','wins','winning'} else None
        if metric=='scoring':
            metric=next((name+'_score' for name in OPERATORS if name in words),'scoring')
        if metric: return {'tools':[],'definition':metric}
    # Explicit metric requests are authoritative even with generic player/pronoun words.
    tools=[]
    if words & SCORE:
        if words & {'top','leaderboard','leading','nangunguna'} or (words & {'who','sino','which'} and words & {'highest','best','most'}):
            tools.append('get_top_scores')
        elif words & {'average','mean','total','sum','highest','lowest'}:
            tools.append('get_event_summary')
        elif words & {'distribution','distributed','histogram','spread','buckets'}:
            tools.append('get_score_distribution')
        elif words & {'top','highest','best','leaderboard','leading','nangunguna','pinakamataas'}:
            tools.append('get_top_scores')
        elif not explanation: tools.append('get_player_scores')
        if words & {'distribution','distributed','histogram','spread','buckets'} and 'get_score_distribution' not in tools:
            tools.append('get_score_distribution')
    if words & {'level','levels','row','rows'} and words & {'attempts','attempt','placement','placements','failed','failure','failures','performance','miss','misses'} and not explanation:
        tools.append('get_level_statistics')
    if words & {'accuracy','overlap','failures','misses','difficult','difficulty','hardest'} and not explanation:
        tools.append('get_level_statistics' if words & {'level','levels','antas'} else 'get_event_summary')
    if words & {'win','wins','winning','panalo','loss','losses','talo','timeout','timeouts','duration'} and not explanation:
        tools.append('get_event_summary')
    peak_question=bool(words & {'when','kailan'} and words & {'most','pinakamaraming','busiest'} and words & {'games','laro','event','activity','players'})
    if (words & {'trend','trends','busiest','hourly','daily','activity'} or peak_question) and not explanation: tools.append('get_play_trend')
    if words & QUEUE and not explanation:
        tools.append('get_queue_summary')
        if words & {'stuck','why','bakit','readiness'}: tools.append('get_machine_summary')
    if words & MACHINE and not explanation and (not words & SCORE or words & {'heartbeat','rssi','firmware','connection','connectivity','connected'}): tools.append('get_machine_summary')
    if not tools and words & (REGISTRATION|COMPLETED) and not explanation: tools.append('get_event_summary')
    if not tools and words & {'top','leaderboard','leading','nangunguna'} and not explanation: tools.append('get_top_scores')
    if tools: return {'tools':list(dict.fromkeys(tools))[:5],'definition':None}
    if words & {'players','player','participants','students'} and words & {'many','count','number','total'} and not explanation:
        return {'tools':['get_event_summary'],'definition':None}
    return None


def compatible(target, normalized):
    """A reviewed label is a hint, not permission to substitute another subject."""
    if normalized.get('requires_scope_check'): return True
    explanation=reviewed_explanation(normalized)
    if explanation: return target.get('topic')=='knowledge' and target.get('knowledge')==explanation
    needed=constraints(normalized)
    if needed is None: return True
    if needed['definition']: return target.get('topic')=='definition' and target.get('definition')==needed['definition']
    if set(needed['tools']) == {'get_event_summary','get_queue_summary','get_machine_summary'}:
        return target.get('topic') == 'overview'
    topics={'get_player_scores':{'scores'},'get_score_distribution':{'scores'},'get_top_scores':{'top'},
            'get_event_summary':{'players','scores'} if set(normalized['safe_tokens'])&SCORE else {'players'},
            'get_queue_summary':{'queue'},'get_machine_summary':{'machine'},
            'get_level_statistics':{'levels'},'get_play_trend':{'trend'}}
    return target.get('topic') in set().union(*(topics[t] for t in needed['tools']))


def resolve_subject(normalized, previous):
    """Fill only an omitted measure from typed context, never overwrite a current one."""
    if previous is None or normalized['has_unrecognized_words'] or normalized.get('requires_scope_check') or constraints(normalized): return normalized,False
    words=semantic_words(normalized)
    score_subject=bool(set(previous.tools)&{'get_player_scores','get_top_scores','get_score_distribution'} or
                       any(metric.endswith('_score') for metric in previous.metrics) or
                       previous.definition in {'scoring','average_score','total_score','highest_score','lowest_score'})
    if score_subject and words&OPERATORS.keys():
        return dict(normalized,safe_tokens=normalized['safe_tokens']+['score']),True
    return normalized,False
