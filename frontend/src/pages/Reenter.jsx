import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../state/api'
import { useApp } from '../state/AppContext'
import { PublicHeader } from './Leaderboard'
import { Card } from '../components/ui'

// Opened from the operator's one-time re-entry QR (/reenter#<code>). The code rides in the
// URL fragment, so it never reaches the server or tunnel logs; it is removed from the address
// bar immediately and redeemed exactly once.
export default function Reenter() {
  const { refreshPlayer } = useApp()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const started = useRef(false)

  useEffect(() => {
    if (started.current) return // the code is single use; never send it twice
    started.current = true
    const token = window.location.hash.slice(1)
    window.history.replaceState(null, '', '/reenter')
    if (!/^[A-Za-z0-9_-]{40,64}$/.test(token)) {
      setError('This re-entry link is incomplete. Ask the operator to show the QR again.')
      return
    }
    api('/player/reenter', { method: 'POST', body: { token } })
      .then(async () => {
        await refreshPlayer()
        navigate('/ticket', { replace: true })
      })
      .catch((failure) => setError(failure.message))
  }, [navigate, refreshPlayer])

  return (
    <div className="public-shell registration-shell">
      <PublicHeader />
      <main id="main-content" className="tw:mx-auto tw:w-full tw:max-w-xl tw:px-4 tw:py-10">
        <Card className="tw:p-7" role="status" aria-live="polite">
          <h1 className="tw:m-0 tw:mb-3 tw:text-2xl tw:font-bold">
            {error ? 'Re-entry did not work' : 'Restoring your ticket…'}
          </h1>
          {error ? (
            <>
              <p className="tw:m-0 tw:mb-5">{error}</p>
              <Link className="button light" to="/scan">
                Scan the cabinet QR instead
              </Link>
            </>
          ) : (
            <p className="tw:m-0">One moment while we reopen your place in line.</p>
          )}
        </Card>
      </main>
    </div>
  )
}
