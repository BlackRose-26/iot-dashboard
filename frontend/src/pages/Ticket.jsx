import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { Check, ArrowUpRight, Ticket as TicketIcon } from '../components/icons'
import { useApp } from '../state/AppContext'
import { gameLabel } from '../state/game'
import { PublicHeader } from './Leaderboard'
import { Card, Badge, Button, Modal, InfoNote } from '../components/ui'
import { StackArtwork } from './Registration'
import { ScanGate } from './Entry'
import UpdateStatus from '../components/UpdateStatus'

const titles = {
  waiting: 'You’re on the list.',
  called: 'It’s your turn.',
  playing: 'Make it count.',
  review: 'The operator is checking your round.',
  completed: 'That’s your stack.',
  cancelled: 'Your place was released.',
  expired: 'Your ticket has expired.',
}
const waitingMessages = {
  paused: 'The operator has paused the queue. Your place is saved; wait for it to reopen.',
  offline:
    'The cabinet is not ready yet. Your place is saved. Ask the operator to check the cabinet connection.',
  review:
    'The operator is reviewing the cabinet. Your place is saved; please wait for the review to finish.',
  busy: 'The cabinet is handling another round. The operator will call the next player when it is ready.',
  awaiting_operator:
    'The cabinet is ready. Wait for the operator to call the next player; registration does not start a round.',
}
export default function Ticket() {
  const { ticket, player, cancelTicket, connectionError } = useApp()
  const [cancelOpen, setCancelOpen] = useState(false)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [permission, setPermission] = useState(() =>
    'Notification' in window ? Notification.permission : 'unsupported',
  )
  const [notificationHint, setNotificationHint] = useState('')
  const heading = useRef(null)
  const lastStatus = useRef('')
  useEffect(() => {
    heading.current?.focus()
  }, [ticket?.status])
  useEffect(() => {
    if (!ticket) return
    const key = `${ticket.id}:${ticket.status}`
    if (lastStatus.current === key) return
    const changed = Boolean(lastStatus.current)
    lastStatus.current = key
    if (
      changed &&
      ['called', 'completed'].includes(ticket.status) &&
      'Notification' in window &&
      Notification.permission === 'granted'
    ) {
      try {
        new Notification(
          ticket.status === 'called'
            ? 'Your turn at Cabinet 01!'
            : ticket.outcome === 'win'
              ? 'You won! Your result is ready.'
              : 'Game finished. Your result is ready.',
          {
            body:
              ticket.status === 'called'
                ? `Bring your player code ${ticket.code}.`
                : `${ticket.score} points. Open your ticket to view the leaderboard.`,
            tag: key,
          },
        )
      } catch {
        setNotificationHint('Your browser uses in-page alerts on this device. Keep this page open.')
      }
    }
  }, [ticket])
  async function enableNotifications() {
    try {
      const result = await Notification.requestPermission()
      setPermission(result)
      if (result !== 'granted')
        setNotificationHint('You will still receive updates here. Keep this page open.')
    } catch {
      setNotificationHint(
        'Browser notifications are unavailable. Updates will appear on this page.',
      )
    }
  }
  if (!ticket) return <ScanGate />
  const called = ticket.status === 'called'
  const completed = ticket.status === 'completed'
  const waiting = ticket.status === 'waiting'
  const playing = ticket.status === 'playing'
  return (
    <div className="public-shell ticket-shell">
      <PublicHeader />
      <main id="main-content">
        <div className="ticket-layout">
          <div className="ticket-story">
            <Badge tone="lime">
              <Check size={14} />
              {completed ? 'ROUND COMPLETE' : 'YOUR PLACE IS SAVED'}
            </Badge>
            <h1 ref={heading} tabIndex={-1}>
              {completed
                ? ticket.outcome === 'win'
                  ? 'All the way up.\nYou won!'
                  : 'One more level.\nNext time.'
                : titles[ticket.status]}
            </h1>
            <p>
              {called
                ? 'Head to Cabinet 01. The operator will help you start with the physical button.'
                : playing
                  ? 'Your game is running at the cabinet. Your result will arrive here automatically.'
                  : completed
                    ? 'Win or lose, every stack counts. Your score is saved.'
                    : waiting
                      ? 'Keep this page open. Your place updates automatically.'
                      : ticket.status === 'review'
                        ? 'Your round is held for review. Keep this ticket open and ask the operator for help.'
                        : 'Check with the operator, or scan the cabinet QR code to join again.'}
            </p>
            <StackArtwork />
          </div>
          <Card className="player-ticket">
            <div className="ticket-top">
              <span className="ticket-icon">
                <TicketIcon size={29} />
              </span>
              <Badge tone={called || completed ? 'blue' : 'soft'} dot>
                {ticket.status}
              </Badge>
            </div>
            <span className="eyebrow">YOUR PLAYER CODE</span>
            <h2>{ticket.code}</h2>
            <p className="ticket-nickname">Hey, {ticket.nickname}.</p>
            <UpdateStatus />
            <div className="ticket-divider" />
            <div className="ticket-position" role="status" aria-live="polite" aria-atomic="true">
              <span>
                {completed
                  ? ticket.outcome === 'win'
                    ? 'You reached the top!'
                    : 'Good game. Keep stacking.'
                  : called
                    ? 'You’re up now'
                    : playing
                      ? 'Round in progress'
                      : waiting
                        ? 'Your place in line'
                        : ticket.status === 'review'
                          ? 'Waiting for the operator'
                          : 'Ticket closed'}
              </span>
              <strong>
                {completed ? (
                  ticket.score?.toLocaleString()
                ) : waiting ? (
                  String(ticket.position).padStart(2, '0')
                ) : called ? (
                  <ArrowUpRight size={62} />
                ) : (
                  '—'
                )}
              </strong>
              <p>
                {completed
                  ? `points · Level ${ticket.level} / ${ticket.game?.levels || 12}`
                  : waiting
                    ? ticket.position === 1
                      ? 'You’re first in line. Wait for the operator to call you.'
                      : `${ticket.position - 1} ${ticket.position === 2 ? 'player' : 'players'} ahead of you`
                    : called
                      ? 'The cabinet is reserved for you.'
                      : playing
                        ? 'Timing stays on the cabinet.'
                        : ticket.status === 'review'
                          ? 'Your reservation is held. Please speak with the operator.'
                          : 'Scan the QR for another turn.'}
              </p>
            </div>
            {waiting && (
              <div role="status" aria-live="polite" aria-atomic="true">
                <InfoNote>
                  {waitingMessages[player.queueState] ||
                    'Your place is saved. The operator calls players when the cabinet is ready.'}
                </InfoNote>
              </div>
            )}
            {completed && (
              <div className="result-notification" role="alert">
                <i
                  className={`fa-solid fa-${ticket.outcome === 'win' ? 'trophy' : 'flag-checkered'}`}
                  aria-hidden="true"
                />
                <div>
                  <strong>
                    {ticket.outcome === 'win'
                      ? 'You won! Congratulations.'
                      : 'Game finished. Thanks for playing!'}
                  </strong>
                  <p>Your result is saved. The leaderboard is now unlocked.</p>
                </div>
              </div>
            )}
            {ticket.source === 'simulator' && (
              <Badge tone="soft">Simulator round · separate from device scores</Badge>
            )}
            <div className="ticket-details">
              <div>
                <span>Event</span>
                <strong>ACS Carnival</strong>
              </div>
              <div>
                <span>Cabinet</span>
                <strong>01</strong>
              </div>
              <div>
                <span>Rules</span>
                <strong>{gameLabel(ticket.game)}</strong>
              </div>
            </div>
            {completed ? (
              <Link className="button dark full-width" to="/leaderboard/acs-day">
                View the leaderboard
                <ArrowUpRight size={17} />
              </Link>
            ) : (
              <p className="field-help">The leaderboard unlocks after your game finishes.</p>
            )}
            {!completed && permission === 'default' && window.isSecureContext && (
              <button className="button light full-width" onClick={enableNotifications}>
                <i className="fa-solid fa-bell" aria-hidden="true" />
                Enable turn & result alerts
              </button>
            )}
            {notificationHint && (
              <p role="status" className="field-help">
                {notificationHint}
              </p>
            )}
            {permission === 'granted' && !completed && (
              <p className="field-help">
                Browser alerts enabled. Keep this page open for reliable updates.
              </p>
            )}
            {waiting && (
              <button className="text-button ticket-cancel" onClick={() => setCancelOpen(true)}>
                Leave queue
              </button>
            )}
            {error && (
              <p className="field-error" role="alert">
                {error}
              </p>
            )}
            <InfoNote>
              Your ticket is private to this browser. Your student ID never appears here. Updates
              reconnect automatically.
            </InfoNote>
          </Card>
        </div>
      </main>
      <footer className="public-footer">Stack Moko Baby · A little timing. A lot of fun.</footer>
      <Modal
        title="Leave the queue?"
        description="Your waiting place will be released. Scan the QR again to rejoin."
        open={cancelOpen}
        onOpenChange={setCancelOpen}
      >
        <div className="modal-actions">
          <Button tone="light" onClick={() => setCancelOpen(false)}>
            Keep my place
          </Button>
          <Button
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              try {
                await cancelTicket()
                setCancelOpen(false)
              } catch (e) {
                setError(e.message)
              } finally {
                setBusy(false)
              }
            }}
          >
            Leave queue
          </Button>
        </div>
      </Modal>
    </div>
  )
}
