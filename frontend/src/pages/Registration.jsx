import { useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  ArrowUpRight,
  ArrowRight,
  ShieldCheck,
  Eye,
  EyeOff,
  UserRound,
  Hash,
  Layers3,
  Timer,
  Trophy,
  LoaderCircle,
} from '../components/icons'
import { Badge, Button, StepLabel, InfoNote, Card, EmptyState } from '../components/ui'
import { PublicHeader } from './Leaderboard'
import { useApp } from '../state/AppContext'
import { validateRegistration } from '../data/demo'
import { ScanGate } from './Entry'
import { CLASSIC_GAME, gameLabel } from '../state/game'

export function StackArtwork() {
  return (
    <div className="stack-artwork" aria-hidden="true">
      <div className="art-orbit orbit-one" />
      <div className="art-orbit orbit-two" />
      <div className="art-chip top">
        <span className="tiny-dot" />
        YOU’VE GOT THIS.
      </div>
      <div className="art-blocks">
        {[1, 2, 3, 4, 5].map((n, i) => (
          <div key={n} className={`art-row art-row-${i}`}>
            {Array.from({ length: n }, (_, j) => (
              <i key={j} />
            ))}
          </div>
        ))}
      </div>
      <div className="art-chip bottom">
        <Trophy size={17} />
        ONE MORE LEVEL.
      </div>
      <span className="art-star star-one">
        <i className="fa-solid fa-asterisk" />
      </span>
      <span className="art-star star-two">
        <i className="fa-solid fa-asterisk" />
      </span>
    </div>
  )
}
export default function Registration() {
  const { admissionsOpen, joinQueue, ticket, player, ready, game = CLASSIC_GAME } = useApp()
  const navigate = useNavigate()
  const [nickname, setNickname] = useState('')
  const [studentId, setStudentId] = useState('')
  const [acknowledged, setAcknowledged] = useState(false)
  const [visible, setVisible] = useState(false)
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const formRef = useRef(null)
  async function submit(event) {
    event.preventDefault()
    if (submitting || !admissionsOpen) return
    const nextErrors = validateRegistration({ nickname, studentId, acknowledged })
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length) {
      formRef.current?.elements.namedItem(Object.keys(nextErrors)[0])?.focus()
      return
    }
    setSubmitting(true)
    try {
      await joinQueue(nickname, studentId, acknowledged)
      setStudentId('')
      navigate('/ticket', { replace: true })
    } catch (error) {
      setErrors({ server: error.message })
    } finally {
      setStudentId('')
      setSubmitting(false)
    }
  }
  if (!ready)
    return (
      <div className="page-loading" role="status">
        Checking your QR entry…
      </div>
    )
  if (!player.canRegister && !ticket) return <ScanGate />
  const activeTicket = ticket && ['waiting', 'called', 'playing', 'review'].includes(ticket.status)
  if (!player.canRegister && !activeTicket)
    return (
      <ScanGate message="Scan the cabinet QR code again when you are ready for another round." />
    )
  return (
    <div className="public-shell registration-shell">
      <PublicHeader />
      <main id="main-content">
        <div className="registration-layout">
          <section className="registration-story">
            <Badge tone="lime">
              <Layers3 size={15} />
              STACK MOKO BABY
            </Badge>
            <h1>
              Good timing.
              <br />
              Great stacking.
              <br />
              <span>Your turn.</span>
            </h1>
            <p>
              A little focus. One big button.
              <br />
              How high can you go?
            </p>
            <StackArtwork />
            <div className="game-facts">
              <span>
                <Timer size={17} />
                <strong>60 seconds</strong>to make it count
              </span>
              <span>
                <Layers3 size={17} />
                <strong>{game.levels} levels</strong>to the top
              </span>
              <span>
                <Trophy size={17} />
                <strong>
                  {(game.levels * (game.row_points + game.perfect_bonus)).toLocaleString('en-PH')}{' '}
                  points
                </strong>
                the perfect stack
              </span>
            </div>
          </section>
          <Card className="registration-card">
            <div className="registration-topline">
              <StepLabel number="01">JOIN THE CARNIVAL</StepLabel>
              <Badge tone="soft" dot>
                Cabinet 01
              </Badge>
            </div>
            <h2>
              Your next high score
              <br />
              starts here.
            </h2>
            <p className="registration-intro">Join the queue. We’ll save you a spot.</p>
            {!window.isSecureContext && (
              <InfoNote>Use the event’s secure website before entering a real student ID.</InfoNote>
            )}
            {activeTicket ? (
              <div className="existing-ticket">
                <h3>Your place is already saved.</h3>
                <p>Pick up where you left off.</p>
                <Link className="button dark full-width" to="/ticket">
                  View my ticket
                  <ArrowRight size={18} />
                </Link>
              </div>
            ) : !admissionsOpen ? (
              <EmptyState
                title="A quick intermission."
                description="Admissions are paused. Please check with the cabinet operator."
              />
            ) : (
              <form
                className="tw:min-w-0"
                ref={formRef}
                onSubmit={submit}
                noValidate
                aria-label="Player registration"
              >
                {errors.server && (
                  <p className="field-error" role="alert">
                    {errors.server}
                  </p>
                )}
                <div className="form-group">
                  <label htmlFor="nickname">
                    Nickname<span>On the leaderboard</span>
                  </label>
                  <div className={`input-wrap ${errors.nickname ? 'invalid' : ''}`}>
                    <UserRound size={18} />
                    <input
                      id="nickname"
                      name="nickname"
                      autoComplete="off"
                      placeholder="What should we call you?"
                      value={nickname}
                      maxLength={24}
                      onChange={(e) => {
                        setNickname(e.target.value)
                        setErrors((p) => ({ ...p, nickname: undefined }))
                      }}
                      required
                      aria-invalid={Boolean(errors.nickname)}
                      aria-describedby={errors.nickname ? 'nickname-error' : 'nickname-help'}
                      disabled={submitting}
                    />
                  </div>
                  <p
                    id={errors.nickname ? 'nickname-error' : 'nickname-help'}
                    className={errors.nickname ? 'field-error' : 'field-help'}
                    role={errors.nickname ? 'alert' : undefined}
                  >
                    {errors.nickname ||
                      '2–24 characters. Pick something you’d like everyone to see.'}
                  </p>
                </div>
                <div className="form-group">
                  <label htmlFor="studentId">
                    Student ID
                    <span>
                      <ShieldCheck size={12} />
                      Always private
                    </span>
                  </label>
                  <div className={`input-wrap ${errors.studentId ? 'invalid' : ''}`}>
                    <Hash size={18} />
                    <input
                      id="studentId"
                      name="studentId"
                      type={visible ? 'text' : 'password'}
                      autoComplete="off"
                      spellCheck={false}
                      placeholder="For example, DEMO-2026"
                      value={studentId}
                      maxLength={32}
                      onChange={(e) => {
                        setStudentId(e.target.value)
                        setErrors((p) => ({ ...p, studentId: undefined }))
                      }}
                      required
                      aria-invalid={Boolean(errors.studentId)}
                      aria-describedby={errors.studentId ? 'student-error' : 'student-help'}
                      disabled={submitting}
                    />
                    <button
                      type="button"
                      aria-label={visible ? 'Hide student ID' : 'Show student ID'}
                      aria-pressed={visible}
                      onClick={() => setVisible(!visible)}
                    >
                      {visible ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  <p
                    id={errors.studentId ? 'student-error' : 'student-help'}
                    className={errors.studentId ? 'field-error' : 'field-help'}
                    role={errors.studentId ? 'alert' : undefined}
                  >
                    {errors.studentId ||
                      'Used to recognize players. Never shown on the leaderboard.'}
                  </p>
                </div>
                <div className="privacy-note">
                  <ShieldCheck size={21} />
                  <div>
                    <strong>Your game. Your privacy.</strong>
                    <p>
                      Only your nickname and a random player code appear publicly. Your student ID
                      is encrypted and used privately to recognize you and prevent duplicate
                      tickets.
                    </p>
                  </div>
                </div>
                <label className="checkbox-field">
                  <input
                    type="checkbox"
                    id="acknowledged"
                    name="acknowledged"
                    checked={acknowledged}
                    onChange={(e) => {
                      setAcknowledged(e.target.checked)
                      setErrors((p) => ({ ...p, acknowledged: undefined }))
                    }}
                    aria-invalid={Boolean(errors.acknowledged)}
                    aria-describedby={errors.acknowledged ? 'privacy-error' : undefined}
                    disabled={submitting}
                  />
                  <span>I understand how my player information will be used.</span>
                </label>
                {errors.acknowledged && (
                  <p className="field-error" id="privacy-error" role="alert">
                    {errors.acknowledged}
                  </p>
                )}
                <Button
                  type="submit"
                  tone="lime"
                  className="full-width join-button"
                  disabled={submitting}
                >
                  {submitting ? (
                    <>
                      <LoaderCircle size={19} className="spin" />
                      Saving your place…
                    </>
                  ) : (
                    <>
                      Let’s stack
                      <ArrowUpRight size={20} />
                    </>
                  )}
                </Button>
              </form>
            )}
            <div className="registration-footnote">
              <span>No account to create. Just a game to remember.</span>
              <span>The leaderboard unlocks after your game.</span>
            </div>
          </Card>
        </div>
      </main>
      <footer className="public-footer">
        ACS Carnival · {gameLabel(game)} · Game settings are proposed for play-testing.
      </footer>
    </div>
  )
}
