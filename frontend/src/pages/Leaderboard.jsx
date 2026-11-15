import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowUpRight,
  Trophy,
  Medal,
  ChevronLeft,
  ChevronRight,
  Info,
} from '../components/icons'
import { rankPlayers } from '../data/demo'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import PlayerList from '../components/PlayerList'
import { Logo, Badge, SearchInput, Card, EmptyState, Button, InfoNote } from '../components/ui'

export function PublicHeader() {
  const { ticket } = useApp()
  return (
    <>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <header className="public-header">
        <Logo destination={ticket ? '/ticket' : '/'} />
        <Badge tone="soft">ACS Carnival · Player portal</Badge>
      </header>
    </>
  )
}
export default function Leaderboard() {
  const [rounds, setRounds] = useState([])
  const [source, setSource] = useState('')
  const [error, setError] = useState('')
  useEffect(() => {
    let live = true
    api('/player/leaderboard')
      .then((data) => {
        if (live) {
          setRounds(data.rounds)
          setSource(data.source)
        }
      })
      .catch((e) => {
        if (live) setError(e.message)
      })
    return () => {
      live = false
    }
  }, [])
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)
  const ranked = rankPlayers(rounds)
  const displayed = ranked.filter((p) =>
    `${p.nickname} ${p.code}`.toLowerCase().includes(search.toLowerCase()),
  )
  return (
    <div className="public-shell leaderboard-shell">
      <PublicHeader />
      <main id="main-content">
        <div className="leaderboard-heading">
          <Badge tone="lime">
            <Trophy size={14} />
            THE HIGH STACK
          </Badge>
          <h1>
            A little competitive?
            <br />
            <span>You’re in good company.</span>
          </h1>
          <p>ACS Carnival · 15 November 2026 · Classic v1</p>
        </div>
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
        {source === 'simulator' && (
          <InfoNote>
            Simulator leaderboard ? development rounds only. Physical cabinet scores are separate.
          </InfoNote>
        )}
        <div className="podium">
          {[ranked[1], ranked[0], ranked[2]].filter(Boolean).map((p) => (
            <Card className={`podium-card position-${p.rank}`} key={p.rank}>
              <span className="podium-medal">
                {p.rank === 1 ? <Trophy size={28} /> : <Medal size={25} />}
              </span>
              <span className="podium-rank">#{p.rank}</span>
              <h2>{p.nickname}</h2>
              <span className="subtle">{p.code}</span>
              <strong>
                {p.score.toLocaleString()}
                <span> pts</span>
              </strong>
              <p>
                Level {p.level} · {p.duration}s
              </p>
              <div className="podium-blocks" aria-hidden="true">
                {Array.from({ length: 8 }, (_, i) => (
                  <i key={i} />
                ))}
              </div>
            </Card>
          ))}
        </div>
        <Card className="full-leaderboard">
          <div className="leaderboard-table-heading">
            <div>
              <h2>Every player, one best stack.</h2>
              <p>{ranked.length} players · best valid round per player</p>
            </div>
            <SearchInput
              value={search}
              onChange={(v) => {
                setSearch(v)
                setPage(0)
              }}
            />
          </div>
          {displayed.length ? (
            <>
              <PlayerList players={displayed.slice(page * 12, page * 12 + 12)} />
              <div className="pagination">
                <span>
                  {page * 12 + 1}–{Math.min(page * 12 + 12, displayed.length)} of {displayed.length}{' '}
                  players
                </span>
                <div>
                  <button
                    aria-label="Previous page"
                    disabled={page === 0}
                    onClick={() => setPage((p) => p - 1)}
                  >
                    <ChevronLeft size={18} />
                  </button>
                  <span>Page {page + 1}</span>
                  <button
                    aria-label="Next page"
                    disabled={(page + 1) * 12 >= displayed.length}
                    onClick={() => setPage((p) => p + 1)}
                  >
                    <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            </>
          ) : (
            <EmptyState
              title="No matching players."
              description="Try a different nickname or public player code."
              action={
                <Button tone="light" onClick={() => setSearch('')}>
                  Clear search
                </Button>
              }
            />
          )}
        </Card>
        <InfoNote>
          Ranked by score, then completed levels, fastest round and earliest completion. Student IDs
          are always private. Only validated, saved rounds appear here.
        </InfoNote>
        <div className="leaderboard-cta">
          <span>Scan the cabinet QR again for another round.</span>
          <Link className="button dark" to="/ticket">
            Back to my result
            <ArrowUpRight size={17} />
          </Link>
        </div>
      </main>
      <footer className="public-footer">Stack Moko Baby · A little timing. A lot of fun.</footer>
    </div>
  )
}
