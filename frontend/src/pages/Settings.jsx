import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useApp } from '../state/AppContext'
import { useAssistant, assistantStatus } from '../state/AssistantContext'
import { Card, CardHeader, PageHeading } from '../components/ui'
import AssistantTrainingReview from '../components/AssistantTrainingReview'
import StaffAccounts from '../components/StaffAccounts'
import GameScreenPairing from '../components/GameScreenPairing'
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
      <div className="tw:grid tw:grid-cols-2 tw:max-[760px]:grid-cols-1 tw:gap-6 tw:[&_.card]:p-6">
        <Card>
          <CardHeader title="Appearance" subtitle="Choose your dashboard theme." />
          <label className="tw:grid tw:gap-2 tw:text-muted tw:text-[13px] tw:[&_select]:p-3 tw:[&_select]:rounded-xl tw:[&_select]:border tw:[&_select]:border-solid tw:[&_select]:border-line tw:[&_select]:bg-surface tw:[&_select]:text-ink">
            Color mode
            <select value={theme} onChange={(event) => setTheme(event.target.value)}>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </label>
        </Card>
        <Card>
          <CardHeader title="Stack Intelligence" subtitle="Local analysis and connection status." />
          <div className="tw:flex tw:gap-3 tw:items-center tw:flex-wrap tw:justify-between">
            <span>{assistantStatus[ai.service.reason] || 'Local analysis unavailable'}</span>
            <button
              className="button light"
              disabled={['checking', 'warming'].includes(ai.service.reason)}
              onClick={() => void ai.checkConnection()}
            >
              Check connection
            </button>
          </div>
          <p className="tw:text-muted tw:text-[13px] tw:leading-[1.7] tw:my-4">
            All available system information is considered automatically. You can ask for a specific
            date or result source in your message.
          </p>
          <p className="tw:text-muted tw:text-[13px] tw:leading-[1.7] tw:my-4">
            ACS Carnival · {gameLabel(game)} · Local Ollama. Simulator and physical-device results
            are labelled separately.
          </p>
        </Card>
        <Card>
          <CardHeader title="Conversation memory" subtitle="Private to your staff account." />
          <label className="tw:flex tw:items-center tw:gap-2.5 tw:text-[14px]">
            <input
              type="checkbox"
              checked={ai.useMemory}
              disabled={ai.pending || ai.memoryBusy}
              onChange={(event) => ai.setUseMemory(event.target.checked)}
            />
            Use private memory
          </label>
          <p className="tw:text-muted tw:text-[13px] tw:leading-[1.7] tw:my-4">
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
        {isAdmin && <GameScreenPairing />}
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
              <p className="tw:text-muted tw:text-[13px] tw:leading-[1.7] tw:my-4">
                Only approved, current examples from your account can guide future questions. Model
                weights remain unchanged.
              </p>
              <div className="tw:flex tw:gap-3 tw:items-center tw:flex-wrap">
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
