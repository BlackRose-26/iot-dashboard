import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button, Card, PageHeading } from '../components/ui'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'

import { topics, kinds } from '../components/reviewLabels'

const actions = {
  answer: 'Answer the question',
  needs_clarification: 'Ask what the person means',
  refused: 'Explain why it cannot help',
}
const decisions = { confirm: 'Marked right', correct: 'Meaning changed', reject: 'Marked unclear' }
const periods = {
  today: 'Today',
  yesterday: 'Yesterday',
  last_7_days: 'Past seven days',
  event_to_date: 'Whole event',
}
const sources = { all: 'Both game sources', device: 'Physical game', simulator: 'Simulator' }
const toolNames = {
  get_event_summary: 'Event totals',
  get_queue_summary: 'Waiting line',
  get_machine_summary: 'Machine status',
  get_player_scores: 'Player scores',
  get_top_scores: 'Leaders',
  get_level_statistics: 'Game levels',
  get_play_trend: 'Play over time',
  get_score_distribution: 'Spread of scores',
}
const selector = 'tw:w-full tw:rounded-lg tw:border tw:border-line tw:bg-surface tw:p-2 tw:text-ink'
const group = 'tw:flex tw:flex-wrap tw:items-center tw:gap-2'
const words = (value) => value.replaceAll('_', ' ')
function meaning(t) {
  return kinds[t.topic]?.[t[t.topic]] || topics[t.topic]
}
function describeContext(c) {
  if (!c) return 'No earlier topic.'
  const subject =
    kinds.knowledge[c.knowledge] ||
    kinds.definition[c.definition] ||
    c.tools.map((t) => toolNames[t]).join(', ')
  const parts = [subject, ...(c.metrics || []).map(words)]
  if (c.tools.length) parts.push(periods[c.period], sources[c.source])
  if (c.level) parts.push('Level ' + c.level)
  if (c.tools.includes('get_top_scores')) parts.push('First ' + c.limit + ' players')
  if (c.tools.includes('get_player_scores')) parts.push('Page ' + c.score_page)
  if (c.detailed) parts.push('More detail')
  if (c.language === 'taglish') parts.push('In Taglish')
  return parts.filter(Boolean).join(' · ')
}
function Select({ label, values, value, onChange }) {
  return (
    <label className="tw:grid tw:gap-1 tw:text-sm">
      {label}
      <select className={selector} value={value} onChange={(e) => onChange(e.target.value)}>
        {Object.entries(values).map(([key, name]) => (
          <option key={key} value={key}>
            {name}
          </option>
        ))}
      </select>
    </label>
  )
}
function Correction({ row, onSave, onCancel, busy }) {
  const previous = row.review?.annotation
  const [target, setTarget] = useState(previous?.target || row.target)
  const [behavior, setBehavior] = useState(previous?.behavior || row.expected_behavior)
  const [context, setContext] = useState(
    previous ? previous.expected_context : row.expected_context,
  )
  const subtypes = kinds[target.topic]
  const allowedActions = { ...actions }
  if (target.topic === 'unsupported' || (target.topic === 'follow_up' && !row.previous))
    delete allowedActions.answer
  function changeTopic(topic) {
    setTarget(subtypesFor(topic))
    setBehavior(
      topic === 'unsupported'
        ? 'refused'
        : topic === 'follow_up' && !row.previous
          ? 'needs_clarification'
          : 'answer',
    )
    setContext(topic === 'follow_up' ? row.expected_context || row.previous : null)
  }
  function subtypesFor(topic) {
    return kinds[topic] ? { topic, [topic]: '' } : { topic }
  }
  const state = target.topic === 'follow_up' && behavior === 'answer' ? context : null
  const changed =
    target.topic !== row.target.topic ||
    target[target.topic] !== row.target[row.target.topic] ||
    behavior !== row.expected_behavior ||
    JSON.stringify(state) !== JSON.stringify(row.expected_context)
  return (
    <fieldset
      disabled={busy}
      className="tw:grid tw:gap-3 tw:rounded-lg tw:border tw:border-line tw:p-4"
    >
      <legend>What should it mean?</legend>
      <Select label="Pick the topic" values={topics} value={target.topic} onChange={changeTopic} />
      {subtypes && (
        <Select
          label="Which part?"
          values={{ '': 'Choose one', ...subtypes }}
          value={target[target.topic]}
          onChange={(v) => setTarget({ ...target, [target.topic]: v })}
        />
      )}
      <Select
        label="What should the assistant do?"
        values={allowedActions}
        value={behavior}
        onChange={setBehavior}
      />
      {state && (
        <details>
          <summary>Change details from the last question</summary>
          <div className="tw:mt-2 tw:grid tw:gap-2">
            <Select
              label="When?"
              values={periods}
              value={state.period}
              onChange={(v) => setContext({ ...state, period: v })}
            />
            <Select
              label="Which games?"
              values={sources}
              value={state.source}
              onChange={(v) => setContext({ ...state, source: v })}
            />
            {[
              ['get_top_scores', 'limit', 'How many leaders?', 10],
              ['get_level_statistics', 'level', 'Which level?', 12],
              ['get_player_scores', 'score_page', 'Which page?', 2000],
            ].map(
              ([tool, field, label, max]) =>
                state.tools.includes(tool) && (
                  <label key={field}>
                    {label}
                    <input
                      className={selector}
                      type="number"
                      min="1"
                      max={max}
                      value={state[field] ?? ''}
                      onChange={(e) =>
                        setContext({
                          ...state,
                          [field]: e.target.value === '' ? null : Number(e.target.value),
                        })
                      }
                    />
                  </label>
                ),
            )}
            <Select
              label="Reply language"
              values={{ en: 'English', taglish: 'Taglish' }}
              value={state.language}
              onChange={(v) => setContext({ ...state, language: v })}
            />
            <label>
              <input
                type="checkbox"
                checked={state.detailed}
                onChange={(e) => setContext({ ...state, detailed: e.target.checked })}
              />{' '}
              Give more detail
            </label>
          </div>
        </details>
      )}
      <div className={group}>
        <Button
          disabled={!changed || Boolean(subtypes && !target[target.topic])}
          onClick={() => onSave('correct', { target, behavior, expected_context: state })}
        >
          Save my change
        </Button>
        <Button tone="light" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </fieldset>
  )
}

