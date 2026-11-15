// Synthetic, reproducible fixtures. These are never hardware or database readings.
const names = [
  'Mika',
  'Anton',
  'Kyla',
  'Paolo',
  'Bea',
  'Enzo',
  'Jules',
  'Thea',
  'Nico',
  'Sam',
  'Dani',
  'Luis',
]
export const EVENT = {
  name: 'ACS Carnival',
  code: 'acs-day',
  machine: 'cabinet-01',
  date: '15 November 2026',
  timezone: 'Asia/Manila',
  ruleset: 'Classic v1',
}
export const players = Array.from({ length: 96 }, (_, i) => ({
  code: `SMB-${String(i + 1).padStart(3, '0')}`,
  nickname: `${names[i % names.length]}${i >= names.length ? ` ${String.fromCharCode(65 + Math.floor(i / names.length))}.` : ''}`,
}))
export const rounds = Array.from({ length: 148 }, (_, i) => {
  const won = i % 4 === 0 && i < 144
  const timedOut = !won && i % 5 === 0
  const level = won ? 12 : 2 + ((i * 7) % 10)
  let width = 3
  const placements = []
  for (let l = 1; l <= level; l++) {
    const overlap = l === 4 && i % 3 === 0 ? Math.max(1, width - 1) : width
    placements.push({ level: l, width, overlap })
    width = overlap
  }
  if (!won && !timedOut) placements.push({ level: level + 1, width, overlap: 0 })
  const perfect = placements.filter((p) => p.overlap > 0 && p.overlap === p.width).length
  const totalWidth = placements.reduce((sum, p) => sum + p.width, 0)
  const overlap = placements.reduce((sum, p) => sum + p.overlap, 0)
  return {
    id: `ROUND-${String(i + 1).padStart(4, '0')}`,
    ...players[i % players.length],
    won,
    reason: won ? 'Target reached' : timedOut ? 'Time expired' : 'No overlap',
    score: level * 100 + perfect * 25,
    level,
    perfect,
    placements,
    overlap,
    totalWidth,
    accuracy: totalWidth ? (100 * overlap) / totalWidth : null,
    duration: won ? 24 + (i % 25) : timedOut ? 60 : 12 + ((i * 13) % 42),
    hour: 9 + Math.floor(i / 22),
    minute: (i * 7) % 60,
    completedAt: new Date(Date.UTC(2026, 10, 15, 1, 0) + i * 165000).toISOString(),
  }
})
export const initialQueue = [
  players[23],
  players[37],
  players[52],
  players[68],
  players[71],
  players[89],
].map((p, i) => ({
  ...p,
  id: `ticket-${i}`,
  joinedAt: `14:${String(22 + i * 2).padStart(2, '0')}`,
  status: 'Waiting',
}))
export const activity = Array.from({ length: 7 }, (_, i) => ({
  label: `${i + 9}:00`,
  games: rounds.filter((r) => r.hour === i + 9).length,
  wins: rounds.filter((r) => r.hour === i + 9 && r.won).length,
}))
export function summarize(data) {
  const wins = data.filter((r) => r.won).length
  const width = data.reduce((n, r) => n + r.totalWidth, 0)
  return {
    games: data.length,
    players: new Set(data.map((r) => r.code)).size,
    wins,
    losses: data.length - wins,
    timeouts: data.filter((r) => r.reason === 'Time expired').length,
    winRate: data.length ? (wins / data.length) * 100 : null,
    duration: data.length ? data.reduce((n, r) => n + r.duration, 0) / data.length : null,
    accuracy: width ? (data.reduce((n, r) => n + r.overlap, 0) / width) * 100 : null,
  }
}
export function rankPlayers(data) {
  const order = (a, b) =>
    b.score - a.score ||
    b.level - a.level ||
    a.duration - b.duration ||
    a.completedAt.localeCompare(b.completedAt) ||
    a.id.localeCompare(b.id)
  const best = new Map()
  data.forEach((r) => {
    if (!best.has(r.code) || order(r, best.get(r.code)) < 0) best.set(r.code, r)
  })
  return [...best.values()].sort(order).map((r, i) => ({ ...r, rank: i + 1 }))
}
export function levelStatistics(data) {
  return Array.from({ length: 12 }, (_, i) => {
    const attempts = data.flatMap((r) => r.placements).filter((p) => p.level === i + 1)
    const failures = attempts.filter((p) => p.overlap === 0).length
    return {
      level: String(i + 1),
      attempts: attempts.length,
      failures,
      rate: attempts.length ? Math.round((failures / attempts.length) * 1000) / 10 : 0,
    }
  })
}
export const scoreBuckets = (data) =>
  Array.from({ length: 5 }, (_, i) => ({
    label: `${i * 300}–${i === 4 ? '1,500' : (i + 1) * 300 - 1}`,
    rounds: data.filter(
      (r) => r.score >= i * 300 && (i === 4 ? r.score <= 1500 : r.score < (i + 1) * 300),
    ).length,
  }))
export function validateRegistration({ nickname, studentId, acknowledged }) {
  const errors = {}
  if ([...nickname.trim()].length < 2 || [...nickname.trim()].length > 24)
    errors.nickname = 'Use a nickname between 2 and 24 characters.'
  if (!/^[A-Za-z0-9-]{4,32}$/.test(studentId.trim()))
    errors.studentId = 'Use 4–32 letters, numbers or hyphens. Keep any leading zeros.'
  if (!acknowledged) errors.acknowledged = 'Please acknowledge the privacy notice to continue.'
  return errors
}
