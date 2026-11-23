"""Human-reviewed, owner-scoped routing examples. Never ingests raw conversation/answers."""
import hashlib
import json
from typing import Literal, get_args
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from .assistant import Context, Definition, DEFINITIONS, NORMALIZATION_VERSION, POLICY, PROMPT, RoutingPlan, TAGLISH_HINTS, VOCABULARY, normalize
from .assistant_knowledge import KNOWLEDGE, Knowledge, Social
from .analytics import Period, ChatSource
from .assistant_language import ALIASES, CONTRACTIONS
from .assistant_language import lexical_resource
from .database import all_rows, execute, one


class TrainingInput(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    safe_tokens: list[str] = Field(min_length=1, max_length=150)
    level_number: int | None = Field(default=None, ge=1, le=12)
    top_number: int | None = Field(default=None, ge=1, le=10)
    has_unrecognized_words: bool = False
    requires_scope_check: bool = False
    system_topic_hint: Knowledge | None = None
    language_hint: Literal['en','taglish'] = 'en'
    meaning_hints: list[str] = Field(default_factory=list, max_length=50)
    requested_period: Period | None = None
    requested_source: ChatSource | None = None
    previous: Context | None = None
    prior_contexts: list[Context] = Field(default_factory=list, max_length=6)

    @field_validator('safe_tokens')
    @classmethod
    def approved_words_only(cls, tokens):
        if any(token not in VOCABULARY for token in tokens):
            raise ValueError('Only approved normalized vocabulary can be reviewed.')
        if len(' '.join(tokens))>1000: raise ValueError('Normalized input is too long.')
        _, blocked = normalize(' '.join(tokens))
        if blocked: raise ValueError('Private, control or unsupported input cannot become an example.')
        return tokens

    @field_validator('meaning_hints')
    @classmethod
    def approved_meanings_only(cls, values):
        if any(value not in TAGLISH_HINTS.values() for value in values):
            raise ValueError('Unknown meaning hint.')
        return values


class TrainingTarget(RoutingPlan):
    @model_validator(mode='after')
    def one_consistent_label(self):
        required = {'knowledge':'knowledge', 'social':'social', 'definition':'definition'}
        for field in ('knowledge','social','definition'):
            value = getattr(self, field)
            if required.get(self.topic) == field:
                if value is None: raise ValueError('Select the matching response label.')
            elif value is not None:
                raise ValueError('Unrelated response labels must be empty.')
        return self


class Proposal(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    input: TrainingInput
    target: TrainingTarget

    @model_validator(mode='after')
    def grounded_label(self):
        if self.target.topic=='follow_up' and (self.input.previous is None or not (
            self.input.previous.tools or self.input.previous.definition or self.input.previous.knowledge)):
            raise ValueError('A follow-up example requires an approved previous subject.')
        if self.target.topic=='knowledge' and self.input.system_topic_hint and self.target.knowledge!=self.input.system_topic_hint:
            raise ValueError('A knowledge label must match the explicit reviewed system subject.')
        return self


class Review(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    revision: int = Field(ge=0)
    decision: Literal['revise','approve','reject']
    target: TrainingTarget
    reviewed: bool = False
    context_version: str | None = Field(default=None,pattern=r'^[0-9a-f]{64}$')


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':'))


def context_version():
    from .assistant_learning import corpus_digest
    public = {'policy':POLICY,'normalizer':NORMALIZATION_VERSION,'prompt':PROMPT,'knowledge':KNOWLEDGE,'definitions':DEFINITIONS,'vocabulary':sorted(VOCABULARY),
              'language_aliases':ALIASES,'language_contractions':CONTRACTIONS,
              'public_lexicon_sha256':lexical_resource()[1],
              'routing_corpus':corpus_digest(),
              'input_schema':TrainingInput.model_json_schema(),'target_schema':RoutingPlan.model_json_schema()}
    return hashlib.sha256(canonical(public).encode()).hexdigest()


class TrainingStore:
    def __init__(self, engine): self.engine = engine

    def options(self):
        return {'topics':RoutingPlan.model_json_schema()['properties']['topic']['enum'],
                'knowledge':list(get_args(Knowledge)), 'social':list(get_args(Social)),
                'definition':list(get_args(Definition)), 'context_version':context_version(),
                'purpose':'Reviewed intent-routing examples. No raw chat, answers, player records or automatic training.'}

    def view(self, row):
        return {'id':row['public_id'],'input':TrainingInput.model_validate_json(row['input_json']).model_dump(),
                'target':TrainingTarget.model_validate_json(row['target_json']).model_dump(),
                'status':row['status'],'revision':row['revision'],
                'current':row['context_version']==context_version(),
                'created_at':row['created_at'].isoformat()+'Z'}

    def list(self, staff_id, before=None):
        with self.engine.connect() as connection:
            rows = all_rows(connection, '''SET STATEMENT max_statement_time=1 FOR SELECT * FROM ai_training_examples
                WHERE staff_user_id=:staff AND (:before IS NULL OR id<:before) ORDER BY id DESC LIMIT 26''', staff=staff_id, before=before)
        items, skipped = [], 0
        for row in rows[:25]:
            try: items.append(self.view(row))
            except (ValidationError, ValueError, TypeError): skipped += 1
        return {'items':items,'next_cursor':rows[24]['id'] if len(rows)>25 else None,
                'skipped_invalid':skipped,'context_version':context_version()}

    def propose(self, staff_id, proposal):
        fingerprint = hashlib.sha256(canonical(proposal.input.model_dump()).encode()).hexdigest()
        with self.engine.begin() as connection:
            # Lock the account row: bound the review queue even for concurrent proposals.
            one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT id FROM staff_users WHERE id=:staff FOR UPDATE', staff=staff_id)
            existing = one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT * FROM ai_training_examples WHERE staff_user_id=:staff AND input_hash=:hash', staff=staff_id, hash=fingerprint)
            if existing: return dict(self.view(existing), duplicate=True)
            count = one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT COUNT(*) AS total FROM ai_training_examples WHERE staff_user_id=:staff', staff=staff_id)
            if count['total']>=1000: raise HTTPException(409,'The example limit is reached. Remove examples before adding more.')
            public_id = str(uuid.uuid4())
            execute(connection, '''SET STATEMENT max_statement_time=1 FOR INSERT INTO ai_training_examples
                (public_id,staff_user_id,input_hash,input_json,target_json,context_version,policy_version)
                VALUES(:id,:staff,:hash,:input,:target,:context,:policy)''',
                id=public_id, staff=staff_id, hash=fingerprint, input=canonical(proposal.input.model_dump()),
                target=canonical(proposal.target.model_dump()), context=context_version(), policy=POLICY)
            row=one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT * FROM ai_training_examples WHERE public_id=:id AND staff_user_id=:staff', id=public_id, staff=staff_id)
            return dict(self.view(row), duplicate=False)

    def review(self, staff_id, public_id, review):
        if review.decision=='approve' and not review.reviewed:
            raise HTTPException(422,'Confirm that you reviewed the sanitized input and labels before approval.')
        if review.decision=='approve' and review.context_version!=context_version():
            raise HTTPException(409,'The system context changed. Reopen the review queue before approving.')
        with self.engine.begin() as connection:
            row=one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT * FROM ai_training_examples WHERE public_id=:id AND staff_user_id=:staff FOR UPDATE', id=public_id, staff=staff_id)
            if not row: raise HTTPException(404,'Example not found.')
            if row['revision']!=review.revision: raise HTTPException(409,'The example changed. Reload it before reviewing.')
            # Revalidate stored input on approval, including after context/policy changes.
            if review.decision!='reject':
                try: Proposal(input=TrainingInput.model_validate_json(row['input_json']),target=review.target)
                except (ValidationError, ValueError, TypeError):
                    raise HTTPException(422,'The input and label do not match the current reviewed schema.') from None
            status={'revise':'pending','approve':'approved','reject':'rejected'}[review.decision]
            execute(connection, '''SET STATEMENT max_statement_time=1 FOR UPDATE ai_training_examples
                SET target_json=:target,status=:status,revision=revision+1,context_version=:context,
                    policy_version=:policy,reviewed_at=IF(:status='pending',NULL,UTC_TIMESTAMP(3))
                WHERE public_id=:id AND staff_user_id=:staff''', id=public_id, staff=staff_id,
                target=canonical(review.target.model_dump()), status=status, context=context_version(), policy=POLICY)
            return self.view(one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT * FROM ai_training_examples WHERE public_id=:id AND staff_user_id=:staff', id=public_id, staff=staff_id))

    def remove(self, staff_id, public_id):
        with self.engine.begin() as connection:
            result=execute(connection, 'SET STATEMENT max_statement_time=1 FOR DELETE FROM ai_training_examples WHERE public_id=:id AND staff_user_id=:staff', id=public_id, staff=staff_id)
            if not result.rowcount: raise HTTPException(404,'Example not found.')
        return {'removed':True}

    def export(self, staff_id):
        version=context_version()
        with self.engine.connect() as connection:
            rows=all_rows(connection, '''SET STATEMENT max_statement_time=2 FOR SELECT input_json,target_json
                FROM ai_training_examples WHERE staff_user_id=:staff AND status='approved'
                AND context_version=:context AND policy_version=:policy ORDER BY id LIMIT 1000''', staff=staff_id, context=version, policy=POLICY)
        lines=[]
        for row in rows:
            try:
                model_input=TrainingInput.model_validate_json(row['input_json'])
                target=TrainingTarget.model_validate_json(row['target_json'])
                Proposal(input=model_input,target=target)
            except (ValidationError, ValueError, TypeError): continue
            lines.append(json.dumps({'messages':[{'role':'system','content':PROMPT},
                {'role':'user','content':json.dumps(model_input.model_dump(),ensure_ascii=False)},
                {'role':'assistant','content':json.dumps(target.model_dump(),ensure_ascii=False)}]},ensure_ascii=False))
        if not lines: raise HTTPException(409,'No approved examples match the current system context. Review and approve an example first.')
        return {'jsonl':'\n'.join(lines)+'\n','count':len(lines),'context_version':version,
                'filename':'stack-intelligence-routing-approved.jsonl','automatic_training':False}
