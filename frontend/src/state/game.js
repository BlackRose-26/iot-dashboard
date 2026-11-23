export const CLASSIC_GAME = {
  code: 'classic-v1',
  columns: 8,
  levels: 12,
  row_points: 100,
  perfect_bonus: 25,
  round_limit_ms: 60000,
}
export const gameLabel = (game = CLASSIC_GAME) =>
  game.code === 'matrix-v1' ? 'Matrix v1' : 'Classic v1'
