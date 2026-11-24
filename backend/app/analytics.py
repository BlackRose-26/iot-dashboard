"""Bounded, read-only event analytics. No identity columns or model-generated SQL."""
from datetime import datetime, timedelta
from decimal import Decimal
import json
from typing import Literal
import uuid

from fastapi import HTTPException
from sqlalchemy import text

from .security import now
from .machine_status import cabinet_state
from .game import active_rules

Period = Literal['today', 'yesterday', 'last_7_days', 'event_to_date']
Source = Literal['simulator', 'device']
ChatSource = Literal['all', 'simulator', 'device']
PERIOD_LABELS = {'today': 'Today', 'yesterday': 'Yesterday', 'last_7_days': 'Last seven days', 'event_to_date': 'Event to date'}
TOOL_KEYS = {
    'get_event_summary': 'summary', 'get_queue_summary': 'queue',
    'get_machine_summary': 'machine', 'get_top_scores': 'top',
    'get_level_statistics': 'levels', 'get_play_trend': 'trend',
    'get_score_distribution': 'scores',
    'get_player_scores': 'player_scores',
}
RESULTS = """ FROM game_sessions g WHERE g.event_id=:event AND g.ruleset_id=:rules
 AND g.status='completed' AND g.invalidated_at IS NULL AND g.result_source=:source
 AND g.completed_at>=:start AND g.completed_at<:end """


def stamp(value):
    return value.isoformat(timespec='milliseconds') + 'Z' if value else None


