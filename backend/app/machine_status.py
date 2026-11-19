"""One cabinet-state definition shared by dashboard, queue and read-only AI analytics."""
import json


def health_data(machine):
    try:
        value = json.loads(machine['health'] or '{}')
        return value if isinstance(value,dict) else {}
    except (ValueError,TypeError):
        return {}


def cabinet_state(machine, game, at, simulator_enabled):
    if not machine['enabled'] or machine['maintenance']:
        return 'offline'
    if game and (game['status']=='review' or (game.get('result_source')=='device'
            and game['status']=='reserved' and game.get('ready_deadline_at')
            and game['ready_deadline_at']<=at)):
        return 'review'
    if health_data(machine).get('source')=='simulator':
        fresh = simulator_enabled
    else:
        age = (at-machine['last_seen_at']).total_seconds() if machine['last_seen_at'] else None
        fresh = age is not None and 0<=age<15
    if not fresh: return 'offline'
    return {'reserved':'reserved','countdown':'reserved','playing':'playing',
            'awaiting_result':'pending'}.get(game['status'] if game else '',
                'ready' if machine['observed_state']=='ready' else 'offline')
