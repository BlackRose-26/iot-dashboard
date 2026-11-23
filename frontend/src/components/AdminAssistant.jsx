import { useEffect, useRef, useState } from 'react'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import QuestionReview from '../pages/QuestionReview'
import AssistantTrainingReview from './AssistantTrainingReview'
import { useAssistant } from '../state/AssistantContext'

const answerLabels = {
  ok: 'From your event data',
  conversation: 'Let’s chat',
  no_data: 'No matching data',
  refused: 'Request declined',
  needs_clarification: 'Clarification needed',
  unavailable: 'Temporarily unavailable',
}

function Evidence({ response }) {
  const rows = []
  const sources = [response, ...(response.cohorts || [])]
  for (const source of sources) {
    const prefix =
      source === response
        ? ''
        : `${source.scope.source === 'device' ? 'Physical device' : 'Simulator'} · `
    const start = rows.length
    for (const [group, values] of Object.entries(source.evidence || {})) {
      if (group === 'player_scores')
        values.rows?.forEach((row) =>
          rows.push([row.public_code, `${row.score} points · level ${row.highest_level}`]),
        )
      if (group === 'trend')
        values.buckets
          ?.filter((row) => row.games)
          .sort((a, b) => b.games - a.games)
          .slice(0, 5)
          .forEach((row) =>
            rows.push([row.label, `${row.games} games · ${row.players} distinct players`]),
          )
      if (typeof values === 'object' && values && !Array.isArray(values)) {
        for (const [key, value] of Object.entries(values)) {
          if (value === null || ['string', 'number', 'boolean'].includes(typeof value))
            rows.push([
              `${group} · ${key.replaceAll('_', ' ')}`,
              value === null ? 'N/A' : String(value),
            ])
        }
      }
      if (Array.isArray(values))
        values.forEach((row, index) => {
          if (group === 'scores') rows.push([`${row.label} points`, `${row.rounds} rounds`])
          if (group === 'top')
            rows.push([
              `Rank ${index + 1} · ${row.public_code}`,
              `${row.score} points · level ${row.highest_level}`,
            ])
          if (
            group === 'levels' &&
            row.attempts &&
            (source.context?.level == null || source.context.level === row.level)
          )
            rows.push([
              `Level ${row.level}`,
              `${row.failures}/${row.attempts} misses · ${row.rate}% failure · ${row.accuracy == null ? 'N/A' : `${row.accuracy}%`} overlap accuracy`,
            ])
        })
    }
    for (let i = start; i < rows.length; i++) rows[i][0] = prefix + rows[i][0]
  }
  return (
    <details className="assistant-evidence">
      <summary>Details & sources</summary>
      <p>{response.scope_label}</p>
      <p>
        As of {new Date(response.as_of).toLocaleString('en-PH', { timeZone: 'Asia/Manila' })} ·
        Asia/Manila
      </p>
      <dl>
        {rows.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
      {response.claims?.map((claim, index) => (
        <small key={index}>{claim.metric_refs.join(' · ')}</small>
      ))}
      {response.caveats?.map((caveat) => (
        <p key={caveat}>{caveat}</p>
      ))}
    </details>
  )
}

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

export default function AdminAssistant({ onReviewPage = false }) {
  const { admin, refresh } = useApp()
  const {
    useMemory,
    memoryBusy,
    setMemory,
    loadMemory,
    forgetRevision,
    service,
    setService,
    checkConnection,
    pending,
    setPending,
    setCandidate,
  } = useAssistant()
  const [open, setOpen] = useState(false)
  const [reviewMode, setReviewing] = useState(false)
  const reviewing = reviewMode && !onReviewPage
  const [replyForReview, setReplyForReview] = useState(null)
  const [draft, setDraft] = useState('')
  const [messages, setMessages] = useState([])
  const launcher = useRef(null)
  const input = useRef(null)
  const transcript = useRef(null)
  const nextId = useRef(0)
  const returnFocus = useRef(false)
  const [context, setContext] = useState(null)
  const [lastRequest, setLastRequest] = useState(null)
  const activeRequest = useRef(null)
  const restoreMemory = useRef(true)
  const memoryMode = useRef(useMemory)
  useEffect(() => {
    if (memoryMode.current === useMemory) return
    memoryMode.current = useMemory
    cancel()
    restoreMemory.current = false
    setContext(null)
    setLastRequest(null)
  }, [useMemory])

  useEffect(() => {
    if (!open || !useMemory) return
    let active = true
    loadMemory().then((state) => {
      if (active && restoreMemory.current && state?.context) setContext(state.context)
      if (active) restoreMemory.current = false
    })
    return () => {
      active = false
    }
  }, [open, useMemory, loadMemory])
  useEffect(() => {
    if (open) void checkConnection()
  }, [open, checkConnection])
  useEffect(() => {
    if (!forgetRevision) return
    cancel()
    setContext(null)
    setMessages([])
    setLastRequest(null)
    setDraft('')
    restoreMemory.current = false
  }, [forgetRevision])

  useEffect(
    () => () => {
      activeRequest.current?.abort()
    },
    [],
  )

  useEffect(() => {
    if (open && !reviewing && !pending) input.current?.focus({ preventScroll: true })
    else if (!open && returnFocus.current) {
      launcher.current?.focus()
      returnFocus.current = false
    }
  }, [open, reviewing, pending])

  useEffect(() => {
    if (open && transcript.current) {
      transcript.current.scrollTop = messages.length ? transcript.current.scrollHeight : 0
    }
  }, [open, reviewing, messages])

  function minimize() {
    returnFocus.current = true
    setOpen(false)
  }

  async function send(request, retry = false) {
    if (activeRequest.current) return
    const controller = new AbortController()
    activeRequest.current = controller
    setLastRequest(request)
    setPending(true)
    const userMessage = { id: ++nextId.current, role: 'user', text: request.question }
    if (!retry) setMessages((previous) => [...previous.slice(-18), userMessage])
    try {
      const response = await api('/admin/assistant/query', {
        method: 'POST',
        body: request,
        csrf: admin?.csrf,
        signal: controller.signal,
      })
      if (activeRequest.current !== controller) return
      const answer = { id: ++nextId.current, role: 'assistant', text: response.answer, response }
      setMessages((previous) => [...previous.slice(-19), answer])
      if (response.memory) setMemory(response.memory)
      setCandidate(response.review_candidate || null)
      if (response.status === 'conversation') {
        if (response.reason === 'system_context' || response.reason === 'preference') {
          setContext(response.context)
        }
        setLastRequest(null)
        setDraft('')
      } else if (['ok', 'no_data'].includes(response.status)) {
        setContext(response.context)
        setService((state) => ({ ...state, available: true, reason: 'ready' }))
        setLastRequest(null)
        setDraft('')
      } else if (response.reason === 'warming') {
        setService((state) => ({ ...state, available: false, reason: 'warming' }))
        void checkConnection()
      } else if (['refused', 'needs_clarification'].includes(response.status)) {
        setLastRequest(null)
      }
    } catch (error) {
      if (activeRequest.current !== controller) return
      if (error.name !== 'AbortError') {
        const failure = {
          id: ++nextId.current,
          role: 'assistant',
          text: error.message,
          failed: true,
        }
        setMessages((previous) => [...previous.slice(-19), failure])
        if (error.status === 401) void refresh()
      }
    } finally {
      if (activeRequest.current === controller) {
        activeRequest.current = null
        setPending(false)
      }
    }
  }

  function cancel() {
    activeRequest.current?.abort()
    activeRequest.current = null
    setPending(false)
  }

  function submit(event) {
    event.preventDefault()
    const question = draft.trim()
    if (!question || pending || memoryBusy) return
    restoreMemory.current = false
    void send({ question, previous: context, use_memory: useMemory })
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
        if (open && !replyForReview && event.key === 'Escape') {
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
          <strong>Stack Intelligence</strong>
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
            <h2 id="assistant-title">Stack Intelligence</h2>
            <button
              type="button"
              className="text-button tw:mt-1 tw:min-h-8 tw:text-sm"
              aria-pressed={reviewing}
              onClick={() => (onReviewPage ? minimize() : setReviewing(!reviewing))}
            >
              {reviewing ? 'Back to chat' : 'Review practice questions'}
            </button>
          </div>
          {!reviewing && (
            <button
              type="button"
              className="assistant-tool"
              aria-label="Clear conversation"
              title="New conversation"
              onClick={() => {
                cancel()
                restoreMemory.current = false
                setMessages([])
                setDraft('')
                setContext(null)
                setLastRequest(null)
                input.current?.focus()
              }}
            >
              <Symbol name="rotate-left" />
            </button>
          )}
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

        {reviewing ? (
          <section
            className="tw:min-h-0 tw:flex-1 tw:overflow-y-auto tw:overscroll-contain tw:p-3"
            aria-label="Practice question review"
          >
            <QuestionReview embedded />
          </section>
        ) : (
          <>
            {service.reason === 'warming' && (
              <p className="assistant-loading-note" role="status">
                Loading event analysis; first use can take up to two minutes. You can still say
                hello or ask what I can help with while it loads.
              </p>
            )}

            <div
              className="assistant-transcript"
              ref={transcript}
              role="region"
              aria-label="Conversation and suggested questions"
              tabIndex={0}
            >
              {!messages.length && (
                <div className="assistant-welcome">
                  <span className="eyebrow">LET’S TALK ABOUT YOUR EVENT</span>
                  <h3>Hi! How can I help?</h3>
                  <p>Say hello, ask a quick question, or choose something below to get started.</p>
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
                aria-label="Conversation"
                aria-live="polite"
                aria-relevant="additions"
              >
                {messages.map((message) => (
                  <div key={message.id} className={`assistant-message is-${message.role}`}>
                    <span className="assistant-message-author">
                      {message.role === 'user'
                        ? 'You'
                        : `Stack Intelligence · ${answerLabels[message.response?.status] || 'Connection problem'}`}
                    </span>
                    <p>{message.text}</p>
                    {message.response?.interpretations?.length > 0 && (
                      <div
                        className="assistant-interpretations"
                        aria-label="Choose the intended meaning"
                      >
                        {message.response.interpretations.map((option) => (
                          <button
                            type="button"
                            key={option.question}
                            disabled={pending || memoryBusy}
                            onClick={() =>
                              void send({
                                question: option.question,
                                previous: context,
                                use_memory: useMemory,
                              })
                            }
                          >
                            {option.label}
                          </button>
                        ))}
                      </div>
                    )}
                    {message.response?.as_of && (
                      <small className="assistant-caveat">{message.response.scope_label}</small>
                    )}
                    {message.response?.review_candidate && (
                      <button
                        type="button"
                        className="text-button tw:mt-2 tw:min-h-8"
                        onClick={() => setReplyForReview(message.response.review_candidate)}
                      >
                        Review this reply
                      </button>
                    )}
                    {message.response?.as_of && <Evidence response={message.response} />}
                    {message.response?.knowledge_sources?.map((source) => (
                      <small className="assistant-caveat" key={source.document}>
                        System guide · {source.title}
                      </small>
                    ))}
                  </div>
                ))}
              </div>
              {pending && (
                <p className="assistant-pending" role="status">
                  Thinking…
                </p>
              )}
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
                  disabled={pending}
                  onChange={(event) => setDraft(event.target.value)}
                  onKeyDown={(event) => {
                    if (
                      event.key === 'Enter' &&
                      !event.shiftKey &&
                      !event.nativeEvent.isComposing
                    ) {
                      event.preventDefault()
                      event.currentTarget.form.requestSubmit()
                    }
                  }}
                  rows={2}
                  maxLength={1000}
                  placeholder="Say hello, or ask about your event…"
                  aria-describedby="assistant-composer-help"
                />
                <button
                  className="assistant-send"
                  type="submit"
                  disabled={!draft.trim() || pending}
                  aria-label="Send question"
                  title="Send question"
                >
                  <Symbol name="arrow-up" />
                </button>
              </div>
              <div className="assistant-composer-meta" id="assistant-composer-help">
                <span>
                  Read-only · English / Taglish · Keep student IDs and credentials out of chat.
                </span>
                <span>{draft.length}/1,000</span>
              </div>
              {pending ? (
                <button type="button" className="text-button" onClick={cancel}>
                  Cancel request · keep draft
                </button>
              ) : (
                lastRequest && (
                  <button
                    type="button"
                    className="text-button"
                    disabled={!service.available}
                    onClick={() => void send(lastRequest, true)}
                  >
                    Retry last question
                  </button>
                )
              )}
            </form>
          </>
        )}
      </section>
      {replyForReview && (
        <AssistantTrainingReview
          open
          singleReply
          candidate={replyForReview}
          csrf={admin?.csrf}
          onOpenChange={(shown) => {
            if (!shown) setReplyForReview(null)
          }}
        />
      )}
    </aside>
  )
}
