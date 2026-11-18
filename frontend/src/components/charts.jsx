import { useId } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import { Clock3, TrendingUp, Layers3, Target } from './icons'
import { Card, CardHeader, Badge } from './ui'
import { levelStatistics, scoreBuckets, summarize } from '../data/demo'

const axis = {
  axisLine: false,
  tickLine: false,
  tick: { fill: '#60696d', fontSize: 11 },
  tickMargin: 10,
}
function ChartTip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <strong>{label}</strong>
      {payload.map((p) => (
        <span key={p.dataKey}>
          <i style={{ background: p.color }} />
          {p.name}:{' '}
          <b>
            {p.value}
            {p.dataKey === 'rate' ? '%' : ''}
          </b>
        </span>
      ))}
      {payload[0]?.payload?.attempts != null && (
        <small>
          {payload[0].payload.attempts} attempts · {payload[0].payload.failures} misses
        </small>
      )}
    </div>
  )
}
export function ActivityChart({ data, rounds = [], large = false, granularity = 'hour' }) {
  data =
    data ||
    Array.from({ length: 24 }, (_, hour) => ({
      label: `${hour}:00`,
      games: rounds.filter((r) => r.hour === hour).length,
      wins: rounds.filter((r) => r.hour === hour && r.won).length,
    }))
  const id = useId().replaceAll(':', '')
  const games = data.reduce((n, d) => n + d.games, 0)
  return (
    <Card className={`chart-card ${large ? 'span-2' : ''}`}>
      <CardHeader
        title="A good day to stack"
        subtitle="Completed games in the selected window"
        icon={TrendingUp}
        action={<Badge>{granularity === 'day' ? 'Daily' : 'Hourly'}</Badge>}
      />
      <div className="chart-summary">
        <strong>
          {games}
          <span> games</span>
        </strong>
        <span className="chart-legend">
          <i className="blue-dot" />
          All rounds
          <i className="black-dot" />
          Wins
        </span>
      </div>
      <div
        className="chart-frame"
        role="img"
        aria-label={`${games} completed games by ${granularity}. ${data.map((d) => `${d.label}: ${d.games} games and ${d.wins} wins`).join('; ')}`}
      >
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 15, right: 10, bottom: 5, left: -27 }}>
            <defs>
              <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#96b6ff" stopOpacity={0.42} />
                <stop offset="100%" stopColor="#96b6ff" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} stroke="#ededed" strokeDasharray="3 5" />
            <XAxis dataKey="label" {...axis} />
            <YAxis allowDecimals={false} {...axis} />
            <Tooltip content={<ChartTip />} />
            <Area
              dataKey="games"
              name="Games"
              type="monotone"
              stroke="#7d9ee9"
              strokeWidth={3}
              fill={`url(#${id})`}
              isAnimationActive={false}
            />
            <Area
              dataKey="wins"
              name="Wins"
              type="monotone"
              stroke="#151616"
              strokeWidth={2}
              fill="transparent"
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <p className="chart-footnote">Asia/Manila · valid completed rounds only</p>
    </Card>
  )
}
export function LevelChart({ rounds = [], large = false, data: suppliedData }) {
  const data = suppliedData || levelStatistics(rounds)
  const hardest = [...data].filter((d) => d.attempts >= 20).sort((a, b) => b.rate - a.rate)[0]
  return (
    <Card className={`chart-card ${large ? 'span-2' : ''}`}>
      <CardHeader
        title="Where the stack slips"
        subtitle="Zero-overlap failure rate by attempted level"
        icon={Layers3}
        action={<Badge>12 levels</Badge>}
      />
      <div className="chart-summary">
        <strong>
          {hardest ? `Level ${hardest.level}` : 'Not enough data'}
          <span>{hardest ? ' is the toughest' : ''}</span>
        </strong>
      </div>
      <div
        className="chart-frame"
        role="img"
        aria-label={`Failure rate by level. ${data.map((d) => `Level ${d.level}: ${d.rate == null ? 'N/A' : `${d.rate}%`} from ${d.attempts} attempts`).join('; ')}`}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 15, right: 5, bottom: 5, left: 0 }}>
            <CartesianGrid vertical={false} stroke="#ededed" strokeDasharray="3 5" />
            <XAxis dataKey="level" {...axis} />
            <YAxis width={56} {...axis} tickFormatter={(v) => `${v}%`} domain={[0, 100]} />
            <Tooltip cursor={{ fill: '#f3f4f4', radius: 8 }} content={<ChartTip />} />
            <Bar dataKey="rate" name="Failure rate" radius={[7, 7, 7, 7]} isAnimationActive={false}>
              {data.map((d) => (
                <Cell key={d.level} fill={d.level === hardest?.level ? '#a8bd5d' : '#d8e1c1'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="chart-footnote">
        Misses ÷ attempted rounds at each level. Timeouts reported separately.
      </p>
    </Card>
  )
}
export function OutcomesChart({ rounds = [], stats: suppliedStats }) {
  const stats = suppliedStats || summarize(rounds)
  const data = [
    { name: 'Wins', value: stats.wins, fill: '#b8cf77' },
    { name: 'No overlap', value: stats.losses - stats.timeouts, fill: '#96b6ff' },
    { name: 'Timeouts', value: stats.timeouts, fill: '#e7e9ea' },
  ]
  return (
    <Card className="chart-card outcomes">
      <CardHeader title="Every round counts" subtitle="Round outcomes" icon={Target} />
      <div className="outcomes-content">
        <div
          className="donut-frame"
          role="img"
          aria-label={data.map((d) => `${d.name}: ${d.value}`).join(', ')}
        >
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                innerRadius="72%"
                outerRadius="95%"
                paddingAngle={4}
                stroke="none"
                cornerRadius={5}
                isAnimationActive={false}
              >
                {data.map((d) => (
                  <Cell key={d.name} fill={d.fill} />
                ))}
              </Pie>
              <Tooltip content={<ChartTip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="donut-label">
            <strong>{stats.games}</strong>
            <span>rounds played</span>
          </div>
        </div>
        <div className="outcome-legend">
          {data.map((d) => (
            <div key={d.name}>
              <span>
                <i style={{ background: d.fill }} />
                {d.name}
              </span>
              <strong>
                {d.value}
                <small>{stats.games ? Math.round((d.value / stats.games) * 100) : 0}%</small>
              </strong>
            </div>
          ))}
        </div>
      </div>
    </Card>
  )
}
export function ScoreChart({ rounds = [], data: suppliedData }) {
  const data = suppliedData || scoreBuckets(rounds)
  return (
    <Card className="chart-card">
      <CardHeader title="The score spread" subtitle="Completed rounds by points" icon={Clock3} />
      <div
        className="chart-frame compact-chart"
        role="img"
        aria-label={data.map((d) => `${d.label} points: ${d.rounds} rounds`).join('; ')}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ left: -28, top: 25, bottom: 7 }}>
            <CartesianGrid vertical={false} stroke="#ededed" />
            <XAxis dataKey="label" {...axis} tick={{ ...axis.tick, fontSize: 10 }} />
            <YAxis allowDecimals={false} {...axis} />
            <Tooltip content={<ChartTip />} />
            <Bar
              dataKey="rounds"
              name="Rounds"
              fill="#96b6ff"
              radius={[9, 9, 0, 0]}
              maxBarSize={58}
              isAnimationActive={false}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="chart-footnote">Classic v1 · maximum 1,500 points</p>
    </Card>
  )
}
