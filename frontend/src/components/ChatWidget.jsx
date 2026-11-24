import { useEffect, useRef, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useApp } from '../state/AppContext'
import PlayerAssistant from './PlayerAssistant'
import RobotIcon from './RobotIcon'
import { OPEN_CHAT_EVENT } from './SiteSections'

// Stack Intelligence as a sticky robot in the corner of every player page. Closed, it is a
// small robot button (with a one-time greeting); open, a panel with the player assistant.
// Mounted once in App so the conversation survives moving between pages.
const NUDGE_KEY = 'smb-robot-greeted'

function seen() {
  try {
    return sessionStorage.getItem(NUDGE_KEY) === '1'
  } catch {
    return false
  }
}
function remember() {
  try {
    sessionStorage.setItem(NUDGE_KEY, '1')
  } catch {
    // Private browsing: the greeting may show again; nothing else depends on it.
  }
}

export function chatContext(ticket) {
  const status = ticket?.status
  if (status === 'completed')
    return {
      greeting: 'Nice run! Ask me how you did, or how to climb higher next time.',
      suggestions: ['How did I do?', 'Where did I lose it?', 'Tips for next time', 'Play again?'],
    }
  if (status === 'called')
    return {
      greeting: 'It’s your turn! Head to Cabinet 01 and press the big button. Good luck!',
      suggestions: ['What do I do now?', 'Tips for my first game', 'What if I miss my turn?'],
    }
  if (status === 'waiting')
    return {
      greeting: `You’re #${ticket.position ?? 1} in line. Want a quick tip for your first stack?`,
      suggestions: [
        'When is my turn?',
        'Tips for my first game',
        'What if I miss my turn?',
        'Top score today?',
      ],
    }
  if (status === 'playing' || status === 'review')
    return {
      greeting: 'Your round is on! Your result will appear on your ticket.',
      suggestions: ['How do I play?', 'Tips for my first game'],
    }
  return {
    greeting:
      'Hi! I’m Stack Intelligence. Ask me how to play, how long the line is, or today’s top score.',
    suggestions: [
      'How do I play?',
      'How long is the wait?',
      'Top score today?',
      'Is my student ID safe?',
    ],
  }
}

