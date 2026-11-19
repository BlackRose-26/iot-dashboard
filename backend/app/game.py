import hashlib
import json

RULES = {'code': 'classic-v1', 'columns': 8, 'levels': 12, 'initial_width': 3,
         'foundation_x': 2, 'round_limit_ms': 60000, 'base_step_ms': 350,
         'step_decrease_ms': 20, 'minimum_step_ms': 120, 'row_points': 100, 'perfect_bonus': 25}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


RULES_HASH = hashlib.sha256(canonical(RULES).encode()).digest()


def replay(placements, duration_ms, outcome):
    if not 0 <= duration_ms <= RULES['round_limit_ms']:
        raise ValueError('Invalid round duration.')
    support_x, width, last_time = 2, 3, 0
    successful, perfect, retained, attempted = 0, 0, 0, 0
    proof = []
    missed = False
    for index, placement in enumerate(placements):
        level = index + 1
        if missed or level > 12:
            raise ValueError('Placement after the round ended.')
        locked = placement['locked_at_ms']
        x = placement['candidate_x']
        interval = max(120, 350 - 20 * index)
        elapsed = locked - last_time
        if elapsed < 30 or locked >= 60000 or locked > duration_ms:
            raise ValueError('Invalid placement time.')
        steps = elapsed // interval
        span = 8 - width
        phase = steps % (2 * span)
        expected_x = phase if phase <= span else 2 * span - phase
        if x != expected_x or placement['candidate_width'] != width:
            raise ValueError('Placement does not match the row movement.')
        left, right = max(support_x, x), min(support_x + width, x + width)
        overlap = max(0, right - left)
        if placement['overlap_width'] != overlap:
            raise ValueError('Invalid overlap evidence.')
        proof.append({'level': level, 'x': x, 'width': width, 'support_x': support_x,
                      'support_width': width, 'overlap': overlap, 'locked': locked})
        attempted += width
        retained += overlap
        if overlap:
            successful += 1
            perfect += int(overlap == width)
            support_x, width = left, overlap
        else:
            missed = True
        last_time = locked
    expected_outcome = 'win' if successful == 12 else 'loss'
    if outcome != expected_outcome or (not missed and successful < 12 and duration_ms != 60000):
        raise ValueError('The outcome does not match the placement evidence.')
    if (missed or successful == RULES['levels']) and duration_ms != last_time:
        raise ValueError('Terminal duration must match the final placement time.')
    return {'score': 100 * successful + 25 * perfect, 'level': successful, 'perfect': perfect,
            'retained': retained, 'attempted': attempted, 'placements': proof,
            'reason': 'target_reached' if outcome == 'win' else 'zero_overlap' if missed else 'timeout'}


def simulated_result(outcome):
    import uuid
    placements, clock = [], 0
    count = 12 if outcome == 'win' else 4
    for index in range(count):
        miss = outcome == 'loss' and index == count - 1
        interval = max(120, 350 - 20 * index)
        clock += interval * (5 if miss else 2) + 5
        placements.append({'candidate_x': 5 if miss else 2, 'candidate_width': 3,
                           'overlap_width': 0 if miss else 3, 'locked_at_ms': clock})
    return {'terminalId': str(uuid.uuid4()), 'outcome': outcome, 'durationMs': clock,
            'rulesHash': RULES_HASH.hex(), 'placements': placements}
