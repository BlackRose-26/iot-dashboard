import {
  ArrowUpRight,
  Timer,
  Zap,
  Layers3,
  WifiOff,
  CheckCircle2,
  LoaderCircle,
  UserRound,
  Plus,
  MoreHorizontal,
} from './icons'
import { Link } from 'react-router-dom'
import { useApp } from '../state/AppContext'
import { Card, CardHeader, Badge, Menu, Button } from './ui'
import { CLASSIC_GAME, gameLabel } from '../state/game'

export const stateLabels = {
  playing: 'Playing',
  ready: 'Ready',
  offline: 'Offline',
  pending: 'Result pending',
  review: 'Review required',
  reserved: 'Player called',
}
export function Matrix({ large = false, level = 7, columns = 8, levels = 12 }) {
  const cells = []
  const left = Math.floor(columns / 3)
  for (let row = levels - 1; row >= 0; row--)
    for (let col = 0; col < columns; col++) {
      const filled = row < level && col >= left && col < columns - left - Math.floor(row / 5)
      cells.push(
        <span
          key={`${row}-${col}`}
          className={filled ? (row === level - 1 ? 'lit active' : 'lit') : ''}
        />,
      )
    }
  return (
    <div
      className={`matrix ${large ? 'large' : ''}`}
      style={{
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gridTemplateRows: `repeat(${levels}, 1fr)`,
      }}
      aria-label={`Illustration of ${level} stacked rows`}
      role="img"
    >
      {cells}
    </div>
  )
}
export function Gauge({ state = 'offline' }) {
  return (
    <div className="gauge inactive" role="img" aria-label={stateLabels[state]}>
      <svg viewBox="0 0 440 240" aria-hidden="true">
        {Array.from({ length: 49 }, (_, i) => {
          const angle = Math.PI - (i / 48) * Math.PI
          const point = (r) => [220 + Math.cos(angle) * r, 218 - Math.sin(angle) * r]
          const [x1, y1] = point(i % 4 === 0 ? 155 : 169)
          const [x2, y2] = point(194)
          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke="#dce0e1"
              strokeWidth={i % 4 === 0 ? 2.5 : 2}
            />
          )
        })}
        {[0, 15, 30, 45, 60].map((n, i) => {
          const a = Math.PI - (i / 4) * Math.PI
          return (
            <text
              key={n}
              x={220 + Math.cos(a) * 132}
              y={220 - Math.sin(a) * 132}
              textAnchor="middle"
              fill="#777c80"
              fontSize="10"
            >
              {n}
            </text>
          )
        })}
      </svg>
      <div className="gauge-value">
        <>
          <span className="gauge-state-icon">
            {state === 'offline' ? (
              <WifiOff size={34} />
            ) : ['pending', 'review'].includes(state) ? (
              <LoaderCircle size={34} />
            ) : (
              <CheckCircle2 size={34} />
            )}
          </span>
          <strong className="state-value">{stateLabels[state]}</strong>
          <span>
            {state === 'playing'
              ? 'Timing runs on the cabinet'
              : state === 'ready'
                ? 'Ready for the next stack'
                : state === 'reserved'
                  ? 'Press the cabinet button'
                  : state === 'review'
                    ? 'The operator is checking this round'
                    : state === 'pending'
                      ? 'Waiting for score acknowledgment'
                      : 'Waiting for a fresh heartbeat'}
          </span>
        </>
      </div>
    </div>
  )
}
export default function LiveRound() {
  const {
    machineState,
    currentPlayer,
    queue,
    admissionsOpen,
    callNext,
    game = CLASSIC_GAME,
  } = useApp()
  const isPlaying = machineState === 'playing'
  const isReady = machineState === 'ready'
  const blockedReason = !admissionsOpen
    ? 'Admissions paused'
    : machineState === 'offline'
      ? 'Machine offline'
      : machineState === 'review'
        ? 'Operator review required'
        : machineState === 'pending'
          ? 'Result pending'
          : !isReady
            ? 'Round in progress'
            : !queue.length
              ? 'Queue empty'
              : ''
  return (
    <>
      <Card className="live-card">
        <CardHeader
          title="On the stack"
          subtitle="Cabinet 01 · server state"
          icon={Zap}
          action={
            <Badge tone={machineState === 'offline' ? 'danger' : 'soft'} dot>
              {stateLabels[machineState]}
            </Badge>
          }
        />
        <div className="round-badges">
          <Badge tone="blue">
            <Timer size={13} />
            60s round
          </Badge>
          <span>{gameLabel(game)}</span>
        </div>
        <Gauge state={machineState} />
        <div className="live-bottom">
          <div className="live-player">
            <span className="player-icon">
              <UserRound size={18} />
            </span>
            <div>
              <strong>
                {isPlaying || machineState === 'reserved'
                  ? currentPlayer?.nickname
                  : 'Your next challenger'}
              </strong>
              <span>
                {isPlaying || machineState === 'reserved'
                  ? currentPlayer?.code
                  : `One button. ${game.levels} levels.`}
              </span>
            </div>
          </div>
          <div className="level-label">
            <strong>
              —<span> / {game.levels}</span>
            </strong>
            <span>level completed</span>
          </div>
        </div>
        <div className="level-track" aria-hidden="true">
          {Array.from({ length: game.levels }, (_, i) => (
            <i key={i} className="" />
          ))}
        </div>
      </Card>
      <div className="operations-tray">
        <div className="operation-tiles">
          <button
            className="operation-tile blue"
            onClick={callNext}
            disabled={Boolean(blockedReason)}
            aria-describedby="call-next-reason"
          >
            <span className="tile-top">
              <span className="tile-icon">
                <ArrowUpRight size={24} />
              </span>
              <MoreHorizontal size={20} />
            </span>
            <strong>Call next player</strong>
            <span id="call-next-reason">
              {blockedReason || `${queue[0]?.nickname} is next in line`}
            </span>
          </button>
          <Link className="operation-tile white" to="/admin/sessions">
            <span className="tile-top">
              <span className="tile-icon lime">
                <Layers3 size={23} />
              </span>
              <ArrowUpRight size={20} />
            </span>
            <strong>The high stack</strong>
            <span>View saved results</span>
          </Link>
        </div>
        <div className="tray-footer">
          <span className="tray-plus">
            <Plus size={15} />
          </span>
          <div>
            <strong>{queue.length} players in the queue</strong>
            <span>Every great stack starts somewhere.</span>
          </div>
          <Link className="black-pill" to="/admin/queue">
            View queue
          </Link>
        </div>
      </div>
    </>
  )
}
