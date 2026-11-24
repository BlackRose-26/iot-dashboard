import { useEffect, useId, useRef, useState } from 'react'
import { api } from '../state/api'

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
  embedded = false,
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

  const v = embedded ? embeddedStyles : cardStyles
  return (
    <section
      className={v.card}
      {...(embedded ? { 'aria-label': title } : { 'aria-labelledby': `${inputId}-title` })}
    >
      {!embedded && (
        <div className="tw:flex tw:items-center tw:gap-3">
          <span
            className="tw:w-11 tw:h-11 tw:flex-none tw:rounded-[22px] tw:bg-ink tw:text-lime tw:grid tw:place-items-center tw:text-[18px]"
            aria-hidden="true"
          >
            <i className="fa-solid fa-comment-dots" />
          </span>
          <div>
            <h2
              id={`${inputId}-title`}
              className="tw:m-0 tw:text-[17px] tw:font-extrabold tw:tracking-[-0.2px]"
            >
              {title}
            </h2>
            {intro && <p className="tw:mt-0.5 tw:mb-0 tw:text-[13px] tw:text-note">{intro}</p>}
          </div>
        </div>
      )}
      <div
        className={v.log}
        ref={log}
        role="log"
        aria-live="polite"
        aria-label="Conversation with Stack Intelligence"
        tabIndex={0}
      >
        {shown.map((message) => (
          <div
            key={message.id}
            className={`${bubble} ${message.role === 'user' ? userBubble : v.bot} tw:motion-safe:animate-fade-in`}
          >
            {message.text}
            {message.source && (
              <>
                <br />
                <span className={v.source}>{message.source}</span>
              </>
            )}
          </div>
        ))}
        {pending && (
          <div className={v.thinking} aria-label="Stack Intelligence is answering">
            <span className={dot} />
            <span className={`${dot} tw:[animation-delay:150ms]`} />
            <span className={`${dot} tw:[animation-delay:300ms]`} />
          </div>
        )}
      </div>
      {error && (
        <p className="tw:m-0 tw:text-[13px] tw:text-danger" role="alert">
          {error}
        </p>
      )}
      {chips.length > 0 && (
        <div className="tw:flex tw:flex-wrap tw:gap-2" aria-label="Suggested questions">
          {chips.map((label) => (
            <button
              key={label}
              type="button"
              className={v.chip}
              disabled={pending}
              onClick={() => void ask(label)}
            >
              {label}
            </button>
          ))}
        </div>
      )}
      <form
        className={v.input}
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
          className="tw:flex-1 tw:min-w-0 tw:border-0 tw:bg-transparent tw:text-[15px] tw:font-medium tw:text-ink tw:min-h-10 tw:focus:outline-none"
          value={draft}
          maxLength={300}
          autoComplete="off"
          placeholder="Ask about the game…"
          onChange={(event) => setDraft(event.target.value)}
        />
        <button
          type="submit"
          className="tw:w-11 tw:h-11 tw:flex-none tw:border-0 tw:rounded-[22px] tw:bg-ink tw:text-lime tw:cursor-pointer tw:text-[16px] tw:disabled:opacity-50 tw:disabled:cursor-default tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-ink tw:focus-visible:outline-offset-2"
          aria-label="Send question"
          disabled={pending || !draft.trim()}
        >
          <i className="fa-solid fa-arrow-right" aria-hidden="true" />
        </button>
      </form>
      <p className={v.note}>
        Read-only: it can’t change your place in line. Don’t type your student ID here.
      </p>
    </section>
  )
}

const bubble = 'tw:max-w-[88%] tw:text-[14px] tw:leading-normal tw:px-3.5 tw:py-3 tw:wrap-anywhere'
const userBubble = 'tw:self-end tw:bg-ink tw:text-white tw:rounded-[22px_22px_6px_22px]'
const dot = 'tw:w-2 tw:h-2 tw:rounded tw:bg-muted tw:opacity-35 tw:motion-safe:animate-typing'
const chipBase =
  'tw:min-h-11 tw:rounded-full tw:text-ink tw:px-4 tw:py-2.5 tw:text-[13px] tw:font-semibold tw:cursor-pointer tw:hover:bg-lime tw:disabled:cursor-default tw:disabled:opacity-60 tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-ink tw:focus-visible:outline-offset-2 tw:motion-safe:transition-colors tw:motion-safe:duration-[120ms]'
const logBase =
  'tw:flex tw:flex-col tw:gap-2.5 tw:overflow-y-auto tw:p-0.5 tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-ink tw:focus-visible:outline-offset-[3px] tw:focus-visible:rounded-[18px]'
const thinkingBase =
  'tw:self-start tw:flex tw:gap-1.5 tw:rounded-[22px_22px_22px_6px] tw:px-4 tw:py-3.5'
// The standalone card (blue tint) and the version inside the robot chat panel.
const cardStyles = {
  card: 'tw:bg-[var(--blue-soft)] tw:rounded-[32px] tw:p-[22px] tw:flex tw:flex-col tw:gap-3.5 tw:text-ink',
  log: `${logBase} tw:max-h-[340px]`,
  bot: 'tw:self-start tw:bg-surface tw:rounded-[22px_22px_22px_6px]',
  source:
    'tw:inline-block tw:mt-2 tw:text-[11px] tw:font-bold tw:text-note tw:bg-[var(--blue-soft)] tw:rounded-full tw:px-2.5 tw:py-[3px]',
  thinking: `${thinkingBase} tw:bg-surface`,
  chip: `${chipBase} tw:border-0 tw:bg-surface`,
  input:
    'tw:flex tw:items-center tw:gap-2 tw:bg-surface tw:rounded-full tw:py-1.5 tw:pr-1.5 tw:pl-[18px]',
  note: 'tw:m-0 tw:text-[12px] tw:leading-normal tw:text-note',
}
const embeddedStyles = {
  card: 'tw:bg-transparent tw:rounded-none tw:p-3.5 tw:flex tw:flex-col tw:flex-1 tw:min-h-0 tw:gap-2.5 tw:text-ink',
  log: `${logBase} tw:flex-1 tw:min-h-0`,
  bot: 'tw:self-start tw:bg-cloud tw:border-[1.5px] tw:border-solid tw:border-night/16 tw:rounded-[22px_22px_22px_6px]',
  source:
    'tw:inline-block tw:mt-2 tw:text-[11px] tw:font-bold tw:text-note tw:bg-transparent tw:border-[1.5px] tw:border-solid tw:border-night/30 tw:rounded-full tw:px-2.5 tw:py-[3px]',
  thinking: `${thinkingBase} tw:bg-cloud tw:border-[1.5px] tw:border-solid tw:border-night/16`,
  chip: `${chipBase} tw:bg-cloud tw:border-[1.5px] tw:border-solid tw:border-ink`,
  input:
    'tw:flex tw:items-center tw:gap-2 tw:bg-cloud tw:border-[1.5px] tw:border-solid tw:border-night/30 tw:rounded-full tw:py-1.5 tw:pr-1.5 tw:pl-[18px]',
  note: 'tw:m-0 tw:text-[11px] tw:leading-normal tw:text-note',
}
