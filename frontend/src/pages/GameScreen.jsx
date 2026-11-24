import { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../state/api'
import { ScreenDevice, pageClock } from '../screen/deviceClient'
import { SerialButton, serialSupported } from '../screen/button'
import {
  COUNTDOWN_MS,
  COUNTDOWN_STEP_MS,
  MATRIX_RULES,
  createRound,
  positionAt,
  press,
  timeout,
  toResult,
} from '../screen/engine'
import { playSound, unlockAudio } from '../screen/sound'

// Plan B game screen (25 Nov 2026): the stacking game runs here, full screen on the second
// laptop, and the arcade button reaches it through the ESP32 button bridge (Web Serial).
// The page plays as Cabinet 01 through the device journal, so every round is replayed and
// timed by the server exactly like an ESP32 round.

const COLORS = { night: '#111313', grid: '#1c2020', cloud: '#f4f5f5', lime: '#dfff00' }
const RESULT_MS = 8000
const KEYBOARD_KEY = 'smb.gameScreen.keyboard'
const ROWS = MATRIX_RULES.levels + 1 // foundation + 15 levels

function readFlag(key) {
  try {
    return window.localStorage.getItem(key) === '1'
  } catch {
    return false
  }
}

function drawBoard(canvas, game, now) {
  const context = canvas?.getContext('2d')
  if (!context) return
  const ratio = window.devicePixelRatio || 1
  const { width: cssWidth, height: cssHeight } = canvas.getBoundingClientRect()
  if (canvas.width !== Math.round(cssWidth * ratio)) canvas.width = Math.round(cssWidth * ratio)
  if (canvas.height !== Math.round(cssHeight * ratio)) canvas.height = Math.round(cssHeight * ratio)
  const cell = Math.min(canvas.width / MATRIX_RULES.columns, canvas.height / ROWS)
  const left = (canvas.width - cell * MATRIX_RULES.columns) / 2
  const top = (canvas.height - cell * ROWS) / 2
  const gap = Math.max(1, cell * 0.08)
  context.fillStyle = COLORS.night
  context.fillRect(0, 0, canvas.width, canvas.height)
  const block = (column, row, span, color, alpha = 1) => {
    context.globalAlpha = alpha
    context.fillStyle = color
    for (let i = 0; i < span; i += 1)
      context.fillRect(
        left + (column + i) * cell + gap / 2,
        top + row * cell + gap / 2,
        cell - gap,
        cell - gap,
      )
    context.globalAlpha = 1
  }
  for (let row = 0; row < ROWS; row += 1) block(0, row, MATRIX_RULES.columns, COLORS.grid)
  // Row 15 (bottom) is the foundation; level n is drawn on row 15 - n.
  block(MATRIX_RULES.foundation_x, ROWS - 1, MATRIX_RULES.initial_width, COLORS.cloud)
  const round = game.round
  if (!round) return
  round.trace.forEach((placement, index) => {
    const row = ROWS - 2 - index
    if (placement.overlap)
      block(Math.max(placement.x, placement.support), row, placement.overlap, COLORS.lime)
    else block(placement.x, row, placement.width, COLORS.cloud, 0.35)
  })
  if (game.phase === 'playing' && !round.ended) {
    const elapsed = Math.max(0, now - game.startClock)
    block(positionAt(round, elapsed), ROWS - 2 - round.count, round.width, COLORS.lime, 0.85)
  }
}

export default function GameScreen() {
  const device = useRef(null)
  if (!device.current) device.current = new ScreenDevice()
  const canvas = useRef(null)
  const game = useRef({
    phase: 'idle',
    round: null,
    sessionId: null,
    startClock: 0,
    countdownAt: 0,
  })
  const button = useRef(null)
  const [paired, setPaired] = useState(device.current.paired)
  const [view, setView] = useState({ phase: 'idle', score: 0, seconds: 60, step: 0, won: false })
  const [server, setServer] = useState({
    ok: false,
    message: 'Connecting…',
    round: null,
    held: false,
  })
  const [buttonState, setButtonState] = useState({
    state: serialSupported() ? 'none' : 'unsupported',
  })
  const [keyboard, setKeyboard] = useState(() => readFlag(KEYBOARD_KEY))
  const [menu, setMenu] = useState(false)
  const [lobby, setLobby] = useState(null)
  const [saved, setSaved] = useState('')
  const [secondTab, setSecondTab] = useState(false)

  const show = useCallback((patch) => setView((current) => ({ ...current, ...patch })), [])

  // One game screen tab per browser: two tabs would race the same journal.
  useEffect(() => {
    if (!navigator.locks) return undefined
    let release
    let cancelled = false
    let retry
    const held = new Promise((resolve) => (release = resolve))
    // Retry briefly: a reload or remount frees the previous holder a moment later.
    const attempt = (tries) =>
      navigator.locks.request('smb-game-screen', { ifAvailable: true }, (lock) => {
        if (lock) {
          if (!cancelled) setSecondTab(false)
          return held
        }
        if (cancelled) return undefined
        if (tries > 0) retry = setTimeout(() => void attempt(tries - 1), 250)
        else setSecondTab(true)
        return undefined
      })
    void attempt(8)
    return () => {
      cancelled = true
      clearTimeout(retry)
      release()
    }
  }, [])

  // Keep the laptop screen on while this page is visible.
  useEffect(() => {
    let lock = null
    const acquire = async () => {
      try {
        if (document.visibilityState === 'visible')
          lock = await navigator.wakeLock?.request('screen')
      } catch {
        /* not allowed right now; Windows power settings are the backup */
      }
    }
    void acquire()
    document.addEventListener('visibilitychange', acquire)
    return () => {
      document.removeEventListener('visibilitychange', acquire)
      void lock?.release()
    }
  }, [])

  const finish = useCallback(
    (now) => {
      const current = game.current
      const round = current.round
      const result = toResult(round, crypto.randomUUID())
      try {
        device.current.saveTerminal(current.sessionId, result)
      } catch (error) {
        setSaved(error.message)
      }
      playSound(round.won ? 'win' : 'loss')
      current.phase = 'result'
      current.resultUntil = now + RESULT_MS
      show({ phase: 'result', score: round.score, won: round.won })
      setSaved('Saving the score…')
      device.current
        .reportTerminal(current.sessionId)
        .then((reply) =>
          setSaved(
            reply?.reviewRequired
              ? 'Held for the operator to review.'
              : 'Score saved to the leaderboard.',
          ),
        )
        .catch(() => setSaved('Score kept on this laptop; it will upload when the server is back.'))
    },
    [show],
  )

  const onPress = useCallback(
    (at) => {
      const current = game.current
      if (current.phase === 'idle') {
        const round = device.current.playableRound()
        if (!device.current.canStart(round)) return
        unlockAudio()
        current.phase = 'countdown'
        current.countdownAt = at
        current.sessionId = round.sessionId
        current.round = createRound()
        setSaved('')
        show({ phase: 'countdown', step: 3, score: 0, seconds: 60 })
        playSound('countdown')
      } else if (current.phase === 'playing' && at >= current.startClock) {
        const round = current.round
        if (press(round, at - current.startClock) && !round.ended) playSound('place')
        show({ score: round.score })
        if (round.ended) finish(at)
      }
    },
    [finish, show],
  )

  // Animation loop: countdown, timing, timeout and drawing.
  useEffect(() => {
    let frame
    const loop = () => {
      const now = pageClock()
      const current = game.current
      if (current.phase === 'countdown') {
        const passed = now - current.countdownAt
        if (passed >= COUNTDOWN_MS) {
          const round = device.current.markStarted(current.sessionId)
          current.startClock = device.current.saved.epochMs + round.startUptimeMs
          current.phase = 'playing'
          show({ phase: 'playing', step: 0 })
          device.current
            .sendStarted(current.sessionId)
            .then((reply) => {
              if (reply?.reviewRequired && game.current.sessionId === current.sessionId) {
                game.current.phase = 'idle'
                game.current.round = null
                show({ phase: 'idle' })
                setServer((s) => ({ ...s, held: true }))
              }
            })
            .catch(() => {}) // retried by the sync loop and before the result
        } else {
          const step = 3 - Math.floor(passed / COUNTDOWN_STEP_MS)
          if (step !== view.step) show({ step })
        }
      } else if (current.phase === 'playing') {
        const elapsed = now - current.startClock
        if (!current.round.ended && elapsed >= MATRIX_RULES.round_limit_ms) timeout(current.round)
        if (current.round.ended) finish(now)
        else {
          const seconds = Math.max(0, Math.ceil((MATRIX_RULES.round_limit_ms - elapsed) / 1000))
          if (seconds !== view.seconds) show({ seconds })
        }
      } else if (current.phase === 'result' && now >= current.resultUntil) {
        current.phase = 'idle'
        current.round = null
        current.sessionId = null
        show({ phase: 'idle' })
      }
      drawBoard(canvas.current, current, now)
      frame = requestAnimationFrame(loop)
    }
    frame = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(frame)
  }, [finish, show, view.step, view.seconds])

  // Server sync every second: heartbeat, commands, and any unsent journal event.
  useEffect(() => {
    if (!paired || secondTab) return undefined
    let stopped = false
    let busy = false
    const tick = async () => {
      if (busy || stopped) return
      busy = true
      const phase = game.current.phase
      try {
        const data = await device.current.sync(
          phase === 'countdown' || phase === 'playing' ? 'playing' : 'ready',
        )
        if (stopped) return
        const round = device.current.playableRound()
        setServer({
          ok: true,
          message: '',
          held: Boolean(data.reviewRequired),
          round: round ? { sessionId: round.sessionId, expiresAt: round.expiresAt } : null,
        })
      } catch (error) {
        if (stopped) return
        if (error.status === 401) {
          device.current.unpair()
          setPaired(false)
        }
        setServer((s) => ({ ...s, ok: false, message: error.message }))
      } finally {
        busy = false
      }
    }
    void tick()
    const timer = setInterval(tick, 1000)
    return () => {
      stopped = true
      clearInterval(timer)
    }
  }, [paired, secondTab])

  // Queue size for the waiting screen (public lobby numbers only).
  useEffect(() => {
    let stopped = false
    const load = () =>
      api('/player/lobby')
        .then((data) => !stopped && setLobby(data))
        .catch(() => {})
    void load()
    const timer = setInterval(load, 5000)
    return () => {
      stopped = true
      clearInterval(timer)
    }
  }, [])

  // The arcade button over USB, reconnecting to a port this browser was already allowed.
  useEffect(() => {
    if (!serialSupported()) return undefined
    const bridge = new SerialButton({ onPress, onStatus: setButtonState, clock: pageClock })
    button.current = bridge
    void bridge.reconnect().catch(() => {})
    return () => void bridge.stop()
  }, [onPress])

  // Keyboard fallback (Space or Enter), off unless the operator switches it on.
  useEffect(() => {
    if (!keyboard) return undefined
    const onKey = (event) => {
      if (event.repeat || (event.code !== 'Space' && event.key !== 'Enter')) return
      if (event.target.closest?.('input, textarea, select')) return
      // Space must play, not press whichever operator button still has focus.
      event.preventDefault()
      if (document.activeElement instanceof HTMLElement) document.activeElement.blur()
      onPress(performance.timeOrigin + event.timeStamp)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [keyboard, onPress])

  function toggleKeyboard() {
    const next = !keyboard
    setKeyboard(next)
    try {
      window.localStorage.setItem(KEYBOARD_KEY, next ? '1' : '0')
    } catch {
      /* the setting just won't be remembered */
    }
  }

  async function connectButton() {
    unlockAudio()
    try {
      await button.current?.choose()
    } catch (error) {
      if (error?.name !== 'NotFoundError') setButtonState({ state: 'error', detail: error.message })
    }
  }

  function fullScreen() {
    unlockAudio()
    if (document.fullscreenElement) void document.exitFullscreen()
    else void document.documentElement.requestFullscreen?.()
  }

  function unpair() {
    device.current.unpair()
    setPaired(false)
    setMenu(false)
  }

  if (!paired)
    return (
      <ScreenMessage title="This laptop is not the game screen yet">
        An administrator signs in on this laptop and chooses Settings → Game screen → Use this
        laptop as the game screen.
        <Link to="/admin/login" className={screenButton + ' tw:mt-6'}>
          Administrator sign-in
        </Link>
      </ScreenMessage>
    )
  if (secondTab)
    return (
      <ScreenMessage title="The game screen is already open">
        Use the other tab or window. Only one game screen can run in this browser.
      </ScreenMessage>
    )

  const called = server.round && view.phase === 'idle'
  const buttonLabel = {
    connected: 'Button connected',
    none: 'Button not connected',
    lost: 'Button unplugged',
    error: 'Button error',
    unsupported: 'No Web Serial: use Chrome or Edge',
  }[buttonState.state]

  return (
    <main
      className="tw:fixed tw:inset-0 tw:z-[60] tw:grid tw:grid-cols-1 tw:bg-night tw:text-cloud tw:lg:grid-cols-[minmax(0,1fr)_minmax(320px,30vw)] tw:font-sans"
      onClick={unlockAudio}
    >
      <h1 className="tw:sr-only">Stack Moko Baby game screen</h1>
      <div className="tw:relative tw:flex tw:min-h-0 tw:items-center tw:justify-center tw:p-[3vh]">
        <canvas
          ref={canvas}
          className="tw:aspect-square tw:h-full tw:max-h-[94vh] tw:max-w-full"
          role="img"
          aria-label={`Stacking board, score ${view.score}`}
        />
        {view.phase === 'countdown' && (
          <Overlay>
            <span
              key={view.step}
              className="tw:text-[min(30vh,22vw)] tw:font-black tw:leading-none tw:text-lime tw:motion-safe:animate-pop-in"
            >
              {view.step}
            </span>
          </Overlay>
        )}
        {view.phase === 'result' && (
          <Overlay>
            <div className="tw:rounded-[28px] tw:bg-night/85 tw:px-[6vw] tw:py-[4vh] tw:text-center tw:motion-safe:animate-modal-in">
              <p className="tw:m-0 tw:text-[min(9vh,7vw)] tw:font-black tw:leading-none tw:text-lime">
                {view.won ? 'YOU WIN!' : 'GAME OVER'}
              </p>
              <p className="tw:mt-[2vh] tw:mb-0 tw:text-[min(6vh,5vw)] tw:font-bold">
                Score {view.score}
              </p>
              <p className="tw:mt-[2vh] tw:mb-0 tw:text-[18px] tw:text-cloud/70" role="status">
                {saved}
              </p>
            </div>
          </Overlay>
        )}
      </div>

      <aside className="tw:flex tw:min-h-0 tw:flex-col tw:gap-6 tw:border-l tw:border-solid tw:border-white/10 tw:p-[4vh] tw:max-lg:border-l-0">
        <div className="tw:flex tw:items-center tw:justify-between tw:gap-3">
          <span className="tw:text-[22px] tw:font-black tw:tracking-tight">
            stack moko baby<span className="tw:text-lime">.</span>
          </span>
          <button
            type="button"
            className="tw:rounded-full tw:border tw:border-solid tw:border-white/20 tw:bg-transparent tw:px-4 tw:py-2 tw:text-[14px] tw:text-cloud tw:cursor-pointer"
            aria-expanded={menu}
            onClick={() => setMenu(!menu)}
          >
            Operator
          </button>
        </div>

        {view.phase === 'playing' || view.phase === 'countdown' ? (
          <div className="tw:grid tw:grid-cols-2 tw:gap-4">
            <Stat label="Score" value={view.score} />
            <Stat label="Time" value={view.phase === 'countdown' ? 60 : view.seconds} />
            <p className="tw:col-span-2 tw:m-0 tw:text-[min(5vh,40px)] tw:font-black tw:text-lime">
              {view.phase === 'countdown' ? 'Get ready…' : 'GO! Press to stack'}
            </p>
          </div>
        ) : view.phase === 'result' ? (
          <Stat label="Final score" value={view.score} />
        ) : called ? (
          <div className="tw:motion-safe:animate-fade-up">
            <p className="tw:m-0 tw:text-[14px] tw:font-bold tw:uppercase tw:tracking-[0.12em] tw:text-lime">
              Player called
            </p>
            <p className="tw:mt-3 tw:mb-0 tw:text-[min(6vh,46px)] tw:font-black tw:leading-[1.05]">
              Your turn! Press the button to start.
            </p>
            <Deadline expiresAt={server.round.expiresAt} />
          </div>
        ) : (
          <div>
            <p className="tw:m-0 tw:text-[14px] tw:font-bold tw:uppercase tw:tracking-[0.12em] tw:text-lime">
              {server.held ? 'Round held' : 'Waiting for the next player'}
            </p>
            <p className="tw:mt-3 tw:mb-0 tw:text-[min(5vh,40px)] tw:font-black tw:leading-[1.1]">
              {server.held
                ? 'The operator is checking the last round.'
                : 'Scan the QR at the booth to join the line.'}
            </p>
            {lobby && (
              <p className="tw:mt-4 tw:mb-0 tw:text-[18px] tw:text-cloud/70">
                {lobby.inLine} in line
                {lobby.bestToday != null ? ` · best today ${lobby.bestToday}` : ''}
              </p>
            )}
          </div>
        )}

        <p className="tw:m-0 tw:text-[15px] tw:leading-[1.6] tw:text-cloud/70">
          Stack all 15 rows in 60 seconds. Press when the moving row sits on the one below; only the
          overlap stays.
        </p>

        <div
          className="tw:mt-auto tw:grid tw:gap-2 tw:text-[14px]"
          role="status"
          aria-live="polite"
        >
          <StatusLine ok={server.ok} label={server.ok ? 'Server connected' : server.message} />
          <StatusLine
            ok={buttonState.state === 'connected' || keyboard}
            label={
              keyboard && buttonState.state !== 'connected'
                ? 'Keyboard fallback on (Space)'
                : buttonLabel
            }
          />
        </div>

        {menu && (
          <div className="tw:grid tw:gap-2 tw:rounded-2xl tw:border tw:border-solid tw:border-white/15 tw:p-4 tw:motion-safe:animate-panel-in">
            <button type="button" className={screenButton} onClick={() => void connectButton()}>
              Connect button (USB)
            </button>
            <button type="button" className={screenButtonGhost} onClick={fullScreen}>
              Full screen
            </button>
            <button
              type="button"
              className={screenButtonGhost}
              aria-pressed={keyboard}
              onClick={toggleKeyboard}
            >
              Keyboard fallback: {keyboard ? 'on' : 'off'}
            </button>
            <button type="button" className={screenButtonGhost} onClick={unpair}>
              Unpair this laptop
            </button>
            {buttonState.detail && <p className="tw:m-0 tw:text-cloud/70">{buttonState.detail}</p>}
          </div>
        )}
      </aside>
    </main>
  )
}

const screenButton =
  'tw:inline-flex tw:items-center tw:justify-center tw:rounded-full tw:border-0 tw:bg-lime tw:px-5 tw:py-3 tw:text-[15px] tw:font-bold tw:text-night tw:no-underline tw:cursor-pointer'
const screenButtonGhost =
  'tw:inline-flex tw:items-center tw:justify-center tw:rounded-full tw:border tw:border-solid tw:border-white/20 tw:bg-transparent tw:px-5 tw:py-3 tw:text-[15px] tw:font-bold tw:text-cloud tw:cursor-pointer'

function Overlay({ children }) {
  return (
    <div className="tw:pointer-events-none tw:absolute tw:inset-0 tw:flex tw:items-center tw:justify-center">
      {children}
    </div>
  )
}

function Stat({ label, value }) {
  return (
    <div>
      <p className="tw:m-0 tw:text-[14px] tw:font-bold tw:uppercase tw:tracking-[0.12em] tw:text-cloud/60">
        {label}
      </p>
      <p className="tw:m-0 tw:text-[min(14vh,110px)] tw:font-black tw:leading-none tw:tabular-nums">
        {value}
      </p>
    </div>
  )
}

function StatusLine({ ok, label }) {
  return (
    <span className="tw:flex tw:items-center tw:gap-2">
      <span
        aria-hidden="true"
        className={`tw:size-2.5 tw:rounded-full ${ok ? 'tw:bg-lime' : 'tw:bg-cloud/40'}`}
      />
      {label}
    </span>
  )
}

function Deadline({ expiresAt }) {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(timer)
  }, [])
  const left = Math.max(0, Math.floor((Date.parse(expiresAt) - now) / 1000))
  if (!expiresAt || Number.isNaN(left)) return null
  return (
    <p className="tw:mt-4 tw:mb-0 tw:text-[18px] tw:text-cloud/70">
      Start within {Math.floor(left / 60)}:{String(left % 60).padStart(2, '0')}
    </p>
  )
}

function ScreenMessage({ title, children }) {
  return (
    <main className="tw:fixed tw:inset-0 tw:z-[60] tw:flex tw:items-center tw:justify-center tw:bg-night tw:p-8 tw:text-cloud">
      <div className="tw:max-w-[560px] tw:text-center">
        <h1 className="tw:m-0 tw:text-[32px] tw:font-black tw:leading-tight">{title}</h1>
        <p className="tw:mt-4 tw:text-[17px] tw:leading-[1.6] tw:text-cloud/75">{children}</p>
      </div>
    </main>
  )
}
