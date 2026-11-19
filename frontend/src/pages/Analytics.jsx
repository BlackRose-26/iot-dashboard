import { useEffect, useState } from 'react'
import { CalendarDays, Gamepad2, Target, Trophy, Clock3 } from '../components/icons'
import { api } from '../state/api'
import { useApp } from '../state/AppContext'
import { Card, PageHeading, Metric, Menu, EmptyState, Button, InfoNote } from '../components/ui'
import { ActivityChart, LevelChart, OutcomesChart, ScoreChart } from '../components/charts'

const periods = {
  event_to_date: 'Event to date',
  today: 'Today',
  yesterday: 'Yesterday',
  last_7_days: 'Last seven days',
}
const sources = { simulator: 'Simulator results', device: 'Physical device results' }
const value = (number, suffix = '') =>
  number == null
    ? 'N/A'
    : `${Number(number).toLocaleString('en-PH', { maximumFractionDigits: 1 })}${suffix}`

export default function Analytics() {
  const eventRevision = useApp()?.revision
  const [period, setPeriod] = useState('event_to_date')
  const [source, setSource] = useState('simulator')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [revision, setRevision] = useState(0)
  useEffect(() => {
    setData(null)
  }, [period, source])
  useEffect(() => {
    const controller = new AbortController()
    let active = true
    let running = false
    setError('')
    setLoading(true)
    async function load() {
      if (running) return
      running = true
      try {
        const response = await api(`/admin/analytics?${new URLSearchParams({ period, source })}`, {
          signal: controller.signal,
        })
        if (active) {
          setData(response)
          setError('')
        }
      } catch (failure) {
        if (active && failure.name !== 'AbortError') setError(failure.message)
      } finally {
        running = false
        if (active) setLoading(false)
      }
    }
    void load()
    const timer = setInterval(load, 15000)
    window.addEventListener('focus', load)
    return () => {
      active = false
      controller.abort()
      clearInterval(timer)
      window.removeEventListener('focus', load)
    }
  }, [period, source, revision, eventRevision])
  const summary = data?.summary
  return (
    <>
      <PageHeading
        title="A little insight goes a long way."
        description="Verified event analytics, shared with Stack Intelligence."
      >
        <Menu
          label="Analytics time window"
          value={periods[period]}
          icon={CalendarDays}
          options={Object.entries(periods).map(([key, label]) => ({ value: key, label }))}
          onChange={setPeriod}
        />
        <Menu
          label="Analytics result source"
          value={sources[source]}
          options={Object.entries(sources).map(([key, label]) => ({ value: key, label }))}
          onChange={setSource}
        />
        <Button tone="light" disabled={loading} onClick={() => setRevision((n) => n + 1)}>
          Refresh
        </Button>
      </PageHeading>
      {error && (
        <p className="field-error" role="alert">
          {error} {data ? 'Showing the last successful snapshot below.' : ''}
        </p>
      )}
      {loading && <p role="status">Loading recorded analytics…</p>}
      {summary && (
        <>
          <p className="analytics-scope">
            {data.scope_label} · Updated{' '}
            {new Date(data.as_of).toLocaleString('en-PH', { timeZone: 'Asia/Manila' })} Asia/Manila
          </p>
          <div className="metrics-grid">
            <Metric
              label="Completed rounds"
              value={summary.completed_games}
              detail={`${summary.completed_players} distinct completed players`}
              icon={Gamepad2}
            />
            <Metric
              label="Win rate"
              value={value(summary.win_rate, '%')}
              detail={`${summary.wins} wins / ${summary.completed_games} completed rounds`}
              icon={Trophy}
            />
            <Metric
              label="Avg. round time"
              value={value(summary.average_duration, 's')}
              detail="Valid completed rounds only"
              icon={Clock3}
            />
            <Metric
              label="Overlap accuracy"
              value={value(summary.accuracy, '%')}
              detail="Pooled retained / attempted cells"
              icon={Target}
            />
          </div>
          <InfoNote>
            {summary.registrations} new event registrations in this window (all sources). Result
            metrics above use only {sources[source].toLowerCase()}. Match these filters when
            comparing answers in chat.
          </InfoNote>
          {summary.completed_games ? (
            <div className="two-column analytics-charts">
              <ActivityChart data={data.trend.buckets} granularity={data.trend.granularity} />
              <LevelChart data={data.levels} />
              <OutcomesChart
                stats={{
                  games: summary.completed_games,
                  wins: summary.wins,
                  losses: summary.losses,
                  timeouts: summary.timeouts,
                }}
              />
              <ScoreChart data={data.scores} />
            </div>
          ) : (
            <Card>
              <EmptyState
                title="No completed rounds in this selection."
                description="Try a different time window or source. Missing averages and rates remain N/A."
              />
            </Card>
          )}
          <Card className="analytics-assistant-note">
            <h2>Ask Stack Intelligence.</h2>
            <p>
              Use the chat at the bottom for English or Taglish questions about players, queues,
              scores, trends and cabinet readiness. Answers use the same backend calculations.
              Ollama is optional for these charts.
            </p>
          </Card>
          {data.caveats.map((caveat) => (
            <InfoNote key={caveat}>{caveat}</InfoNote>
          ))}
        </>
      )}
    </>
  )
}
