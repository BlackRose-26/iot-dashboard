"""Proposed typed dialogue state. No metrics, identities, SQL or tool execution."""
from typing import Literal

from pydantic import BaseModel, ConfigDict,Field

from app.assistant import Context


class Frame(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    mode: Literal['analytics','knowledge','social','unsupported','clarify']
    domain: Literal['event','players','queue','cabinet','scores','levels','trend','metric','gameplay','registration','queue_flow','architecture','dashboard','privacy','offline','results','assistant','memory','training','knowledge','definition'] | None=None
    operation: str | None=None
    dialogue_act: Literal['request','follow_up','social']='request'
    period: Literal['event_to_date','today','yesterday','last_7_days']='event_to_date'
    source: Literal['all','simulator','device']='all'
    level: int | None=Field(default=None,ge=1,le=12)
    limit: int=Field(default=5,ge=1,le=10)
    score_page: int=Field(default=1,ge=1,le=2000)


def frame(label,safe,previous=None):
    previous=Context.model_validate(previous) if previous else None
    topic,_,subtype=label.partition(':')
    if topic=='unsupported': return Frame(mode='unsupported')
    if topic=='social': return Frame(mode='social',operation=subtype,dialogue_act='social')
    if topic=='follow_up':
        if previous is None: return Frame(mode='clarify',dialogue_act='follow_up')
        tools=previous.tools
        domain=('knowledge' if previous.knowledge else 'definition' if previous.definition else
                'scores' if set(tools)&{'get_player_scores','get_top_scores','get_score_distribution'} else
                'queue' if 'get_queue_summary' in tools else 'cabinet' if 'get_machine_summary' in tools else
                'levels' if 'get_level_statistics' in tools else 'trend' if 'get_play_trend' in tools else 'players')
        result=Frame(mode='knowledge' if previous.knowledge or previous.definition else 'analytics',
                     domain=domain,operation=previous.knowledge or previous.definition or 'continue',
                     dialogue_act='follow_up',period=previous.period,source=previous.source,
                     level=previous.level,limit=previous.limit,score_page=previous.score_page)
        if {'next','page'}<=set(safe['safe_tokens']): result.score_page=min(2000,result.score_page+1)
    elif topic in {'knowledge','definition'}:
        result=Frame(mode='knowledge',domain='metric' if topic=='definition' else subtype,operation=subtype if topic=='definition' else 'explain')
    else:
        domain={'machine':'cabinet','top':'scores','overview':'event'}.get(topic,topic)
        words=set(safe['safe_tokens'])
        operation='ranking' if topic=='top' else next((term for term in ('total','average','highest','lowest','distribution') if term in words),'list' if topic=='scores' else 'summary')
        result=Frame(mode='analytics',domain=domain,operation=operation)
    # A new explicit domain never inherits an old domain/window. Only a labelled
    # follow-up merges existing state; all updates are validated enumerations.
    if safe['requested_period']: result.period=safe['requested_period']
    if safe['requested_source']: result.source=safe['requested_source']
    if safe['level_number'] is not None: result.level=safe['level_number']
    if safe['top_number'] is not None: result.limit=safe['top_number']
    return result
