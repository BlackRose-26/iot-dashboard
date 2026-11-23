"""Bounded local retrieval of sanitized routing examples, never historical facts."""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from .database import all_rows
from .assistant_interactions import INTERACTIONS, BEHAVIORAL
from .assistant_semantics import compatible
from .assistant_language import GRAMMAR

CORPUS = Path(__file__).resolve().parents[1] / 'data' / 'assistant-routing.json'
CONTRASTS = CORPUS.with_name('assistant-routing-contrasts.json')
RUNTIME_CORPORA = (CORPUS,INTERACTIONS,BEHAVIORAL,CONTRASTS)
STOP = set('a an the is are was were be do does did can could would should will what which how why who me my us our this that it its they their them there here of in on at to for from and or please paki po ang ng sa ba mga'.split())
STOP |= GRAMMAR - {'how','why','when','who','what','explain','describe','current','currently','recorded','today','yesterday','now','earlier','previous','prior','latest','long','longer','short','brief','detailed','detail','details'}


def corpus_digest():
    return hashlib.sha256(b'\0'.join(path.read_bytes() for path in RUNTIME_CORPORA)).hexdigest()


def seed_examples():
    return _seed_examples(corpus_digest())


@lru_cache(maxsize=1)
def _seed_examples(version):
    from .assistant import normalize
    from .assistant_training import Proposal, TrainingInput, TrainingTarget
    result = []
    rows = [row for path in RUNTIME_CORPORA for row in json.loads(path.read_text(encoding='utf-8'))['examples']]
    for row in rows:
        if row['split']!='train': continue
        normalized, blocked = normalize(row['question'])
        if blocked: continue
        sample = Proposal(input=TrainingInput(**normalized,previous=row.get('previous')),
                          target=TrainingTarget(**row['target']))
        result.append((sample.input.model_dump(),sample.target.model_dump(),'project'))
    return tuple(result)


def signature(sample):
    # A follow-up must match its typed previous subject; recent history is only a hint.
    return json.dumps({key:value for key,value in sample.items() if key!='prior_contexts'},sort_keys=True)


def retrieve(engine, staff_id, normalized, previous=None, use_memory=True):
    from .assistant_training import Proposal, context_version
    examples = list(seed_examples())
    available = True
    if use_memory and engine is not None:
        try:
            with engine.connect() as connection:
                rows = all_rows(connection, '''SET STATEMENT max_statement_time=1 FOR
                    SELECT input_json,target_json FROM ai_training_examples
                    WHERE staff_user_id=:staff AND status='approved' AND context_version=:version
                    ORDER BY id DESC LIMIT 1000''',staff=staff_id,version=context_version())
            for row in rows:
                try:
                    sample = Proposal.model_validate({'input':json.loads(row['input_json']),'target':json.loads(row['target_json'])})
                    examples.append((sample.input.model_dump(),sample.target.model_dump(),'reviewed_chat'))
                except (ValidationError,ValueError,TypeError): continue
        except SQLAlchemyError:
            available = False
    current = {**normalized,'previous':previous,'prior_contexts':[]}
    current_words = semantic_features(normalized)-STOP
    ranked = []
    for sample,target,origin in examples:
        if not compatible(target,normalized): continue
        exact = signature(sample)==signature(current) and not normalized['has_unrecognized_words'] and not normalized.get('requires_scope_check')
        words = semantic_features(sample)-STOP
        overlap = current_words & words
        score = len(overlap)/len(current_words|words) if current_words|words else 0
        if exact or (overlap and score>=0.2):
            ranked.append((exact,origin=='reviewed_chat',score,sample,target,origin))
    ranked.sort(key=lambda row:row[:3],reverse=True)
    # Conflicting exact human labels must be clarified rather than chosen arbitrarily.
    exact_owner = {json.dumps(row[4],sort_keys=True) for row in ranked if row[0] and row[1]}
    exact = ranked[0][4] if ranked and ranked[0][0] and ranked[0][1] and len(exact_owner)==1 else None
    demonstrations = []
    seen=set()
    for row in ranked:
        key=(tuple(row[3]['safe_tokens']),json.dumps(row[4],sort_keys=True))
        if key in seen: continue
        seen.add(key)
        sample = dict(row[3],prior_contexts=[])
        sample['safe_tokens'] = sample['safe_tokens'][:60]
        sample['meaning_hints'] = sample['meaning_hints'][:10]
        demonstration = {'input':sample,'target':row[4]}
        if len(json.dumps(demonstration))<=2000: demonstrations.append(demonstration)
        if len(demonstrations)==3: break
    return {'examples':demonstrations,'conflicting_corrections':len(exact_owner)>1,
            'exact':exact,'reviewed_matches':sum(row[1] for row in ranked[:3]),'available':available}


def semantic_features(sample):
    """Approved dictionary meanings reduce English/Taglish lexical mismatch."""
    from .assistant_semantics import semantic_words
    return semantic_words(sample) | {word for hint in sample.get('meaning_hints',[]) for word in hint.split()}


def interpretation_choices(normalized, routing):
    """Two domain-specific readings only when a supported question is ambiguous."""
    words = set(normalized['safe_tokens'])
    if normalized.get('requires_scope_check') and routing.topic in {'unsupported','knowledge','definition','social'}:
        return []
    if words & {'define','definition','explain','meaning','means','calculate','calculated','paano'}:
        return []
    pair = None
    if words & {'accuracy','accurate'} and not words & {'overall','whole','total','level','levels','antas'}:
        pair = [('Overall game accuracy','Show overall overlap accuracy.'),
                ('Accuracy by level','Show overlap accuracy by level.')]
    elif words & {'players','player','manlalaro'} and words & {'performance','progress','doing'} and not words & {'scores','score','wins','win','registered','completed','accuracy'}:
        pair = [('Player participation','How many players registered and completed a round?'),
                ('Player results','Show average score and win rate.')]
    elif routing.topic=='unsupported' and words & {'system','event','game','cabinet'} and words & {'performance','progress','health'}:
        pair = [('Event results','Give me an overview of the whole event.'),
                ('Cabinet readiness','What is the cabinet connection and readiness status?')]
    if pair is None: return []
    period = normalized.get('requested_period')
    source = normalized.get('requested_source')
    suffix = {'today':' Today.','yesterday':' Yesterday.','last_7_days':' Last seven days.','event_to_date':' Event to date.'}.get(period,'')
    suffix += {'all':' All sources.','device':' Physical device results.','simulator':' Simulator results.'}.get(source,'')
    return [{'label':label,'question':question+suffix} for label,question in pair]
