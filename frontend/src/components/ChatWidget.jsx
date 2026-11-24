import { useEffect, useRef, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useApp } from '../state/AppContext'
import PlayerAssistant from './PlayerAssistant'
import RobotIcon from './RobotIcon'
import { OPEN_CHAT_EVENT } from './SiteSections'
import '../styles/chat-widget.css'

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
    <div className="chat-widget">
      {open && (
        <section
          ref={panel}
          className="chat-panel"
          role="dialog"
          aria-modal="false"
          aria-labelledby="chat-panel-title"
          onKeyDown={(event) => {
            if (event.key === 'Escape') closeChat()
          }}
        >
          <header className="chat-panel-head">
            <RobotIcon size={36} />
            <span>
              <strong id="chat-panel-title">Stack Intelligence</strong>
              <small>About the game · English or Taglish</small>
            </span>
            <button
              type="button"
              className="chat-close"
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
        <div className="chat-nudge">
          <button type="button" className="chat-nudge-text" onClick={openChat}>
            Hi! Questions while you wait? <strong>Ask me.</strong>
          </button>
          <button
            type="button"
            className="chat-nudge-close"
            aria-label="Dismiss greeting"
            onClick={dismissNudge}
          >
            <i className="fa-solid fa-xmark" aria-hidden="true" />
          </button>
        </div>
      )}
      <div className="chat-launcher-row">
        {!open && (
          <span className="chat-label" aria-hidden="true">
            Ask me
          </span>
        )}
        <button
          ref={launcher}
          type="button"
          className="chat-launcher"
          aria-label={open ? 'Close Stack Intelligence' : 'Open Stack Intelligence'}
          aria-expanded={open}
          onClick={() => (open ? closeChat() : openChat())}
        >
          {open ? (
            <i className="fa-solid fa-chevron-down" aria-hidden="true" />
          ) : (
            <RobotIcon size={42} blink />
          )}
          {!open && nudge && !quiet && <span className="chat-dot" aria-hidden="true" />}
        </button>
      </div>
    </div>
  )
}
