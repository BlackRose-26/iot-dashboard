import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import {
  MATRIX_RULES,
  MATRIX_RULES_HASH,
  createRound,
  playPresses,
  positionAt,
  press,
  toResult,
} from './engine'

const vectors = JSON.parse(
  readFileSync(resolve(process.cwd(), '../contracts/matrix-v1.vectors.json'), 'utf-8'),
)

describe('Matrix v1 engine', () => {
  it('uses the server rules and hash', () => {
    expect(MATRIX_RULES).toEqual(vectors.rules)
    expect(MATRIX_RULES_HASH).toBe(vectors.rulesHash)
  })

  it.each(vectors.vectors.map((v) => [v.name, v]))('matches the server trace: %s', (_, vector) => {
    const round = playPresses(vector.presses)
    const result = toResult(round, '00000000-0000-4000-8000-000000000000')
    expect(result.outcome).toBe(vector.expected.outcome)
    expect(result.durationMs).toBe(vector.expected.durationMs)
    expect(result.placements).toEqual(vector.expected.placements)
    expect(round.score).toBe(vector.expected.score)
  })

  it('bounces the row between the edges', () => {
    const round = createRound()
    expect(positionAt(round, 0)).toBe(0)
    expect(positionAt(round, 60 * 10)).toBe(10)
    expect(positionAt(round, 60 * 11)).toBe(9)
    expect(positionAt(round, 60 * 20)).toBe(0)
  })

  it('refuses a result before the round ends', () => {
    const round = createRound()
    press(round, 400)
    expect(() => toResult(round, 'x')).toThrow()
  })
})
