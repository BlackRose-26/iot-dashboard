import { useState } from 'react'
import {
  UsersRound,
  Clock3,
  Play,
  Pause,
  ArrowUpRight,
  ListOrdered,
  UserRoundX,
} from '../components/icons'
import { useApp } from '../state/AppContext'
import { stateLabels } from '../components/LiveRound'
import {
  Card,
  CardHeader,
  PageHeading,
  Metric,
  Button,
  Badge,
  SearchInput,
  Avatar,
  Modal,
  EmptyState,
  InfoNote,
} from '../components/ui'
import { RegistrationQR } from '../components/Shell'
import { SimulatorControls } from './Machines'

export default function Queue() {
  const { queue, skipPlayer, machineState, callNext, admissionsOpen, setAdmissionsOpen, busy } =
    useApp()
  const [search, setSearch] = useState('')
  const [skip, setSkip] = useState(null)
  const [reason, setReason] = useState('')
  const displayed = queue.filter((p) =>
    `${p.nickname} ${p.code}`.toLowerCase().includes(search.toLowerCase()),
  )
  const canCall = machineState === 'ready' && admissionsOpen && queue.length > 0
  const nextReason = !admissionsOpen
    ? 'Admissions are paused'
    : machineState !== 'ready'
      ? `Cabinet: ${stateLabels[machineState].toLowerCase()}`
      : !queue.length
        ? 'No players waiting'
        : 'Call the first player when the cabinet is ready'
  const confirmSkip = async () => {
    await skipPlayer(skip.id, reason.trim())
    setSkip(null)
    setReason('')
  }
  return (
    <>
      <PageHeading
        title="Their next big moment."
        description="A fair line. A ready cabinet. Let’s keep the carnival moving."
      >
        <RegistrationQR />
        <Button
          tone="light"
          onClick={() => {
            setAdmissionsOpen(!admissionsOpen)
          }}
        >
          {admissionsOpen ? <Pause size={16} /> : <Play size={16} />}{' '}
          {admissionsOpen ? 'Pause admissions' : 'Open admissions'}
        </Button>
      </PageHeading>
      <div className="queue-layout">
        <Card className="queue-main">
          <CardHeader
            title="Player queue"
            subtitle="First in, first to stack"
            icon={ListOrdered}
            action={
              <Badge tone={admissionsOpen ? 'lime' : 'neutral'} dot>
                {admissionsOpen ? 'Admissions open' : 'Paused'}
              </Badge>
            }
          />
          <SearchInput value={search} onChange={setSearch} />
          {displayed.length ? (
            <div className="queue-full-list">
              {displayed.map((p) => {
                const index = queue.findIndex((q) => q.id === p.id)
                return (
                  <div className="queue-full-row" key={p.id}>
                    <span className="queue-number">{String(index + 1).padStart(2, '0')}</span>
                    <Avatar name={p.nickname} index={index} />
                    <div className="player-info">
                      <strong>{p.nickname}</strong>
                      <span>
                        {p.code} · Joined {p.joinedAt}
                      </span>
                    </div>
                    <Badge tone={index === 0 ? 'blue' : 'neutral'}>
                      {index === 0 ? 'Up next' : 'Waiting'}
                    </Badge>
                    <button
                      className="text-button"
                      onClick={() => {
                        setSkip(p)
                        setReason('')
                      }}
                    >
                      Skip<span className="sr-only"> {p.nickname}</span>
                    </button>
                  </div>
                )
              })}
            </div>
          ) : (
            <EmptyState
              title={search ? 'No players found.' : 'A fresh start.'}
              description={
                search
                  ? 'Try a different nickname or public player code.'
                  : 'The queue is empty. Open registration for the next challenger.'
              }
              action={
                search ? (
                  <Button tone="light" onClick={() => setSearch('')}>
                    Clear search
                  </Button>
                ) : null
              }
            />
          )}
        </Card>
        <div className="queue-aside">
          <Card className="next-card">
            <span className="eyebrow">THE NEXT CHALLENGER</span>
            <div className="next-avatar">
              <UsersRound size={36} strokeWidth={1.4} />
            </div>
            <h2>{queue[0]?.nickname || 'The stage is open.'}</h2>
            <p>{queue[0]?.code || 'No players in the queue'}</p>
            <div className="next-status">
              <span>Cabinet 01</span>
              <Badge dot>{stateLabels[machineState]}</Badge>
            </div>
            <Button className="full-width" disabled={!canCall || busy} onClick={callNext}>
              Call next player
              <ArrowUpRight size={18} />
            </Button>
            <p className="field-help">{nextReason}</p>
          </Card>
          <div className="mini-metrics">
            <Metric label="In the queue" value={queue.length} detail="Players waiting" />
            <Metric label="Order" value="FIFO" detail="First come, first served" />
          </div>
          <InfoNote>
            Registration saves a place in line. An operator must call the next player when the
            cabinet is ready; the physical button starts the reserved game at the cabinet.
          </InfoNote>
        </div>
      </div>
      <SimulatorControls />
      <Modal
        title="Skip this player?"
        description={skip ? `Remove ${skip.nickname} (${skip.code}) from the waiting queue.` : ''}
        open={Boolean(skip)}
        onOpenChange={(open) => {
          if (!open) setSkip(null)
        }}
      >
        <label className="field-label" htmlFor="skip-reason">
          Reason
        </label>
        <input
          autoComplete="off"
          className="text-input"
          id="skip-reason"
          placeholder="For example, player is absent"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          maxLength={160}
        />
        <div className="modal-actions">
          <Button tone="light" onClick={() => setSkip(null)}>
            Keep in queue
          </Button>
          <Button disabled={!reason.trim()} onClick={confirmSkip}>
            Skip player
          </Button>
        </div>
      </Modal>
    </>
  )
}
