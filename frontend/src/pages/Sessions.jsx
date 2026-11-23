import { useState } from 'react'
import {
  Download,
  ArrowUpRight,
  ChevronLeft,
  ChevronRight,
  History,
  Trophy,
  Timer,
} from '../components/icons'
import {
  Card,
  CardHeader,
  PageHeading,
  Badge,
  Menu,
  SearchInput,
  Button,
  Avatar,
  Modal,
  EmptyState,
  Metric,
} from '../components/ui'
import { useApp } from '../state/AppContext'
import { gameLabel } from '../state/game'

export function downloadResults(data) {
  const clean = (value) =>
    `"${String(value)
      .replace(/^(?=\s*[=+@-]|[\t\r\n])/, "'")
      .replaceAll('"', '""')}"`
  const rows = [
    [
      'Round',
      'Player code',
      'Nickname',
      'Score',
      'Level',
      'Result',
      'Duration seconds',
      'Completed UTC',
      'Source',
    ],
    ...data.map((r) => [
      r.id,
      r.code,
      r.nickname,
      r.score,
      r.level,
      r.reason,
      r.duration,
      r.completedAt,
      r.source,
    ]),
  ]
  const blob = new Blob([rows.map((row) => row.map(clean).join(',')).join('\r\n')], {
    type: 'text/csv;charset=utf-8;',
  })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = 'stack-moko-baby-results.csv'
  anchor.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
export default function Sessions() {
  const { rounds, game } = useApp()
  const [search, setSearch] = useState('')
  const [outcome, setOutcome] = useState('all')
  const [requestedPage, setPage] = useState(0)
  const [selected, setSelected] = useState(null)
  const labels = { all: 'All outcomes', win: 'Wins', loss: 'Losses', timeout: 'Timeouts' }
  const filtered = rounds.filter(
    (r) =>
      `${r.nickname} ${r.code} ${r.id}`.toLowerCase().includes(search.toLowerCase()) &&
      (outcome === 'all' ||
        (outcome === 'win' && r.won) ||
        (outcome === 'loss' && !r.won) ||
        (outcome === 'timeout' && r.reason === 'Time expired')),
  )
  const pages = Math.max(1, Math.ceil(filtered.length / 10))
  const page = Math.min(requestedPage, pages - 1)
  return (
    <>
      <PageHeading
        title="Every stack has a story."
        description="A clear record of every round, from the first press to the final score."
      >
        <Button tone="light" onClick={() => downloadResults(filtered)} disabled={!filtered.length}>
          <Download size={16} />
          Export CSV
        </Button>
      </PageHeading>
      <Card className="sessions-card">
        <CardHeader
          title="Round history"
          subtitle={`${gameLabel(game)} · Saved rounds · Asia/Manila`}
          icon={History}
          action={<Badge>{filtered.length} rounds</Badge>}
        />
        <div className="table-tools">
          <SearchInput
            value={search}
            onChange={(v) => {
              setSearch(v)
              setPage(0)
            }}
            placeholder="Search player, code or round"
          />
          <Menu
            label="Filter round outcome"
            value={labels[outcome]}
            options={Object.entries(labels).map(([value, label]) => ({ value, label }))}
            onChange={(v) => {
              setOutcome(v)
              setPage(0)
            }}
          />
        </div>
        {filtered.length ? (
          <>
            <div
              className="table-scroll"
              role="region"
              aria-label="Round history. Scroll horizontally for more columns."
              tabIndex={0}
            >
              <table>
                <caption className="sr-only">
                  Saved round history. Select View round for placement details.
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Player</th>
                    <th scope="col">Round</th>
                    <th scope="col">Score</th>
                    <th scope="col">Level</th>
                    <th scope="col">Outcome</th>
                    <th scope="col">Time</th>
                    <th scope="col">
                      <span className="sr-only">Details</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.slice(page * 10, page * 10 + 10).map((r, i) => (
                    <tr key={r.id}>
                      <td>
                        <div className="table-player">
                          <Avatar name={r.nickname} index={i} />
                          <div>
                            <strong>{r.nickname}</strong>
                            <span>{r.code}</span>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className="mono">{r.id}</span>
                        <div>
                          <Badge tone="soft">
                            {r.source === 'simulator' ? 'Simulator' : 'Cabinet / Wokwi'}
                          </Badge>
                        </div>
                      </td>
                      <td>
                        <strong>{r.score.toLocaleString()}</strong>
                      </td>
                      <td>
                        {r.level}
                        <span className="subtle"> / {r.maxLevel || 12}</span>
                      </td>
                      <td>
                        <Badge tone={r.won ? 'lime' : 'neutral'}>
                          {r.won ? 'Win' : r.reason === 'Time expired' ? 'Timeout' : 'Miss'}
                        </Badge>
                      </td>
                      <td>{r.duration}s</td>
                      <td>
                        <button
                          className="row-open"
                          aria-label={`View round ${r.id}`}
                          onClick={() => setSelected(r)}
                        >
                          <ArrowUpRight size={19} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="pagination">
              <span>
                Showing {page * 10 + 1}–{Math.min(page * 10 + 10, filtered.length)} of{' '}
                {filtered.length} rounds
              </span>
              <div>
                <button
                  disabled={page === 0}
                  onClick={() => setPage(Math.max(0, page - 1))}
                  aria-label="Previous page"
                >
                  <ChevronLeft size={19} />
                </button>
                <span>
                  {page + 1} / {pages}
                </span>
                <button
                  disabled={page + 1 >= pages}
                  onClick={() => setPage(page + 1)}
                  aria-label="Next page"
                >
                  <ChevronRight size={19} />
                </button>
              </div>
            </div>
          </>
        ) : (
          <EmptyState
            title="No rounds match."
            description="Try another player or outcome filter."
            action={
              <Button
                tone="light"
                onClick={() => {
                  setSearch('')
                  setOutcome('all')
                  setPage(0)
                }}
              >
                Clear filters
              </Button>
            }
          />
        )}
      </Card>
      <Modal
        title={selected ? `${selected.nickname}’s round` : 'Round details'}
        description={
          selected
            ? `${selected.id} · ${selected.code} · ${gameLabel({ code: selected.ruleset })} · saved result`
            : ''
        }
        open={Boolean(selected)}
        onOpenChange={(open) => {
          if (!open) setSelected(null)
        }}
      >
        {selected && (
          <>
            <div className="round-detail-metrics">
              <Metric label="Final score" value={selected.score} detail={selected.reason} accent />
              <Metric
                label="Completed level"
                value={`${selected.level} / ${selected.maxLevel || 12}`}
                detail={`${selected.perfect} perfect rows`}
              />
            </div>
            <h3 className="detail-subhead">Placement trail</h3>
            <div className="placement-trail">
              {selected.placements.map((p) => (
                <div key={p.level}>
                  <span>Level {p.level}</span>
                  <div className="overlap-track">
                    <i style={{ width: `${(p.overlap / p.width) * 100}%` }} />
                  </div>
                  <strong>
                    {p.overlap}/{p.width}
                  </strong>
                </div>
              ))}
            </div>
            <p className="field-help">
              Accuracy: {selected.accuracy.toFixed(1)}% · {selected.overlap} retained cells /{' '}
              {selected.totalWidth} attempted cells. {selected.duration}s played.
            </p>
          </>
        )}
      </Modal>
    </>
  )
}
