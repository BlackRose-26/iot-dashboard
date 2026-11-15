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
} from '../components/ui'
import { ActivityChart, LevelChart } from '../components/charts'
import LiveRound from '../components/LiveRound'
import PlayerList from '../components/PlayerList'
import { RegistrationQR } from '../components/Shell'
import { useApp } from '../state/AppContext'
import { rankPlayers } from '../data/demo'

export default function Overview() {
  const { stats, rounds, queue, admissionsOpen } = useApp()
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
              Classic v1 · 60 seconds · 12 levels<span>All saved sources</span>
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
        <LevelChart rounds={rounds} />
      </div>
      <div className="two-column lower-grid">
        <Card>
          <CardHeader
            title="The high stack"
            subtitle="Today’s best round per player"
            icon={Trophy}
            action={<RoundLink to="/admin/sessions" label="View full leaderboard" />}
          />
          <PlayerList compact players={rankPlayers(rounds).slice(0, 4)} />
          <Link className="card-bottom-link" to="/admin/sessions">
            Meet the whole leaderboard
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