export default function ChatWidget() {
  const { ticket } = useApp()
  const { pathname } = useLocation()
  const [open, setOpen] = useState(false)
  const [nudge, setNudge] = useState(() => !seen())
  const launcher = useRef(null)
  const panel = useRef(null)
  const context = chatContext(ticket)
  // The registration form needs the whole screen on a phone; no greeting bubble there.
  const quiet = pathname === '/register'

  function dismissNudge() {
    setNudge(false)
    remember()
  }
  function openChat() {
    dismissNudge()
    setOpen(true)
  }
  function closeChat() {
    setOpen(false)
    launcher.current?.focus()
  }

  useEffect(() => {
    if (open) panel.current?.querySelector('input')?.focus()
  }, [open])

  // "Ask the robot" buttons elsewhere on the page open the panel.
  useEffect(() => {
    const show = () => {
      setNudge(false)
      remember()
      setOpen(true)
    }
    window.addEventListener(OPEN_CHAT_EVENT, show)
    return () => window.removeEventListener(OPEN_CHAT_EVENT, show)
  }, [])

  return (
    <div className="tw:fixed tw:z-[60] tw:right-[max(20px,env(safe-area-inset-right))] tw:bottom-[max(20px,env(safe-area-inset-bottom))] tw:max-[600px]:right-[max(12px,env(safe-area-inset-right))] tw:max-[600px]:bottom-[max(12px,env(safe-area-inset-bottom))] tw:flex tw:flex-col tw:items-end tw:gap-3 tw:font-sans tw:text-ink">
      {open && (
        <section
          ref={panel}
          className="tw:w-[384px] tw:max-w-[calc(100vw-24px)] tw:h-[560px] tw:max-h-[calc(100dvh-120px)] tw:max-[600px]:h-[min(560px,calc(100dvh-100px))] tw:bg-cloud tw:border-2 tw:border-solid tw:border-ink tw:rounded-[28px] tw:flex tw:flex-col tw:overflow-hidden tw:shadow-[0_18px_40px_rgb(17_19_19/0.22)] tw:origin-bottom-right tw:motion-safe:animate-panel-in"
          role="dialog"
          aria-modal="false"
          aria-labelledby="chat-panel-title"
          onKeyDown={(event) => {
            if (event.key === 'Escape') closeChat()
          }}
        >
          <header className="tw:bg-ink tw:text-cloud tw:flex tw:items-center tw:gap-3 tw:py-3 tw:pr-3 tw:pl-4">
            <RobotIcon size={36} />
            <span className="tw:flex-1 tw:flex tw:flex-col tw:min-w-0">
              <strong id="chat-panel-title" className="tw:text-[16px] tw:font-extrabold">
                Stack Intelligence
              </strong>
              <small className="tw:text-[12px] tw:text-cloud/78">
                About the game · English or Taglish
              </small>
            </span>
            <button
              type="button"
              className="tw:w-11 tw:h-11 tw:flex-none tw:border-0 tw:rounded-[22px] tw:bg-cloud/14 tw:text-cloud tw:cursor-pointer tw:text-[17px] tw:hover:bg-cloud/24 tw:motion-safe:transition-colors tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-lime tw:focus-visible:outline-offset-[3px]"
              aria-label="Close chat"
              onClick={closeChat}
            >
              <i className="fa-solid fa-xmark" aria-hidden="true" />
            </button>
          </header>
          <PlayerAssistant
            key={ticket?.status || 'visitor'}
            embedded
            greeting={context.greeting}
            suggestions={context.suggestions}
          />
        </section>
      )}
      {!open && nudge && !quiet && (
        <div className="tw:max-w-[260px] tw:max-[600px]:hidden tw:bg-cloud tw:border-2 tw:border-solid tw:border-ink tw:rounded-[22px_22px_6px_22px] tw:py-2.5 tw:pr-1.5 tw:pl-3.5 tw:flex tw:gap-1 tw:items-start tw:shadow-[0_10px_24px_rgb(17_19_19/0.16)] tw:origin-bottom-right tw:motion-safe:animate-panel-in tw:[animation-delay:600ms]">
          <button
            type="button"
            className="tw:border-0 tw:bg-transparent tw:py-0.5 tw:px-0 tw:text-left tw:cursor-pointer tw:text-[14px] tw:font-semibold tw:leading-[1.45] tw:text-ink tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-lime tw:focus-visible:outline-offset-[3px]"
            onClick={openChat}
          >
            Hi! Questions while you wait? <strong>Ask me.</strong>
          </button>
          <button
            type="button"
            className="tw:w-8 tw:h-8 tw:flex-none tw:border-0 tw:rounded-2xl tw:bg-transparent tw:cursor-pointer tw:text-ink tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-lime tw:focus-visible:outline-offset-[3px]"
            aria-label="Dismiss greeting"
            onClick={dismissNudge}
          >
            <i className="fa-solid fa-xmark" aria-hidden="true" />
          </button>
        </div>
      )}
      <div className="tw:flex tw:items-center tw:gap-2.5">
        {!open && (
          <span
            className="tw:bg-ink tw:text-cloud tw:font-bold tw:text-[14px] tw:px-3.5 tw:py-2 tw:rounded-full tw:max-[600px]:hidden tw:motion-safe:animate-fade-in tw:[animation-delay:400ms]"
            aria-hidden="true"
          >
            Ask me
          </span>
        )}
        <button
          ref={launcher}
          type="button"
          className="tw:relative tw:w-[68px] tw:h-[68px] tw:max-[600px]:w-[60px] tw:max-[600px]:h-[60px] tw:border-2 tw:border-solid tw:border-ink tw:rounded-full tw:bg-ink tw:text-lime tw:cursor-pointer tw:grid tw:place-items-center tw:text-[22px] tw:shadow-[0_10px_24px_rgb(17_19_19/0.25)] tw:motion-safe:animate-pop-in tw:motion-safe:transition-transform tw:motion-safe:duration-150 tw:motion-safe:hover:-translate-y-0.5 tw:motion-safe:active:scale-95 tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-lime tw:focus-visible:outline-offset-[3px]"
          aria-label={open ? 'Close Stack Intelligence' : 'Open Stack Intelligence'}
          aria-expanded={open}
          onClick={() => (open ? closeChat() : openChat())}
        >
          {open ? (
            <i className="fa-solid fa-chevron-down" aria-hidden="true" />
          ) : (
            <RobotIcon size={42} blink />
          )}
          {!open && nudge && !quiet && (
            <span
              className="tw:absolute tw:-top-0.5 tw:-right-0.5 tw:w-4 tw:h-4 tw:rounded-lg tw:bg-lime tw:border-2 tw:border-solid tw:border-ink"
              aria-hidden="true"
            />
          )}
        </button>
      </div>
    </div>
  )
}
