import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useApp } from '../state/AppContext'
import { useAssistant, assistantStatus } from '../state/AssistantContext'
import { Card, CardHeader, PageHeading } from '../components/ui'
import AssistantTrainingReview from '../components/AssistantTrainingReview'
import StaffAccounts from '../components/StaffAccounts'
import '../styles/settings.css'
import { gameLabel } from '../state/game'

export default function Settings() {
  const { admin, isAdmin, theme, setTheme, game } = useApp()
  const ai = useAssistant()
  const [trainingOpen, setTrainingOpen] = useState(false)
  const [reviewLast, setReviewLast] = useState(false)
  useEffect(() => {
    void ai.loadMemory()
    void ai.checkConnection(false)
  }, [ai.loadMemory, ai.checkConnection])
  return (
    <>
      <PageHeading
        eyebrow={isAdmin ? 'ADMINISTRATION' : 'OPERATOR'}
        title="Dashboard settings"
        description="Appearance and Stack Intelligence preferences for your staff account."
      />
      <div className="settings-grid">
        <Card>
          <CardHeader title="Appearance" subtitle="Choose your dashboard theme." />
          <label className="settings-field">
            Color mode
            <select value={theme} onChange={(event) => setTheme(event.target.value)}>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </label>
        </Card>
        <Card>
          <CardHeader title="Stack Intelligence" subtitle="Local analysis and connection status." />
          <div className="settings-row">
            <span>{assistantStatus[ai.service.reason] || 'Local analysis unavailable'}</span>
            <button
              className="button light"
              disabled={['checking', 'warming'].includes(ai.service.reason)}
              onClick={() => void ai.checkConnection()}
            >
              Check connection
            </button>
          </div>
          <p className="settings-help">
            All available system information is considered automatically. You can ask for a specific
            date or result source in your message.
          </p>
          <p className="settings-help">
            ACS Carnival · {gameLabel(game)} · Local Ollama. Simulator and physical-device results
            are labelled separately.
          </p>
        </Card>
        <Card>
          <CardHeader title="Conversation memory" subtitle="Private to your staff account." />
          <label className="settings-toggle">
            <input
              type="checkbox"
              checked={ai.useMemory}
              disabled={ai.pending || ai.memoryBusy}
              onChange={(event) => ai.setUseMemory(event.target.checked)}
            />
            Use private memory
          </label>
          <p className="settings-help">
            Applies to this session.{' '}
            {ai.memory?.available
              ? `${ai.memory.remembered} saved context updates.`
              : 'Saved memory is unavailable.'}{' '}
            Current game data is always queried again.
          </p>
          <button
            className="button light"
            disabled={ai.pending || ai.memoryBusy}
            onClick={() => void ai.forgetMemory()}
          >
            Forget saved memory
          </button>
          {ai.memoryError && <p role="status">{ai.memoryError}</p>}
        </Card>
        {isAdmin && <StaffAccounts />}
        {isAdmin && (
          <>
            <Card>
              <CardHeader
                title="Check practice questions"
                subtitle="Help check what the assistant should understand."
              />
              <Link to="/admin/question-review" className="button light tw:mt-3">
                Review questions
              </Link>
            </Card>
            <Card>
              <CardHeader
                title="Reviewed examples"
                subtitle="Review interpretation labels separately from your conversation."
              />
              <p className="settings-help">
                Only approved, current examples from your account can guide future questions. Model
                weights remain unchanged.
              </p>
              <div className="settings-actions">
                <button
                  className="button light"
                  onClick={() => {
                    setReviewLast(false)
                    setTrainingOpen(true)
                  }}
                >
                  Training examples
                </button>
                <button
                  className="button light"
                  disabled={!ai.candidate}
                  onClick={() => {
                    setReviewLast(true)
                    setTrainingOpen(true)
                  }}
                >
                  Review last eligible answer
                </button>
              </div>
            </Card>
          </>
        )}
      </div>
      <AssistantTrainingReview
        open={trainingOpen}
        onOpenChange={setTrainingOpen}
        candidate={reviewLast ? ai.candidate : null}
        csrf={admin?.csrf}
      />
    </>
  )
}
