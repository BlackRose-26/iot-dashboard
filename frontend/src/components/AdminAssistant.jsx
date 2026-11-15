import { useEffect, useRef, useState } from 'react'

const suggestions = [
  {
    icon: 'table-columns',
    label: 'Event overview',
    question: 'Give me an overview of the whole event.',
  },
  {
    icon: 'microchip',
    label: 'IoT & cabinet',
    question: 'What is the cabinet’s connection and readiness status?',
  },
  {
    icon: 'users',
    label: 'Player activity',
    question: 'How many players registered and completed a round?',
  },
  { icon: 'list-ol', label: 'Queue', question: 'What is happening in the queue right now?' },
  { icon: 'trophy', label: 'Scores & results', question: 'How are scores and wins distributed?' },
  {
    icon: 'chart-line',
    label: 'Trends',
    question: 'Which levels are players finding most difficult?',
  },
]

function Symbol({ name }) {
  return <i className={`fa-solid fa-${name}`} aria-hidden="true" />
}

export default function AdminAssistant() {
  const [open, setOpen] = useState(false)
  const [draft, setDraft] = useState('')
  const [messages, setMessages] = useState([])
  const launcher = useRef(null)
  const input = useRef(null)
  const transcript = useRef(null)
  const nextId = useRef(0)
  const returnFocus = useRef(false)

  useEffect(() => {
    if (open) input.current?.focus({ preventScroll: true })
    else if (returnFocus.current) {
      launcher.current?.focus()
      returnFocus.current = false
    }
  }, [open])

  useEffect(() => {
    if (open && transcript.current) {
      transcript.current.scrollTop = messages.length ? transcript.current.scrollHeight : 0
    }
  }, [open, messages])

  function minimize() {
    returnFocus.current = true
    setOpen(false)
  }

  function submit(event) {
    event.preventDefault()
    const question = draft.trim()
    if (!question) return
    const userMessage = { id: ++nextId.current, role: 'user', text: question }
    const previewReply = {
      id: ++nextId.current,
      role: 'assistant',
      text: 'Live analysis is not connected in this design preview. Once connected, I’ll help you explore your event, cabinet health, player activity, queues and results using the available records.',
    }
    setMessages((previous) => [...previous.slice(-18), userMessage, previewReply])
    setDraft('')
    input.current?.focus()
  }

  function chooseQuestion(question) {
    setDraft(question)
    input.current?.focus()
  }

  return (
    <aside
      className={`admin-assistant${open ? ' is-open' : ''}`}
      aria-label="Stack Intelligence assistant"
      onKeyDown={(event) => {
        if (open && event.key === 'Escape') {
          event.stopPropagation()
          minimize()
        }
      }}
    >
      <button
        ref={launcher}
        className="assistant-launcher"
        type="button"
        aria-expanded={open}
        aria-controls="admin-assistant-panel"
        onClick={() => setOpen(true)}
        hidden={open}
      >
        <span className="assistant-emblem">
          <Symbol name="comment-dots" />
        </span>
        <span className="assistant-launcher-copy">
          <strong>
            Stack Intelligence <span className="assistant-preview">Preview</span>
          </strong>
          <span>Ask about your event, IoT, players and scores</span>
        </span>
        <span className="assistant-launcher-action">
          Ask a question <Symbol name="arrow-up" />
        </span>
      </button>

      <section
        id="admin-assistant-panel"
        className="assistant-panel"
        hidden={!open}
        aria-labelledby="assistant-title"
      >
        <header className="assistant-header">
          <span className="assistant-emblem">
            <Symbol name="comment-dots" />
          </span>
          <div className="assistant-heading">
            <h2 id="assistant-title">
              Stack Intelligence <span className="assistant-preview">Preview</span>
            </h2>
            <p>Your event, in conversation.</p>
          </div>
          <button
            type="button"
            className="assistant-tool"
            aria-label="Clear preview conversation"
            title="New conversation"
            onClick={() => {
              setMessages([])
              setDraft('')
              input.current?.focus()
            }}
          >
            <Symbol name="rotate-left" />
          </button>
          <button
            type="button"
            className="assistant-tool"
            aria-label="Minimize assistant"
            title="Minimize"
            onClick={minimize}
          >
            <Symbol name="chevron-down" />
          </button>
        </header>

        <div className="assistant-scope">
          <span>
            <Symbol name="layer-group" /> ACS Carnival
          </span>
          <span>Design preview · Live analysis not connected</span>
        </div>

        <div
          className="assistant-transcript"
          ref={transcript}
          role="region"
          aria-label="Conversation and suggested questions"
          tabIndex={0}
        >
          {!messages.length && (
            <div className="assistant-welcome">
              <span className="eyebrow">THE BIG PICTURE. THE SMALL DETAILS.</span>
              <h3>What would you like to understand?</h3>
              <p>From the cabinet to the leaderboard, bring your questions here.</p>
              <div className="assistant-suggestions" aria-label="Suggested questions">
                {suggestions.map(({ icon, label, question }) => (
                  <button key={label} type="button" onClick={() => chooseQuestion(question)}>
                    <Symbol name={icon} />
                    <span>
                      <strong>{label}</strong>
                      <span>{question}</span>
                    </span>
                    <Symbol name="arrow-up-right-from-square" />
                  </button>
                ))}
              </div>
            </div>
          )}
          <div
            className="assistant-messages"
            role="log"
            aria-label="Preview conversation"
            aria-live="polite"
            aria-relevant="additions"
          >
            {messages.map((message) => (
              <div key={message.id} className={`assistant-message is-${message.role}`}>
                <span className="assistant-message-author">
                  {message.role === 'user' ? 'You' : 'Stack Intelligence · Preview'}
                </span>
                <p>{message.text}</p>
              </div>
            ))}
          </div>
        </div>

        <form className="assistant-composer" onSubmit={submit}>
          <label className="sr-only" htmlFor="assistant-question">
            Ask Stack Intelligence
          </label>
          <div className="assistant-input-wrap">
            <textarea
              id="assistant-question"
              ref={input}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing) {
                  event.preventDefault()
                  event.currentTarget.form.requestSubmit()
                }
              }}
              rows={2}
              maxLength={1000}
              placeholder="Ask about your event…"
              aria-describedby="assistant-composer-help"
            />
            <button
              className="assistant-send"
              type="submit"
              disabled={!draft.trim()}
              aria-label="Send preview message"
              title="Send preview message"
            >
              <Symbol name="arrow-up" />
            </button>
          </div>
          <div className="assistant-composer-meta" id="assistant-composer-help">
            <span>Preview only. Keep student IDs and credentials out of chat.</span>
            <span>{draft.length}/1,000</span>
          </div>
        </form>
      </section>
    </aside>
  )
}