def clean(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return stamp(value)
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def select(c, sql, params):
    # MariaDB per-statement limit, without altering pooled session defaults.
    return [dict(r) for r in c.execute(text('SET STATEMENT max_statement_time=2 FOR ' + sql), params).mappings()]


def _operations(period, tools):
    if period not in PERIOD_LABELS:
        raise HTTPException(422, 'Unsupported analytics filters.')
    requested = list(dict.fromkeys(tools if tools is not None else [name for name in TOOL_KEYS if name!='get_player_scores']))
    if any(tool not in TOOL_KEYS for tool in requested):
        raise HTTPException(422, 'Unsupported analytics operation.')
    return requested


def collect(engine, period: Period = 'event_to_date', source: Source = 'simulator', tools=None, simulator_enabled=True, score_page=1):
    if source not in ('device','simulator'):
        raise HTTPException(422, 'Unsupported analytics filters.')
    requested = _operations(period, tools)
    with engine.connect().execution_options(isolation_level='REPEATABLE READ') as c:
        c.exec_driver_sql('SET TRANSACTION READ ONLY')
        return _collect_snapshot(c, period, source, requested, simulator_enabled, now(), str(uuid.uuid4()), score_page)


def collect_all(engine, period: Period = 'event_to_date', tools=None, simulator_enabled=True, score_page=1):
    requested = _operations(period, tools)
    current = {'get_queue_summary','get_machine_summary'}
    result_tools = [tool for tool in requested if tool not in current]
    as_of, snapshot = now(), str(uuid.uuid4())
    with engine.connect().execution_options(isolation_level='REPEATABLE READ') as c:
        c.exec_driver_sql('SET TRANSACTION READ ONLY')
        simulator = _collect_snapshot(c, period, 'simulator', requested, simulator_enabled, as_of, snapshot+'.simulator',score_page)
        scope = dict(simulator['scope'], source='all')
        bundle = {'snapshot_id':snapshot,'as_of':simulator['as_of'],'scope':scope,
                  'scope_label':f"ACS Carnival · {scope['ruleset']} · {PERIOD_LABELS[period]} · All available result sources",
                  'tools':requested,'shared':{key:simulator[key] for key in ('queue','machine') if key in simulator},
                  'cohorts':{},'caveats':list(simulator['caveats'])}
        if result_tools:
            device = _collect_snapshot(c, period, 'device', result_tools, simulator_enabled, as_of, snapshot+'.device',score_page)
            for source, data in (('simulator',simulator),('device',device)):
                data['tools'] = result_tools
                for key in ('queue','machine'): data.pop(key,None)
                bundle['cohorts'][source] = data
            bundle['caveats'].extend(device['caveats'])
        if 'get_event_summary' in requested:
            params={'event':None,'rules':None,'start':None,'end':None}
            # The same fixed event/rules and half-open window used by both cohorts.
            event=select(c,"SELECT id FROM events WHERE code='acs-day'",{})[0]
            rules,_=active_rules(c)
            params.update(event=event['id'],rules=rules['id'],start=datetime.fromisoformat(scope['start'].removesuffix('Z')),
                          end=datetime.fromisoformat(scope['end'].removesuffix('Z')))
            all_results=RESULTS.replace('g.result_source=:source',"g.result_source IN ('simulator','device')")
            counts=select(c,'SELECT COUNT(*) AS completed_games,COUNT(DISTINCT g.player_id) AS completed_players'+all_results,params)[0]
            counts['registrations']=simulator['summary']['registrations']
            bundle['global_counts']=counts
        bundle['caveats'].append('All sources were checked in one read-only snapshot. Dashboard-simulator and device-protocol competitive metrics stay separate. Device-protocol rounds come from the web game screen (the default) or the LED cabinet, plus earlier Wokwi tests.')
        bundle['caveats']=list(dict.fromkeys(bundle['caveats']))
        return clean(bundle)


def _collect_snapshot(c, period, source, requested, simulator_enabled, as_of, snapshot_id, score_page=1):
    event_rows = select(c, "SELECT id,name,timezone,created_at,starts_at,status FROM events WHERE code='acs-day'", {})
    if not event_rows:
        raise HTTPException(503, 'Event analytics configuration is unavailable.')
    event = event_rows[0]
    rules, config = active_rules(c)
    if event['timezone'] != 'Asia/Manila':
        raise HTTPException(503, 'This release supports the Asia/Manila event timezone.')
    today = (as_of + timedelta(hours=8)).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=8)
    start, end = min(event['created_at'], event['starts_at'], as_of - timedelta(milliseconds=1)), as_of
    if period == 'today': start = today
    elif period == 'yesterday': start, end = today - timedelta(days=1), today
    elif period == 'last_7_days': start = today - timedelta(days=6)
    # Public evidence and every cohort use the same millisecond window bounds.
    start = start.replace(microsecond=start.microsecond//1000*1000)
    end = end.replace(microsecond=end.microsecond//1000*1000)
    scope = {'event': 'acs-day', 'ruleset': rules['code'], 'timezone': 'Asia/Manila',
             'period': period, 'source': source, 'start': stamp(start), 'end': stamp(end)}
    params = {'event': event['id'], 'rules': rules['id'], 'source': source, 'start': start, 'end': end, 'as_of': as_of}
    data = {'snapshot_id': snapshot_id, 'as_of': stamp(as_of), 'scope': scope,
            'scope_label': f"ACS Carnival · {rules['code']} · {PERIOD_LABELS[period]} · {source} results",
            'game': config,
            'tools': requested, 'caveats': []}
    if 'get_event_summary' in requested:
        summary = select(c, """SELECT COUNT(*) AS completed_games,COUNT(DISTINCT g.player_id) AS completed_players,
          COALESCE(SUM(g.outcome='win'),0) AS wins,COALESCE(SUM(g.outcome='loss'),0) AS losses,
          COALESCE(SUM(g.end_reason='timeout'),0) AS timeouts,AVG(g.duration_ms)/1000 AS average_duration,
          AVG(g.score) AS average_score,MAX(g.score) AS highest_score,MIN(g.score) AS lowest_score,COALESCE(SUM(g.score),0) AS total_score,
          SUM(g.overlap_total) AS retained,SUM(g.attempted_width_total) AS attempted""" + RESULTS, params)[0]
        registrations = select(c, """SELECT COUNT(*) AS registrations FROM
          (SELECT player_id,MIN(joined_at) AS first_join FROM queue_entries WHERE event_id=:event GROUP BY player_id) r
          WHERE first_join>=:start AND first_join<:end""", params)[0]
        summary.update(registrations)
        summary['win_rate'] = round(100 * summary['wins'] / summary['completed_games'], 1) if summary['completed_games'] else None
        summary['accuracy'] = round(100 * summary['retained'] / summary['attempted'], 1) if summary['attempted'] else None
        data['summary'] = summary
        data['caveats'].append('Registrations count each player’s first event queue entry in the selected window, across sources. Completed-player counts use the selected result source.')
    if 'get_queue_summary' in requested:
        q = select(c, """SELECT COALESCE(SUM(status='waiting'),0) AS waiting,
          COALESCE(SUM(status='assigned'),0) AS assigned,
          MIN(CASE WHEN status='waiting' THEN joined_at END) AS oldest
          FROM queue_entries WHERE event_id=:event AND joined_at<:as_of""", params)[0]
        oldest = q.pop('oldest')
        q.update({'admissions': event['status'], 'oldest_wait_seconds': max(0, int((as_of-oldest).total_seconds())) if oldest else None})
        data['queue'] = q
        data['caveats'].append('Queue and cabinet status describe the current event, not the selected historical result window or source.')
    if 'get_machine_summary' in requested:
        machines = select(c, """SELECT m.observed_state,m.last_seen_at,m.health,m.enabled,m.maintenance,m.firmware_version,
          g.status AS active_status,g.result_source,g.ready_deadline_at
          FROM machines m LEFT JOIN game_sessions g ON g.active_machine_id=m.id
          WHERE m.event_id=:event AND m.code='cabinet-01'""", params)
        if not machines:
            data['machine'] = {'state': 'unknown', 'source': 'unknown', 'last_seen': None, 'age_seconds': None}
        else:
            m = machines[0]
            try: health = json.loads(m['health'] or '{}')
            except (ValueError, TypeError): health = {}
            if not isinstance(health, dict): health = {}
            origin = 'simulator' if health.get('source') == 'simulator' else 'device' if m['last_seen_at'] else 'unknown'
            age = max(0, int((as_of-m['last_seen_at']).total_seconds())) if m['last_seen_at'] else None
            game = {'status':m['active_status'],'result_source':m['result_source'],'ready_deadline_at':m['ready_deadline_at']} if m['active_status'] else None
            state = cabinet_state(m,game,as_of,simulator_enabled)
            data['machine'] = {'state': state, 'source': origin, 'last_seen': stamp(m['last_seen_at']),
                               'age_seconds': age, 'enabled': bool(m['enabled']), 'maintenance': bool(m['maintenance']),
                               'firmware': m['firmware_version'] if origin=='device' else None,
                               'rssi': health.get('rssi') if origin=='device' and type(health.get('rssi')) is int and -120<=health['rssi']<=0 else None}
            if origin == 'simulator': data['caveats'].append('Cabinet observations come from the development simulator, not a connected ESP32. The recorded timestamp is not a fresh physical heartbeat.')
    if 'get_score_distribution' in requested:
        maximum = config['levels']*(config['row_points']+config['perfect_bonus'])
        step = max(1, maximum//5)
        counts = select(c, """SELECT LEAST(FLOOR(g.score/:step),4) AS bucket,COUNT(*) AS rounds""" + RESULTS + ' GROUP BY bucket', dict(params,step=step))
        by_bucket = {int(r['bucket']): int(r['rounds']) for r in counts}
        data['scores'] = [{'label': f'{i*step}–{maximum if i==4 else (i+1)*step-1}', 'rounds': by_bucket.get(i, 0)} for i in range(5)]
    if 'get_level_statistics' in requested:
        rows = select(c, """SELECT p.level_no AS level,COUNT(*) AS attempts,
          SUM(p.overlap_width=0) AS failures,SUM(p.overlap_width) AS retained,SUM(p.candidate_width) AS attempted
          FROM placements p JOIN game_sessions g ON g.id=p.session_id""" + RESULTS.replace(' FROM game_sessions g', '') + ' GROUP BY p.level_no', params)
        levels = {int(r['level']): r for r in rows}
        data['levels'] = []
        for level in range(1, config['levels']+1):
            r = levels.get(level, {'level': level, 'attempts': 0, 'failures': 0, 'retained': 0, 'attempted': 0})
            r['rate'] = round(100*r['failures']/r['attempts'], 1) if r['attempts'] else None
            r['accuracy'] = round(100*r['retained']/r['attempted'], 1) if r['attempted'] else None
            data['levels'].append(r)
        data['caveats'].append('Level failures mean recorded zero-overlap placements; timeouts are separate. Fewer than 20 attempts is a small sample.')
    if 'get_player_scores' in requested:
        if type(score_page) is not int or not 1<=score_page<=2000:
            raise HTTPException(422,'Unsupported score page.')
        count=select(c,'SELECT COUNT(DISTINCT g.player_id) AS total'+RESULTS,params)[0]['total']
        rows=select(c,"""SELECT public_code,score,highest_level,duration_ms FROM
          (SELECT p.public_code,g.score,g.highest_level,g.duration_ms,
          ROW_NUMBER() OVER (PARTITION BY g.player_id ORDER BY g.score DESC,g.highest_level DESC,
          g.duration_ms,g.completed_at,g.public_id) AS best
          FROM players p JOIN game_sessions g ON g.player_id=p.id"""+RESULTS.replace(' FROM game_sessions g','')+""") ranked
          WHERE best=1 ORDER BY public_code LIMIT 50 OFFSET :offset""",dict(params,offset=(score_page-1)*50))
        data['player_scores']={'rows':rows,'total_players':count,'page':score_page,'page_size':50,
                               'has_more':score_page*50<count,'basis':'Each participant’s best valid completed score for this result source.'}
    if 'get_top_scores' in requested:
        data['top'] = select(c, """SELECT public_code,score,highest_level,duration_ms,completed_at FROM
          (SELECT p.public_code,g.score,g.highest_level,g.duration_ms,g.completed_at,g.public_id,
          ROW_NUMBER() OVER (PARTITION BY g.player_id ORDER BY g.score DESC,g.highest_level DESC,
          g.duration_ms,g.completed_at,g.public_id) AS best
          FROM players p JOIN game_sessions g ON g.player_id=p.id""" + RESULTS.replace(' FROM game_sessions g', '') + """) ranked
          WHERE best=1 ORDER BY score DESC,highest_level DESC,duration_ms,completed_at,public_id LIMIT 10""", params)
    if 'get_play_trend' in requested:
        hourly = (end.replace(minute=0,second=0,microsecond=0)-start.replace(minute=0,second=0,microsecond=0)).total_seconds() < 168*3600
        trend_start = max(start, end-timedelta(days=167)) if not hourly else start
        tp = dict(params, start=trend_start, fmt='%Y-%m-%d %H:00' if hourly else '%Y-%m-%d')
        rows = select(c, """SELECT DATE_FORMAT(DATE_ADD(g.completed_at,INTERVAL 8 HOUR),:fmt) AS label,
          COUNT(*) AS games,SUM(g.outcome='win') AS wins,COUNT(DISTINCT g.player_id) AS players""" + RESULTS + ' GROUP BY label ORDER BY label LIMIT 168', tp)
        lookup = {r['label']: r for r in rows}
        cursor = (trend_start+timedelta(hours=8)).replace(minute=0, second=0, microsecond=0)
        if not hourly: cursor = cursor.replace(hour=0)
        stop = end+timedelta(hours=8)
        buckets = []
        while cursor < stop and len(buckets) < 168:
            label = cursor.strftime(tp['fmt'])
            buckets.append(lookup.get(label, {'label': label, 'games': 0, 'wins': 0, 'players': 0}))
            cursor += timedelta(hours=1) if hourly else timedelta(days=1)
        data['trend'] = {'granularity': 'hour' if hourly else 'day', 'start': stamp(trend_start), 'end': stamp(end), 'buckets': buckets}
        if trend_start > start: data['caveats'].append('The trend is limited to the latest 168 daily buckets; summary totals still cover the full selected window.')
        data['caveats'].append('Distinct players in separate time buckets must not be summed to produce a window-wide unique-player count.')
    return clean(data)