export default function QuestionReview({ embedded = false }) {
  const { admin } = useApp()
  const [packet, setPacket] = useState(null)
  const [active, setActive] = useState(null)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('unreviewed')
  const [editing, setEditing] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [reload, setReload] = useState(0)
  useEffect(() => {
    let live = true
    setError('')
    api('/admin/evaluation-review')
      .then((data) => {
        if (live) setPacket(data)
      })
      .catch((e) => {
        if (live) setError(e.message)
      })
    return () => {
      live = false
    }
  }, [reload])
  const all = packet?.cases || []
  const reviewed = all.filter((c) => c.review).length
  const visible = all.filter(
    (c) =>
      (filter === 'all' ||
        (filter === 'unreviewed' && !c.review) ||
        (filter === 'reviewed' && c.review) ||
        (filter === 'changes' && c.review?.decision === 'correct') ||
        (filter === 'unclear' && c.review?.decision === 'reject') ||
        (filter === 'missed' && !c.passed)) &&
      (c.question + ' ' + meaning(c.target)).toLowerCase().includes(search.trim().toLowerCase()),
  )
  const row = visible.find((c) => c.id === active) || visible[0]
  const index = visible.indexOf(row)
  function choose(id) {
    setActive(id)
    setEditing(false)
    setError('')
    setNotice('')
  }
  async function save(decision, annotation = null) {
    if (busy) return
    setBusy(true)
    setError('')
    try {
      const review = await api('/admin/evaluation-review/' + row.id, {
        method: 'PUT',
        csrf: admin.csrf,
        body: {
          version: packet.version,
          revision: row.review?.revision || 0,
          decision,
          annotation,
        },
      })
      setPacket((p) => ({
        ...p,
        cases: p.cases.map((c) => (c.id === row.id ? { ...c, review } : c)),
      }))
      setActive(visible[index + 1]?.id || (filter === 'unreviewed' ? null : row.id))
      setEditing(false)
      setNotice('Saved. ' + decisions[decision] + '.')
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }
  return (
    <>
      {!embedded && (
        <PageHeading
          eyebrow="STACK INTELLIGENCE"
          title="Review questions"
          description="Read a practice question. Does the suggested meaning fit?"
        >
          <Link className="text-button" to="/admin/settings">
            Back to settings
          </Link>
        </PageHeading>
      )}
      <div className="tw:mx-auto tw:grid tw:max-w-4xl tw:gap-4">
        {error && (
          <p role="alert">
            {error}{' '}
            <Button
              tone="light"
              onClick={() => {
                setEditing(false)
                setReload((n) => n + 1)
              }}
            >
              Reload questions
            </Button>
          </p>
        )}
        {notice && <p role="status">{notice}</p>}
        {!packet && !error && <p role="status">Loading practice questions…</p>}
        {packet && (
          <>
            <Card className="tw:grid tw:gap-3 tw:p-5">
              <label className="tw:grid tw:gap-1 tw:font-semibold">
                {reviewed} of {all.length} reviewed
                <progress className="tw:w-full" max={all.length} value={reviewed} />
              </label>
              <fieldset
                disabled={busy}
                className="tw:grid tw:gap-3 tw:border-0 tw:p-0 tw:sm:grid-cols-2"
              >
                <Select
                  label="Show questions"
                  value={filter}
                  values={{
                    unreviewed: 'Still to review',
                    reviewed: 'Already reviewed',
                    changes: 'Meanings I changed',
                    unclear: 'Questions I marked unclear',
                    missed: 'Missed in the original test',
                    all: 'All questions',
                  }}
                  onChange={(v) => {
                    setFilter(v)
                    choose(null)
                  }}
                />
                <label className="tw:grid tw:gap-1 tw:text-sm">
                  Find a question
                  <input
                    className={selector}
                    type="search"
                    value={search}
                    onChange={(e) => {
                      setSearch(e.target.value)
                      choose(null)
                    }}
                  />
                </label>
              </fieldset>
            </Card>
            {row ? (
              <Card className="tw:grid tw:gap-4 tw:p-5" key={row.id}>
                <div className="tw:flex tw:flex-wrap tw:justify-between tw:gap-2 tw:text-sm tw:text-muted">
                  <span>
                    Question {index + 1} of {visible.length} shown
                  </span>
                  <span>{decisions[row.review?.decision] || 'Still to review'}</span>
                </div>
                {row.previous && (
                  <div>
                    <strong>Earlier topic</strong>
                    <p>{describeContext(row.previous)}</p>
                  </div>
                )}
                <h2 className="tw:m-0 tw:text-xl tw:font-semibold">{row.question}</h2>
                <div className="tw:rounded-lg tw:bg-surface-soft tw:p-4">
                  <strong>Suggested meaning</strong>
                  <p>{meaning(row.target)}</p>
                  <p>{actions[row.expected_behavior]}.</p>
                  {row.expected_context && <p>{describeContext(row.expected_context)}</p>}
                </div>
                {row.review?.decision === 'correct' && (
                  <p>
                    Your change: {meaning(row.review.annotation.target)} ·{' '}
                    {actions[row.review.annotation.behavior]}
                    {row.review.annotation.expected_context &&
                      ' · ' + describeContext(row.review.annotation.expected_context)}
                  </p>
                )}
                {editing ? (
                  <Correction
                    row={row}
                    busy={busy}
                    onSave={save}
                    onCancel={() => setEditing(false)}
                  />
                ) : (
                  <div className={group}>
                    <Button disabled={busy} onClick={() => save('confirm')}>
                      Yes, that fits
                    </Button>
                    <Button tone="light" disabled={busy} onClick={() => setEditing(true)}>
                      Change the meaning
                    </Button>
                    <Button tone="light" disabled={busy} onClick={() => save('reject')}>
                      Too unclear to use
                    </Button>
                  </div>
                )}
                <details>
                  <summary>See the original test result</summary>
                  <p>
                    {row.passed
                      ? 'The assistant passed this question.'
                      : 'The assistant missed this question.'}{' '}
                    {row.result_status === 'needs_clarification'
                      ? 'It asked for more information.'
                      : row.result_status === 'refused'
                        ? 'It declined the request.'
                        : row.returned_label
                          ? 'It chose “' + meaning(labelTarget(row.returned_label)) + '”.'
                          : 'It returned no topic.'}
                  </p>
                  {row.review_notes && <p>Review note: {row.review_notes}</p>}
                  <small>Your choices are saved separately from the original test.</small>
                </details>
                <div className={group}>
                  <Button
                    tone="light"
                    disabled={busy || index <= 0}
                    onClick={() => choose(visible[index - 1].id)}
                  >
                    Previous
                  </Button>
                  <Button
                    tone="light"
                    disabled={busy || index >= visible.length - 1}
                    onClick={() => choose(visible[index + 1].id)}
                  >
                    Next question
                  </Button>
                </div>
              </Card>
            ) : (
              <Card className="tw:p-5">
                <p>
                  {reviewed === all.length && filter === 'unreviewed'
                    ? 'You reviewed every question.'
                    : 'No questions match this view.'}
                </p>
                <Button
                  tone="light"
                  onClick={() => {
                    setFilter('all')
                    setSearch('')
                    choose(null)
                  }}
                >
                  Show all questions
                </Button>
              </Card>
            )}
          </>
        )}
      </div>
    </>
  )
}
function labelTarget(label) {
  const [topic, subtype] = label.split(':')
  return { topic, [topic]: subtype }
}
