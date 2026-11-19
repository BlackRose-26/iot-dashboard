import { describe, it, expect } from 'vitest'
import { validateRegistration, summarize, rankPlayers, levelStatistics, rounds } from './demo'

describe('registration validation', () => {
  it('rejects nickname characters the registration API cannot accept', () => {
    expect(
      validateRegistration({ nickname: '<Player>', studentId: 'DUMMY-1', acknowledged: true }),
    ).toHaveProperty('nickname')
    expect(
      validateRegistration({ nickname: 'José_1', studentId: 'DUMMY-1', acknowledged: true }),
    ).toEqual({})
  })
  it('accepts IDs with leading zeros without numeric conversion', () => {
    expect(
      validateRegistration({ nickname: 'Player', studentId: '001234', acknowledged: true }),
    ).toEqual({})
  })
  it('rejects missing notice acknowledgment and invalid identifiers', () => {
    expect(
      validateRegistration({ nickname: ' ', studentId: '<script>', acknowledged: false }),
    ).toHaveProperty('nickname')
    expect(
      validateRegistration({ nickname: 'Player', studentId: '<script>', acknowledged: false }),
    ).toHaveProperty('studentId')
    expect(
      validateRegistration({ nickname: 'Player', studentId: 'DEMO-2026', acknowledged: false }),
    ).toHaveProperty('acknowledged')
  })
})
describe('dashboard metric definitions', () => {
  it('reports unattempted level ratios as unknown', () => {
    expect(levelStatistics([]).every((level) => level.rate === null)).toBe(true)
  })
  it('returns unknown ratios for an empty window', () => {
    expect(summarize([])).toMatchObject({
      games: 0,
      players: 0,
      wins: 0,
      winRate: null,
      duration: null,
      accuracy: null,
    })
  })
  it('uses pooled overlap instead of averaging per-game percentages', () => {
    const data = [
      { code: 'A', won: false, duration: 10, overlap: 1, totalWidth: 1 },
      { code: 'A', won: true, duration: 20, overlap: 0, totalWidth: 9 },
    ]
    expect(summarize(data)).toMatchObject({
      games: 2,
      players: 1,
      accuracy: 10,
      winRate: 50,
      duration: 15,
    })
  })
  it('ranks each player once and resolves ties by duration then completion time', () => {
    const data = [
      {
        id: '1',
        code: 'A',
        score: 500,
        level: 4,
        duration: 30,
        completedAt: '2026-11-15T01:00:00Z',
      },
      {
        id: '2',
        code: 'A',
        score: 600,
        level: 5,
        duration: 25,
        completedAt: '2026-11-15T02:00:00Z',
      },
      {
        id: '3',
        code: 'B',
        score: 600,
        level: 5,
        duration: 24,
        completedAt: '2026-11-15T03:00:00Z',
      },
    ]
    expect(rankPlayers(data).map((r) => r.code)).toEqual(['B', 'A'])
    expect(rankPlayers(data)[1].id).toBe('2')
  })
  it('does not invent failed placements for timeouts', () => {
    expect(
      levelStatistics([
        { placements: [{ level: 1, width: 3, overlap: 3 }], reason: 'Time expired' },
      ])[0],
    ).toMatchObject({ attempts: 1, failures: 0, rate: 0 })
  })
  it('keeps sample scores within the published scoring rules', () => {
    for (const round of rounds) {
      expect(round.score).toBe(round.level * 100 + round.perfect * 25)
      expect(round.score).toBeLessThanOrEqual(1500)
    }
  })
})
