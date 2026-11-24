import { useEffect, useId, useRef, useState } from 'react'
import { api } from '../state/api'
import '../styles/player-assistant.css'

// Stack Intelligence for players. The server answers from checked templates filled with live
// facts (rules, the line, today's scores, this player's own ticket); it stores nothing and
// cannot change the queue. Questions that look like a student ID are refused server-side.
const KEEP = 20

export default function PlayerAssistant({
  title = 'Ask Stack Intelligence',
  intro,
  greeting,
  suggestions: initialSuggestions = [],
  compact = false,
}) {
  const [messages, setMessages] = useState(() =>
    greeting ? [{ id: 'greeting', role: 'bot', text: greeting }] : [],
  )
  const [suggestions, setSuggestions] = useState(initialSuggestions)
  const [asked, setAsked] = useState([])
  const [draft, setDraft] = useState('')
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const log = useRef(null)
  const inputId = useId()
  const counter = useRef(0)

  // Suggestions follow the ticket (waiting → called → finished) until the player asks.
  const initialKey = initialSuggestions.join('|')
  useEffect(() => {
    setSuggestions(initialKey ? initialKey.split('|') : [])
  }, [initialKey])

  useEffect(() => {
    const element = log.current
    if (element) element.scrollTop = element.scrollHeight
  }, [messages, pending])

  async function ask(question) {
    const text = question.trim()
    if (!text || pending) return
    const id = ++counter.current
    setError('')
    setDraft('')
    setPending(true)
    setAsked((list) => [...list, text])
    setMessages((list) => [...list, { id: `q${id}`, role: 'user', text }].slice(-KEEP))
    try {
      const reply = await api('/player/assistant', { method: 'POST', body: { question: text } })
      setMessages((list) =>
        [...list, { id: `a${id}`, role: 'bot', text: reply.answer, source: reply.source }].slice(
          -KEEP,
        ),
      )
      if (reply.suggestions?.length) setSuggestions(reply.suggestions)
    } catch (failure) {
      setError(failure.message || 'Stack Intelligence is unavailable right now.')
    } finally {
      setPending(false)
    }
  }

  const chips = suggestions.filter((label) => !asked.includes(label))
  const shown = compact ? messages.slice(-2) : messages

  return (
    <section className="pa-card" aria-labelledby={`${inputId}-title`}>
      <div className="pa-head">
        <span className="pa-emblem" aria-hidden="true">
          <i className="fa-solid fa-comment-dots" />
        </span>
        <div>
          <h2 id={`${inputId}-title`}>{title}</h2>
          {intro && <p>{intro}</p>}
        </div>
      </div>
      <div
        className="pa-log"
        ref={log}
        role="log"
        aria-live="polite"
        aria-label="Conversation with Stack Intelligence"
        tabIndex={0}
      >
        {shown.map((message) => (
          <div key={message.id} className={`pa-bubble ${message.role}`}>
            {message.text}
            {message.source && (
              <>
                <br />
                <span className="pa-source">{message.source}</span>
              </>
            )}
          </div>
        ))}
        {pending && (
          <div className="pa-thinking" aria-label="Stack Intelligence is answering">
            <span />
            <span />
            <span />
          </div>
        )}
      </div>
      {error && (
        <p className="pa-error" role="alert">
          {error}
        </p>
      )}
      {chips.length > 0 && (
        <div className="pa-chips" aria-label="Suggested questions">
          {chips.map((label) => (
            <button
              key={label}
              type="button"
              className="pa-chip"
              disabled={pending}
              onClick={() => void ask(label)}
            >
              {label}
            </button>
          ))}
        </div>
      )}
      <form
        className="pa-input"
        onSubmit={(event) => {
          event.preventDefault()
          void ask(draft)
        }}
      >
        <label htmlFor={inputId} className="sr-only">
          Ask Stack Intelligence a question
        </label>
        <input
          id={inputId}
          value={draft}
          maxLength={300}
          autoComplete="off"
          placeholder="Ask about the game…"
          onChange={(event) => setDraft(event.target.value)}
        />
        <button
          type="submit"
          className="pa-send"
          aria-label="Send question"
          disabled={pending || !draft.trim()}
        >
          <i className="fa-solid fa-arrow-right" aria-hidden="true" />
        </button>
      </form>
      <p className="pa-note">
        Read-only: it can’t change your place in line. Don’t type your student ID here.
      </p>
    </section>
  )
}

const cabinetLabels = {
  ready: 'Cabinet ready',
  busy: 'Round in progress',
  offline: 'Cabinet reconnecting',
}

export function LobbyStatus() {
  const [lobby, setLobby] = useState(null)
  useEffect(() => {
    let current = true
    const load = () =>
      api('/player/lobby')
        .then((data) => current && setLobby(data))
        .catch(() => current && setLobby(null))
    void load()
    const timer = setInterval(load, 15000)
    return () => {
      current = false
      clearInterval(timer)
    }
  }, [])
  if (!lobby) return null
  const paused = !lobby.admissionsOpen
  const state = paused ? 'paused' : lobby.cabinet
  return (
    <div className="lobby-strip" role="status" aria-live="polite">
      <span className="count">
        <small>Right now</small>
        <strong>{lobby.inLine === 1 ? '1 in line' : `${lobby.inLine} in line`}</strong>
      </span>
      <span className="state">
        <b>
          <span className={`lobby-dot ${state}`} aria-hidden="true" />
          {paused ? 'Line paused' : cabinetLabels[lobby.cabinet] || 'Cabinet'}
        </b>
        <small>
          {paused
            ? 'Joining reopens soon'
            : lobby.inLine
              ? `About ${Math.max(1, lobby.waitMinutes)} min wait`
              : 'No wait right now'}
        </small>
      </span>
    </div>
  )
}
