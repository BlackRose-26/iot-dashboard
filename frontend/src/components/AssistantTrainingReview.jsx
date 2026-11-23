import { useEffect, useState } from 'react'
import { api } from '../state/api'
import { Modal } from './ui'
import { topics, kinds } from './reviewLabels'

function freshTarget(topic) {
  return { topic, definition: null, knowledge: null, social: null }
}

export default function AssistantTrainingReview({
  open,
  onOpenChange,
  candidate,
  csrf,
  singleReply = false,
}) {
  const [options, setOptions] = useState(null)
  const [items, setItems] = useState([])
  const [selected, setSelected] = useState(null)
  const [target, setTarget] = useState(null)
  const [checked, setChecked] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [cursor, setCursor] = useState(null)

  async function load(before = null, retained = null) {
    const data = await api(`/admin/assistant/training${before ? `?before=${before}` : ''}`)
    setItems((rows) => [
      ...new Map(
        (before
          ? [...rows, ...data.items]
          : [
              ...data.items,
              ...(retained && !data.items.some((row) => row.id === retained.id) ? [retained] : []),
            ]
        ).map((row) => [row.id, row]),
      ).values(),
    ])
    setCursor(data.next_cursor)
    if (data.skipped_invalid) setError('Some examples need a schema update and were excluded.')
  }

  useEffect(() => {
    if (!open) return
    let active = true
    setSelected(null)
    setTarget(candidate?.target || null)
    setChecked(false)
    setError('')
    setNotice('')
    setBusy(true)
    Promise.all([api('/admin/assistant/training/options'), api('/admin/assistant/training')])
      .then(([settings, data]) => {
        if (!active) return
        setOptions(settings)
        setItems(data.items)
        setCursor(data.next_cursor)
      })
      .catch((failure) => {
        if (active) setError(failure.message)
      })
      .finally(() => {
        if (active) setBusy(false)
      })
    return () => {
      active = false
    }
  }, [open, candidate])

  function choose(item) {
    setSelected(item)
    setTarget(item.target)
    setChecked(false)
    setError('')
    setNotice('')
  }

  async function action(operation) {
    setBusy(true)
    setError('')
    try {
      await operation()
    } catch (failure) {
      setError(failure.message)
    } finally {
      setBusy(false)
    }
  }

  async function save() {
    const row = await api('/admin/assistant/training', {
      method: 'POST',
      csrf,
      body: { input: candidate.input, target },
    })
    await load(null, row)
    choose(row)
    setNotice(
      row.duplicate
        ? 'This input is already queued. Review the existing example.'
        : 'Saved as pending. Review it before approval.',
    )
  }

  async function review(decision) {
    const row = await api(`/admin/assistant/training/${selected.id}`, {
      method: 'PATCH',
      csrf,
      body: {
        revision: selected.revision,
        decision,
        target: decision === 'reject' ? selected.target : target,
        reviewed: checked,
        context_version: options.context_version,
      },
    })
    await load(null, row)
    choose(row)
    setNotice(
      decision === 'approve'
        ? 'Approved for future question interpretation when memory is on. Model weights are unchanged.'
        : decision === 'reject'
          ? 'Rejected examples are excluded from future answers and exports.'
          : 'Saved as pending; approval is required again.',
    )
  }

  async function remove() {
    await api(`/admin/assistant/training/${selected.id}`, { method: 'DELETE', csrf })
    setSelected(null)
    setTarget(candidate?.target || null)
    setChecked(false)
    await load()
    setNotice('Example removed from the review queue, future answers and exports.')
  }

  async function exportApproved() {
    const data = await api('/admin/assistant/training/export', { method: 'POST', csrf })
    const url = URL.createObjectURL(new Blob([data.jsonl], { type: 'application/x-ndjson' }))
    const link = document.createElement('a')
    link.href = url
    link.download = data.filename
    document.body.appendChild(link)
    link.click()
    link.remove()
    setTimeout(() => URL.revokeObjectURL(url), 1000)
    setNotice(
      `Exported ${data.count} approved routing examples. The active Ollama model is unchanged.`,
    )
  }

  const input = selected?.input || candidate?.input
  const labelField = ['knowledge', 'social', 'definition'].includes(target?.topic)
    ? target.topic
    : null
  const validTarget = target && (!labelField || target[labelField])
  const dirty = selected && JSON.stringify(target) !== JSON.stringify(selected.target)

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title={singleReply ? 'Review this reply' : 'Training examples'}
      description={
        singleReply
          ? 'Check the words and choose what the person meant. Approved examples can help with similar questions when memory is on.'
          : 'Review saved examples that can help with similar questions when memory is on.'
      }
    >
      <div className="assistant-training-review">
        {error && <p role="alert">{error}</p>}
        {notice && <p role="status">{notice}</p>}
        {!singleReply && (
          <>
            <button
              className="text-button"
              type="button"
              disabled={busy || dirty}
              onClick={() => void action(exportApproved)}
            >
              <i className="fa-solid fa-download" aria-hidden="true" /> Export approved JSONL
            </button>
            {dirty && <small>Save or approve your label changes before exporting.</small>}
            <label>
              Review queue
              <select
                aria-label="Review queue"
                value={selected?.id || ''}
                disabled={busy}
                onChange={(event) => {
                  const row = items.find((item) => item.id === event.target.value)
                  if (row) choose(row)
                  else {
                    setSelected(null)
                    setTarget(candidate?.target || null)
                    setChecked(false)
                  }
                }}
              >
                <option value="">
                  {candidate ? 'New selected conversation example' : 'Select an example'}
                </option>
                {items.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.status}
                    {!item.current ? ' · needs re-review' : ''} —{' '}
                    {item.input.safe_tokens.slice(0, 12).join(' ')}
                  </option>
                ))}
              </select>
            </label>
            {cursor && (
              <button
                type="button"
                className="text-button"
                disabled={busy}
                onClick={() => void action(() => load(cursor))}
              >
                Load more examples
              </button>
            )}
          </>
        )}
        {input && options && target ? (
          <>
            <div className="assistant-training-preview">
              <strong>Words to check</strong>
              <p>{input.safe_tokens.join(' ')}</p>
              <small>No original message, metric answer or player record is saved.</small>
              {input.has_unrecognized_words && (
                <p>
                  Some words were removed. Approve only if this visible input still expresses the
                  intended question.
                </p>
              )}
              <details>
                <summary>More details</summary>
                <pre>{JSON.stringify({ ...input, safe_tokens: undefined }, null, 2)}</pre>
              </details>
            </div>
            <label>
              What was the question about?
              <select
                value={target.topic}
                disabled={busy}
                onChange={(event) => {
                  setTarget(freshTarget(event.target.value))
                  setChecked(false)
                }}
              >
                {options.topics.map((topic) => (
                  <option key={topic} value={topic}>
                    {topics[topic] || topic.replaceAll('_', ' ')}
                  </option>
                ))}
              </select>
            </label>
            {labelField && (
              <label>
                Which part?
                <select
                  value={target[labelField] || ''}
                  disabled={busy}
                  onChange={(event) => {
                    setTarget({ ...target, [labelField]: event.target.value })
                    setChecked(false)
                  }}
                >
                  <option value="">Choose a label</option>
                  {options[labelField].map((label) => (
                    <option key={label} value={label}>
                      {kinds[labelField]?.[label] || label.replaceAll('_', ' ')}
                    </option>
                  ))}
                </select>
              </label>
            )}
            {selected ? (
              <>
                <p>
                  Status: <strong>{selected.status}</strong>
                  {!selected.current && ' · system context changed; review again before exporting.'}
                </p>
                <label className="assistant-training-attestation">
                  <input
                    type="checkbox"
                    checked={checked}
                    disabled={busy}
                    onChange={(event) => setChecked(event.target.checked)}
                  />
                  I checked the meaning. The example has no private details or real game numbers.
                </label>
                <div className="assistant-training-actions">
                  <button
                    type="button"
                    className="button"
                    disabled={busy || !validTarget || !checked}
                    onClick={() => void action(() => review('approve'))}
                  >
                    Approve example
                  </button>
                  <button
                    type="button"
                    className="text-button"
                    disabled={busy || !validTarget}
                    onClick={() => void action(() => review('revise'))}
                  >
                    Save as pending
                  </button>
                  <button
                    type="button"
                    className="text-button"
                    disabled={busy}
                    onClick={() => void action(() => review('reject'))}
                  >
                    Reject example
                  </button>
                  <button
                    type="button"
                    className="text-button"
                    disabled={busy}
                    onClick={() => void action(remove)}
                  >
                    Remove example
                  </button>
                </div>
              </>
            ) : (
              <button
                type="button"
                className="button"
                disabled={busy || !validTarget}
                onClick={() => void action(save)}
              >
                Save for approval
              </button>
            )}
          </>
        ) : (
          <p>
            {busy
              ? 'Loading review queue…'
              : 'Choose Review for training on a chat reply to propose an example. Nothing is collected automatically.'}
          </p>
        )}
      </div>
    </Modal>
  )
}
