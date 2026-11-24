import { useEffect, useState } from 'react'
import { QRCodeCanvas } from 'qrcode.react'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import { QrCode } from './icons'
import { Card, CardHeader, Button, InfoNote, Modal, SearchInput } from './ui'

// Gives a player back their own ticket after a lost phone, a cleared browser or a launcher
// restart (player cookies belong to the old tunnel address). The operator finds the player,
// checks the person in front of them, and shows a one-time QR that works for 10 minutes.
const SEARCH_DELAY_MS = 300
const ticketLabels = {
  waiting: 'In line',
  assigned: 'Called to the cabinet',
  served: 'Played',
  cancelled: 'Left the line',
  expired: 'Expired',
}

function publicUrl(path) {
  try {
    const base = new URL(import.meta.env.VITE_PUBLIC_BASE_URL || window.location.origin)
    return ['http:', 'https:'].includes(base.protocol) ? new URL(path, base.origin).href : null
  } catch {
    return null
  }
}

export default function PlayerReentry() {
  const { admin, notify } = useApp()
  const [search, setSearch] = useState('')
  const [players, setPlayers] = useState([])
  const [error, setError] = useState('')
  const [issuing, setIssuing] = useState('')
  const [pass, setPass] = useState(null) // { nickname, url, expiresAt }

  useEffect(() => {
    const text = search.trim()
    if (!text) {
      setPlayers([])
      return undefined
    }
    let current = true
    const timer = setTimeout(() => {
      api(`/admin/players?search=${encodeURIComponent(text)}`)
        .then((data) => {
          if (!current) return
          setPlayers(data.players)
          setError('')
        })
        .catch((failure) => current && setError(failure.message))
    }, SEARCH_DELAY_MS)
    return () => {
      current = false
      clearTimeout(timer)
    }
  }, [search])

  async function issue(player) {
    setIssuing(player.id)
    setError('')
    try {
      const data = await api(`/admin/players/${encodeURIComponent(player.id)}/reentry`, {
        method: 'POST',
        csrf: admin.csrf,
      })
      const url = publicUrl(data.path)
      if (!url) throw new Error('The public address is not set, so the QR cannot be made.')
      setPass({ nickname: player.nickname, url, expiresAt: new Date(data.expiresAt) })
    } catch (failure) {
      setError(failure.message)
    } finally {
      setIssuing('')
    }
  }

  function close() {
    if (pass)
      notify(`Re-entry QR for ${pass.nickname} closed. Make a new one if it was not scanned.`)
    setPass(null) // the one-time code is dropped from memory as soon as the QR is closed
  }

  return (
    <Card className="tw:mt-6 tw:p-7">
      <CardHeader
        title="Player lost their ticket?"
        subtitle="New phone, cleared browser or the launcher was restarted. Find them and show a one-time QR."
      />
      <SearchInput
        value={search}
        onChange={setSearch}
        placeholder="Nickname or player code"
        label="Find a player to restore"
      />
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      {search.trim() && !players.length && !error && (
        <p className="field-help">No player matches that nickname or code.</p>
      )}
      {players.length > 0 && (
        <ul
          className="tw:m-0 tw:mt-3 tw:flex tw:list-none tw:flex-col tw:gap-2 tw:p-0"
          aria-label="Matching players"
        >
          {players.map((player) => (
            <li key={player.id} className="tw:flex tw:items-center tw:justify-between tw:gap-3">
              <span className="tw:min-w-0">
                <strong className="tw:block tw:truncate">{player.nickname}</strong>
                <span className="tw:text-muted tw:text-sm">
                  {player.code} · {ticketLabels[player.ticket] || 'No ticket yet'}
                </span>
              </span>
              <Button
                tone="light"
                disabled={Boolean(issuing)}
                onClick={() => void issue(player)}
                aria-label={`Show re-entry QR for ${player.nickname}`}
              >
                <QrCode size={16} /> Re-entry QR
              </Button>
            </li>
          ))}
        </ul>
      )}
      <Modal
        title={pass ? `Re-entry for ${pass.nickname}` : 'Re-entry'}
        description="Have the player scan this with their phone camera. It opens their own ticket."
        open={Boolean(pass)}
        onOpenChange={(open) => {
          if (!open) close()
        }}
      >
        {pass && (
          <>
            <div className="qr-wrap">
              <QRCodeCanvas
                value={pass.url}
                size={360}
                level="M"
                marginSize={4}
                title={`Re-entry QR for ${pass.nickname}`}
              />
            </div>
            <InfoNote>
              First check this is really {pass.nickname}. The QR works once, until{' '}
              {pass.expiresAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}, and
              signs their old phone out.
            </InfoNote>
            <div className="modal-actions">
              <Button onClick={close}>Done</Button>
            </div>
          </>
        )}
      </Modal>
    </Card>
  )
}
