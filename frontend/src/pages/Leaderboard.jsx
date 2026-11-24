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
import { CLASSIC_GAME, gameLabel } from '../state/game'
import { api } from '../state/api'
import PlayerList from '../components/PlayerList'
import SiteHeader from '../components/SiteHeader'
import { Badge, SearchInput, Card, EmptyState, Button, InfoNote } from '../components/ui'

// Every player page shares the site header (Home, About, Contact) with its skip link.
export function PublicHeader() {
  return <SiteHeader />
}
export default function Leaderboard() {
  const { revision } = useApp()
  const [rounds, setRounds] = useState([])
  const [source, setSource] = useState('')
  const [game, setGame] = useState(CLASSIC_GAME)
  const [error, setError] = useState('')
  useEffect(() => {
    let live = true
    api('/player/leaderboard')
      .then((data) => {
        if (live) {
          setRounds(data.rounds)
          setSource(data.source)
          setGame(data.game || CLASSIC_GAME)
          setError('')
        }
      })
      .catch((e) => {
        if (live) setError(e.message)
      })
    return () => {
      live = false
    }
  }, [revision])
  const [search, setSearch] = useState('')
  const [requestedPage, setPage] = useState(0)
  const ranked = rankPlayers(rounds)
  const displayed = ranked.filter((p) =>
    `${p.nickname} ${p.code}`.toLowerCase().includes(search.toLowerCase()),
  )
  const page = Math.min(requestedPage, Math.max(0, Math.ceil(displayed.length / 12) - 1))
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
          <p>ACS Carnival · {gameLabel(game)} · Verified saved results</p>
        </div>
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
        {source === 'simulator' && (
          <InfoNote>
            Dashboard simulator leaderboard · development rounds only. Cabinet / Wokwi scores are
            separate.
          </InfoNote>
        )}
        {source === 'device' && (
          <InfoNote>Cabinet / Wokwi leaderboard · includes connected simulator rounds.</InfoNote>
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
                    onClick={() => setPage(Math.max(0, page - 1))}
                  >
                    <ChevronLeft size={18} />
                  </button>
                  <span>Page {page + 1}</span>
                  <button
                    aria-label="Next page"
                    disabled={(page + 1) * 12 >= displayed.length}
                    onClick={() => setPage(page + 1)}
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
