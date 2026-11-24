import { useEffect, useRef, useState } from 'react'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import { UserRoundX } from './icons'
import { Card, CardHeader, Button, InfoNote, Modal } from './ui'

// One-click no-show handling for a called player who never pressed start.
// It uses the same audited, boot-bound steps as Device recovery: request a device stop,
// then release with no score ONLY if the cabinet confirms the round never started.
// If the cabinet reports the round had started, nothing is released automatically.
const CONFIRM_WAIT_MS = 30000
const DEFAULT_REASON = 'Player did not come to the cabinet'

export default function NoShowRelease() {
  const { currentPlayer, deviceRecovery, admin, refresh, notify, busy } = useApp()
  const [confirming, setConfirming] = useState(false)
  const [reason, setReason] = useState(DEFAULT_REASON)
  const [phase, setPhase] = useState('idle') // idle | stopping | waiting | releasing | started | timeout | error
  const [error, setError] = useState('')
  const run = useRef(null) // { session, nickname, reason, startedAt }

  const actions = deviceRecovery?.allowedActions || []
  const eligible =
    currentPlayer?.source === 'device' &&
    ['reserved', 'review'].includes(currentPlayer.status) &&
    !deviceRecovery?.quarantined &&
    (deviceRecovery?.canFence || actions.includes('release_unstarted'))

  async function release() {
    setPhase('releasing')
    await api(`/admin/sessions/${run.current.session}/resolve`, {
      method: 'POST',
      csrf: admin.csrf,
      key: crypto.randomUUID(),
      body: {
        expectedRevision: deviceRecovery.revision,
        reason: run.current.reason,
        evidenceId: deviceRecovery.evidenceId,
        action: 'release_unstarted',
      },
    })
    notify(
      `${run.current.nickname}'s ticket was closed with no score. Call the next player when the cabinet shows ready.`,
    )
    run.current = null
    setPhase('idle')
    await refresh()
  }

  async function start() {
    const text = reason.trim()
    run.current = {
      session: currentPlayer.sessionId,
      nickname: currentPlayer.nickname,
      reason: text,
      startedAt: Date.now(),
    }
    setConfirming(false)
    setError('')
    try {
      if (actions.includes('release_unstarted')) {
        await release() // the stop was already confirmed earlier
        return
      }
      setPhase('stopping')
      await api(`/admin/sessions/${run.current.session}/fence`, {
        method: 'POST',
        csrf: admin.csrf,
        key: crypto.randomUUID(),
        body: { expectedRevision: deviceRecovery.revision, reason: text },
      })
      setPhase('waiting')
      await refresh()
    } catch (failure) {
      setError(failure.message)
      setPhase('error')
    }
  }

  // While waiting, refresh until the cabinet's stop receipt arrives (live updates also push it).
  useEffect(() => {
    if (phase !== 'waiting') return undefined
    const timer = setInterval(() => void refresh(), 1500)
    return () => clearInterval(timer)
  }, [phase, refresh])

  useEffect(() => {
    if (phase !== 'waiting' || !run.current) return
    if (currentPlayer?.sessionId !== run.current.session) {
      run.current = null // resolved elsewhere (another operator or the Machine page)
      setPhase('idle')
      return
    }
    if (actions.includes('release_unstarted')) {
      release().catch((failure) => {
        setError(failure.message)
        setPhase('error')
      })
    } else if (actions.includes('void_interrupted') || actions.includes('recover_result')) {
      setPhase('started')
    } else if (Date.now() - run.current.startedAt > CONFIRM_WAIT_MS) {
      setPhase('timeout')
    }
    // `release` reads the latest snapshot; re-run only when the snapshot changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, deviceRecovery, currentPlayer])

  const working = ['stopping', 'waiting', 'releasing'].includes(phase)
  if (!eligible && phase === 'idle') return null
  const status = {
    stopping: 'Asking the cabinet to stop this reservation…',
    waiting: 'Waiting for the cabinet to confirm the game never started…',
    releasing: 'Releasing the cabinet…',
  }[phase]

  return (
    <Card className="tw:mt-6 tw:p-7" aria-live="polite">
      <CardHeader
        title="Player didn't come?"
        subtitle={
          currentPlayer
            ? `${currentPlayer.nickname} was called but has not started. Release the cabinet with no score.`
            : 'The called player has not started.'
        }
      />
      {status && <p className="field-help">{status}</p>}
      {phase === 'started' && (
        <InfoNote>
          The cabinet reports this round had already started, so nothing was released. Resolve it on
          the Machine page under Device recovery.
        </InfoNote>
      )}
      {phase === 'timeout' && (
        <InfoNote>
          The cabinet has not confirmed the stop yet. Check that it is online. The stop request
          stays active for 3 minutes; you can finish on the Machine page under Device recovery.
        </InfoNote>
      )}
      {phase === 'error' && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <div className="tw:mt-4 tw:flex tw:flex-wrap tw:gap-2.5">
        <Button
          tone="light"
          disabled={busy || working || !eligible}
          onClick={() => {
            setReason(DEFAULT_REASON)
            setConfirming(true)
          }}
        >
          <UserRoundX size={16} /> Player didn't come
        </Button>
        {['started', 'timeout', 'error'].includes(phase) && (
          <Button tone="light" onClick={() => setPhase('idle')}>
            Dismiss
          </Button>
        )}
      </div>
      <Modal
        title="Release the cabinet?"
        description={`The cabinet is asked to stop ${currentPlayer?.nickname || 'this player'}'s reservation. Only if it confirms the game never started is the ticket closed with no score. The player can scan again to rejoin the line.`}
        open={confirming}
        onOpenChange={(open) => {
          if (!open) setConfirming(false)
        }}
      >
        <label className="field-label" htmlFor="no-show-reason">
          Reason (saved in the audit log)
        </label>
        <input
          id="no-show-reason"
          className="text-input"
          maxLength={160}
          value={reason}
          onChange={(event) => setReason(event.target.value)}
        />
        <div className="modal-actions">
          <Button tone="light" onClick={() => setConfirming(false)}>
            Keep waiting
          </Button>
          <Button disabled={!reason.trim()} onClick={() => void start()}>
            Stop and release
          </Button>
        </div>
      </Modal>
    </Card>
  )
}
