import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Gamepad2,
  UsersRound,
  Trophy,
  Target,
  ArrowRight,
  Sparkles,
  MoreHorizontal,
  Plus,
  Layers3,
  ListOrdered,
  ChevronRight,
} from '../components/icons'
import {
  Card,
  CardHeader,
  Badge,
  RoundLink,
  IconButton,
  FormatNumber,
  Avatar,
  Menu,
} from '../components/ui'
import { ActivityChart, LevelChart } from '../components/charts'
import LiveRound from '../components/LiveRound'
import PlayerList from '../components/PlayerList'
import { RegistrationQR } from '../components/Shell'
import { useApp } from '../state/AppContext'
import { rankPlayers } from '../data/demo'
import { CLASSIC_GAME, gameLabel } from '../state/game'

export default function Overview() {
  const { stats, rounds, queue, admissionsOpen, game = CLASSIC_GAME } = useApp()
  const [rankingSource, setRankingSource] = useState('simulator')
  const metrics = [
    {
      label: 'Games played',
      value: stats.games,
      detail: 'saved completed rounds',
      icon: Gamepad2,
      to: '/admin/sessions',
    },
    {
      label: 'Players on the board',
      value: stats.players,
      detail: 'unique players with results',
      icon: UsersRound,
      to: '/admin/sessions',
    },
    {
      label: 'Win rate',
      value: stats.winRate == null ? '—' : `${stats.winRate.toFixed(1)}%`,
      detail: `${stats.wins} wins out of ${stats.games} rounds`,
      icon: Trophy,
      to: '/admin/analytics',
    },
    {
      label: 'Placement accuracy',
      value: stats.accuracy == null ? '—' : `${stats.accuracy.toFixed(1)}%`,
      detail: 'pooled LED overlap ratio',
      icon: Target,
      to: '/admin/analytics',
    },
  ]
  return (
    <>
      <div className="overview-heading">
        <div>
          <span className="eyebrow">THE GAME IS ON</span>
          <h1>Let the good times stack.</h1>
          <p>Your carnival, one great round at a time.</p>
        </div>
        <RegistrationQR />
      </div>
      <div className="hero-grid">
        <div className="hero-left">
          <div className="welcome-row">
            <span className="welcome-symbol" aria-hidden="true">
              <Layers3 size={33} />
            </span>
            <div className="welcome-pill">
              <div>
                <strong>Hey, operator.</strong>
                <span>One cabinet. Endless possibilities.</span>
              </div>
              <i className="fa-solid fa-ellipsis-vertical welcome-dots" aria-hidden="true" />
            </div>
          </div>
          <Card className="overview-card">
            <CardHeader
              title="Carnival overview"
              subtitle="The numbers behind the fun"
              icon={Sparkles}
              action={<RoundLink to="/admin/analytics" label="Explore game analytics" />}
            />
            <div className="metric-rows">
              {metrics.map(({ label, value, detail, icon: Icon, to }) => (
                <Link className="metric-row" key={label} to={to}>
                  <span className="metric-row-icon">
                    <Icon size={26} strokeWidth={1.45} />
                  </span>
                  <div>
                    <strong>{label}</strong>
                    <span>{detail}</span>
                  </div>
                  <b>{value}</b>
                  <ChevronRight size={19} />
                </Link>
              ))}
            </div>
            <div className="overview-bottom">
              <span className="tiny-dot" />
              {gameLabel(game)} · {game.round_limit_ms / 1000} seconds · {game.levels} levels
              <span>Current rules · all saved sources</span>
            </div>
          </Card>
        </div>
        <div className="hero-right">
          <LiveRound />
        </div>
      </div>
      <div className="section-label">
        <span>BEHIND EVERY GREAT STACK</span>
        <Link to="/admin/analytics">
          Explore analytics
          <ArrowRight size={15} />
        </Link>
      </div>
      <div className="two-column">
        <ActivityChart rounds={rounds} />
        <LevelChart rounds={rounds} levels={game.levels} />
      </div>
      <div className="two-column lower-grid">
        <Card>
          <CardHeader
            title="The high stack"
            subtitle="Best saved round per player · selected source"
            icon={Trophy}
            action={
              <Menu
                label="Leaderboard result source"
                value={rankingSource === 'simulator' ? 'Simulator' : 'Game screen / cabinet'}
                options={[
                  { value: 'simulator', label: 'Simulator' },
                  { value: 'device', label: 'Game screen / cabinet' },
                ]}
                onChange={setRankingSource}
              />
            }
          />
          <PlayerList
            compact
            players={rankPlayers(rounds.filter((round) => round.source === rankingSource)).slice(
              0,
              4,
            )}
          />
          {!rounds.some((round) => round.source === rankingSource) && (
            <p className="subtle">No saved results for this source.</p>
          )}
          <Link className="card-bottom-link" to="/admin/sessions">
            View saved round history
            <ArrowRight size={17} />
          </Link>
        </Card>
        <Card>
          <CardHeader
            title="Up next"
            subtitle={`${queue.length} players waiting for their moment`}
            icon={ListOrdered}
            action={
              <Badge tone={admissionsOpen ? 'lime' : 'neutral'} dot>
                {admissionsOpen ? 'Queue open' : 'Paused'}
              </Badge>
            }
          />
          <div className="queue-preview">
            {queue.slice(0, 4).map((p, i) => (
              <div className="queue-preview-row" key={p.id}>
                <span className="queue-number">{String(i + 1).padStart(2, '0')}</span>
                <Avatar name={p.nickname} index={i} />
                <div className="player-info">
                  <strong>{p.nickname}</strong>
                  <span>{p.code}</span>
                </div>
                <span className="queue-wait">{i === 0 ? 'Next in line' : 'Waiting'}</span>
              </div>
            ))}
            {!queue.length && (
              <p className="subtle">No one waiting. A good time for a fresh challenger.</p>
            )}
          </div>
          <Link className="card-bottom-link" to="/admin/queue">
            Manage the queue
            <ArrowRight size={17} />
          </Link>
        </Card>
      </div>
    </>
  )
}
