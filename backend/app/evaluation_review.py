"""Admin-only annotations for a consumed synthetic packet. No predictor imports this reader."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError

from .assistant import Context
from .assistant_training import TrainingTarget
from .database import all_rows, execute, one


PACKET = Path(__file__).resolve().parents[1] / 'evaluation/review/holdout-v2.json'


@lru_cache(maxsize=1)
def packet():
    try:
        raw = PACKET.read_bytes()
    except FileNotFoundError as error:
        raise HTTPException(503, 'The evaluation questions are unavailable.') from error
    rows = json.loads(raw)['cases']
    return hashlib.sha256(raw).hexdigest(), {r['id']:r for r in rows}


class Annotation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    target: TrainingTarget
    behavior: Literal['answer','refused','needs_clarification']
    expected_context: Context | None = None


class CaseReview(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: str = Field(pattern=r'^[0-9a-f]{64}$')
    revision: int = Field(ge=0)
    decision: Literal['confirm','correct','reject']
    annotation: Annotation | None = None


def proposed(case):
    return Annotation(target=case['target'],behavior=case['expected_behavior'],expected_context=case['expected_context'])


def read_reviews(connection, owner):
    version, cases = packet()
    rows = all_rows(connection, '''
        SELECT r.case_id,r.revision,r.decision,r.annotation FROM evaluation_case_reviews r
        JOIN (SELECT case_id,MAX(revision) rev FROM evaluation_case_reviews
              WHERE staff_user_id=:owner AND packet_version=:version GROUP BY case_id) latest
          ON latest.case_id=r.case_id AND latest.rev=r.revision
        WHERE r.staff_user_id=:owner AND r.packet_version=:version''',owner=owner,version=version)
    decisions = {r['case_id']:dict(revision=r['revision'],decision=r['decision'],
                 annotation=json.loads(r['annotation']) if r['annotation'] else None) for r in rows}
    return {'version':version,'cases':[{**c,'review':decisions.get(key)} for key,c in cases.items()]}


def save_review(connection, owner, case_id, body):
    version, cases = packet()
    if body.version != version:
        raise HTTPException(409,'The question set changed. Refresh the page.')
    if case_id not in cases:
        raise HTTPException(404,'Question not found.')
    reference = proposed(cases[case_id])
    annotation = body.annotation
    if body.decision == 'correct':
        if annotation is None or annotation == reference:
            raise HTTPException(422,'Choose what to change before saving.')
        if annotation.behavior=='answer':
            if annotation.target.topic=='unsupported':
                raise HTTPException(422,'For a question outside the game, choose a different action.')
            if annotation.target.topic=='follow_up' and (not cases[case_id]['previous'] or not annotation.expected_context):
                raise HTTPException(422,'A follow-up answer needs an earlier topic.')
        if annotation.expected_context and (annotation.target.topic!='follow_up' or annotation.behavior!='answer'):
            raise HTTPException(422,'Only an answered follow-up can carry earlier settings.')
    elif annotation is not None:
        raise HTTPException(422,'Only a correction takes new settings.')
    elif body.decision == 'confirm':
        annotation = reference
    params = dict(owner=owner,version=version,case=case_id)
    last = one(connection,'''SELECT MAX(revision) rev FROM evaluation_case_reviews
                WHERE staff_user_id=:owner AND packet_version=:version AND case_id=:case''',**params)
    if (last['rev'] or 0) != body.revision:
        raise HTTPException(409,'This review changed. Reload to see the latest choice.')
    revision = body.revision+1
    try:
        execute(connection,'''INSERT INTO evaluation_case_reviews
            (staff_user_id,packet_version,case_id,revision,decision,annotation)
            VALUES(:owner,:version,:case,:rev,:decision,:annotation)''',**params,rev=revision,decision=body.decision,
            annotation=annotation.model_dump_json() if annotation else None)
    except IntegrityError as err:
        if getattr(err.orig,'args',())[0]==1062:
            raise HTTPException(409,'This review changed. Reload to see the latest choice.') from err
        raise
    return dict(revision=revision,decision=body.decision,annotation=annotation.model_dump() if annotation else None)

