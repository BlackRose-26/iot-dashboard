// Matrix v1 stacking engine for the web game screen.
// An exact port of firmware/stack_moko_baby/game_engine.h: the backend replays
// every placement (backend/app/game.py replay()), so any change here must keep
// contracts/matrix-v1.vectors.json passing in both test suites.

export const MATRIX_RULES = Object.freeze({
  code: 'matrix-v1',
  columns: 16,
  levels: 15,
  initial_width: 6,
  foundation_x: 5,
  round_limit_ms: 60000,
  base_step_ms: 60,
  step_decrease_ms: 10,
  minimum_step_ms: 50,
  row_points: 1,
  perfect_bonus: 0,
})

// sha256 of the canonical (sorted-key, compact) rules JSON; matches the server.
export const MATRIX_RULES_HASH = 'f73ce2ee4d1f607b6ea97038a534c7521a9305ee9ada3e2d418029cf866a58a4'

export const COUNTDOWN_STEP_MS = 500
export const COUNTDOWN_MS = 3 * COUNTDOWN_STEP_MS
export const MIN_GAP_MS = 30

export function createRound(rules = MATRIX_RULES) {
  return {
    rules,
    support: rules.foundation_x,
    width: rules.initial_width,
    count: 0,
    score: 0,
    lastLock: 0,
    duration: 0,
    ended: false,
    won: false,
    trace: [],
  }
}

export function stepInterval(round) {
  const { base_step_ms, step_decrease_ms, minimum_step_ms } = round.rules
  return Math.max(minimum_step_ms, base_step_ms - step_decrease_ms * round.count)
}

// Column of the moving row's left edge at `elapsed` ms after play started.
export function positionAt(round, elapsed) {
  const span = round.rules.columns - round.width
  const steps = Math.floor(Math.max(0, elapsed - round.lastLock) / stepInterval(round))
  const phase = steps % (2 * span)
  return phase <= span ? phase : 2 * span - phase
}

export function timeout(round) {
  round.ended = true
  round.duration = round.rules.round_limit_ms
  return round
}

// Lock the moving row. Returns true when the press placed a row.
export function press(round, elapsed) {
  elapsed = Math.floor(elapsed)
  if (round.ended) return false
  if (elapsed >= round.rules.round_limit_ms) {
    timeout(round)
    return false
  }
  if (elapsed - round.lastLock < MIN_GAP_MS) return false
  const pos = positionAt(round, elapsed)
  const left = Math.max(pos, round.support)
  const right = Math.min(pos + round.width, round.support + round.width)
  const overlap = Math.max(0, right - left)
  round.trace.push({ x: pos, width: round.width, overlap, locked: elapsed, support: round.support })
  round.count += 1
  round.lastLock = elapsed
  if (!overlap) {
    round.ended = true
    round.duration = elapsed
  } else {
    round.score += 1
    round.support = left
    round.width = overlap
    if (round.score === round.rules.levels) {
      round.won = true
      round.ended = true
      round.duration = elapsed
    }
  }
  return true
}

// The terminal payload the device journal sends (device_protocol.Result).
export function toResult(round, terminalId, rulesHash = MATRIX_RULES_HASH) {
  if (!round.ended) throw new Error('The round has not ended.')
  return {
    terminalId,
    rulesHash,
    outcome: round.won ? 'win' : 'loss',
    durationMs: round.duration,
    placements: round.trace.map((p) => ({
      candidate_x: p.x,
      candidate_width: p.width,
      overlap_width: p.overlap,
      locked_at_ms: p.locked,
    })),
  }
}

// Plays a list of press times (ms after play started) to the end of the round.
export function playPresses(times, rules = MATRIX_RULES) {
  const round = createRound(rules)
  for (const t of times) {
    if (round.ended) break
    press(round, t)
  }
  if (!round.ended) timeout(round)
  return round
}
