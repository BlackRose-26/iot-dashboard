import { useState } from 'react'
import {
  CalendarDays,
  ArrowUpRight,
  Gamepad2,
  Target,
  Trophy,
  Clock3,
  Sparkles,
  ArrowRight,
  Info,
  Send,
  Download,
} from '../components/icons'
import { useApp } from '../state/AppContext'
import { summarize } from '../data/demo'
import {
  Card,
  CardHeader,
  PageHeading,
  Metric,
  Menu,
  EmptyState,
  Button,
  Badge,
  FormatNumber,
  InfoNote,
} from '../components/ui'
import { ActivityChart, LevelChart, OutcomesChart, ScoreChart } from '../components/charts'

export default function Analytics() {
  const { rounds } = useApp()
  const [period, setPeriod] = useState('all')
  const [insight, setInsight] = useState('')
  const selected =
    period === 'empty'
      ? []
      : period === 'morning'
        ? rounds.filter((r) => r.hour < 12)
        : period === 'afternoon'
          ? rounds.filter((r) => r.hour >= 12)
          : rounds
  const stats = summarize(selected)
  const data = Array.from({ length: 24 }, (_, hour) => ({ label: `${hour}:00` })).map((a) => ({
    ...a,
    games: selected.filter((r) => `${r.hour}:00` === a.label).length,
    wins: selected.filter((r) => `${r.hour}:00` === a.label && r.won).length,
  }))
  const labels = {
    all: 'Today · all day',
    morning: 'Morning · 9–11',
    afternoon: 'Afternoon · 12–15',
    empty: 'No-data example',
  }
  const questions = [
    'How is the carnival doing?',
    'What does accuracy mean?',
    'What should we improve?',
  ]
  const answer =
    insight === questions[0]
      ? `${stats.players} players completed ${stats.games} rounds in this selection. ${stats.wins} rounds reached all 12 levels, for a ${stats.winRate?.toFixed(1) ?? 'N/A'}% win rate.`
      : insight === questions[1]
        ? 'Placement accuracy is the total LED cells retained divided by the total attempted row width. It measures overlap in this game, not physical tower stability.'
        : 'Compare failure rates using each level’s attempt count. Play-test the timing of difficult levels before changing rules; publish any change as a new ruleset.'
  return (
    <>
      <PageHeading
        title="A little insight goes a long way."
        description="Understand the play. Make the next round even better."
      >
        <Menu
          label="Analytics time window"
          value={labels[period]}
          icon={CalendarDays}
          options={Object.entries(labels).map(([value, label]) => ({ value, label }))}
          onChange={setPeriod}
        />
      </PageHeading>
      <div className="metrics-grid">
        <Metric
          label="Completed rounds"
          value={stats.games}
          detail={`${stats.players} unique players`}
          icon={Gamepad2}
          accent
        />
        <Metric
          label="Win rate"
          value={stats.winRate == null ? 'N/A' : `${stats.winRate.toFixed(1)}%`}
          detail={`${stats.wins} wins / ${stats.games} rounds`}
          icon={Trophy}
        />
        <Metric
          label="Avg. round time"
          value={stats.duration == null ? 'N/A' : `${stats.duration.toFixed(1)}s`}
          detail="Completed rounds only"
          icon={Clock3}
        />
        <Metric
          label="Overlap accuracy"
          value={stats.accuracy == null ? 'N/A' : `${stats.accuracy.toFixed(1)}%`}
          detail="Pooled retained / attempted cells"
          icon={Target}
        />
      </div>
      {!selected.length ? (
        <Card>
          <EmptyState
            title="The story hasn’t started yet."
            description="No completed games in this selection. Metrics appear after valid results are recorded."
            action={
              <Button onClick={() => setPeriod('all')}>
                Show saved activity
                <ArrowRight size={17} />
              </Button>
            }
          />
        </Card>
      ) : (
        <div className="two-column analytics-charts">
          <ActivityChart data={data} />
          <LevelChart rounds={selected} />
          <OutcomesChart rounds={selected} />
          <ScoreChart rounds={selected} />
        </div>
      )}
      <Card className="insights-card">
        <div className="insight-intro">
          <span className="insight-spark">
            <Sparkles size={25} />
          </span>
          <Badge>Read-only insights</Badge>
          <h2>Ask about the game.</h2>
          <p>Turn today’s numbers into a clearer picture.</p>
          <span className="insight-status">
            <span className="tiny-dot" />
            AI connection coming in the backend phase
          </span>
        </div>
        <div className="insight-workspace">
          <span className="eyebrow">EXPLORE SAVED RESULTS</span>
          <div className="question-pills">
            {questions.map((q) => (
              <button
                key={q}
                className={insight === q ? 'selected' : ''}
                onClick={() => setInsight(q)}
              >
                {q}
                <ArrowUpRight size={15} />
              </button>
            ))}
          </div>
          {insight ? (
            <div className="insight-answer" role="status">
              <div>
                <Sparkles size={16} />
                <strong>Recorded game summary</strong>
                <Badge>Not AI-generated</Badge>
              </div>
              <p>
                {selected.length
                  ? answer
                  : 'There are no completed rounds in this selection. Choose a time window with data before drawing a conclusion.'}
              </p>
              <small>
                Source: saved results (all sources) · {labels[period]} · Classic v1 ·{' '}
                {selected.length} rounds
              </small>
            </div>
          ) : (
            <div className="insight-placeholder">
              <span>Pick a question to explore the saved results.</span>
              <ArrowUpRight size={20} />
            </div>
          )}
        </div>
      </Card>
      <InfoNote>
        All charts use valid completed rounds in the selected window. Practice, expired, aborted and
        invalidated results are excluded. Includes clearly marked simulator rounds.
      </InfoNote>
    </>
  )
}
