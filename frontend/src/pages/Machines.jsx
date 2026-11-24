import { useState } from 'react'
import { useApp } from '../state/AppContext'
import { gameLabel } from '../state/game'
import { api } from '../state/api'
import { Card, CardHeader, PageHeading, Badge, Button, InfoNote, Modal } from '../components/ui'
import { Matrix, stateLabels } from '../components/LiveRound'
import { Radio, Layers3 } from '../components/icons'
import DeviceRecovery from '../components/DeviceRecovery'
import NoShowRelease from '../components/NoShowRelease'

export function DeviceCommands() {
  const { deviceCommands = [], currentPlayer, admin, refresh, notify, busy } = useApp()
  const [target, setTarget] = useState(null)
  const [reason, setReason] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const physical = currentPlayer?.source === 'device'
  async function flag() {
    setSaving(true)
    setError('')
    try {
      await api(`/admin/sessions/${target.id}/review`, {
        method: 'POST',
        csrf: admin.csrf,
        body: { expectedRevision: target.revision, reason: reason.trim() },
      })
      await refresh()
      notify('Round held for operator review. The cabinet remains reserved.')
      setTarget(null)
    } catch (failure) {
      setError(failure.message)
    } finally {
      setSaving(false)
    }
  }
  return (
    <Card>
      <CardHeader title="Command delivery" subtitle="Saved reservation, receipt and start status" />
      {!deviceCommands.length && (
        <p className="field-help">No cabinet commands have been recorded.</p>
      )}
      <dl className="device-facts">
        {deviceCommands.map((command) => (
          <div key={command.id}>
            <dt>
              {command.source === 'simulator' ? 'Simulator' : 'Device'}{' '}
              {command.type === 'reserve' ? 'reservation' : command.type}
              <p className="field-help">{new Date(command.createdAt).toLocaleString('en-PH')}</p>
            </dt>
            <dd>
              <Badge tone="soft">{command.status}</Badge>
              {command.rejectionCode && (
                <p className="field-help">{command.rejectionCode.replaceAll('_', ' ')}</p>
              )}
            </dd>
          </div>
        ))}
      </dl>
      <p className="field-help">
        Pending means saved, accepted means the device recorded a receipt, and applied means the
        server recorded the start (or a stop receipt for a fence command). These states do not
        verify physical hardware.
      </p>
      {physical && currentPlayer.reviewRequired && (
        <InfoNote>
          This round needs operator review. The cabinet and player reservation remain held; a
          timeout does not release them.
        </InfoNote>
      )}
      {physical && currentPlayer.status !== 'review' && (
        <Button
          tone="light"
          disabled={busy}
          onClick={() => {
            setTarget({ id: currentPlayer.sessionId, revision: currentPlayer.revision })
            setReason('')
            setError('')
          }}
        >
          Flag round for review
        </Button>
      )}
      {physical && currentPlayer.status === 'review' && (
        <p role="status">
          Review hold active. Device reconciliation is required before another turn can be assigned.
        </p>
      )}
      <Modal
        title="Hold this round for review"
        description="The cabinet stays reserved while the operator investigates. This does not stop a physical game or release its ticket."
        open={Boolean(target)}
        onOpenChange={(open) => {
          if (!open && !saving) setTarget(null)
        }}
      >
        <label className="field-label" htmlFor="device-review-reason">
          Reason for review
        </label>
        <textarea
          id="device-review-reason"
          className="text-input"
          maxLength={160}
          value={reason}
          onChange={(event) => setReason(event.target.value)}
        />
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
        <div className="modal-actions">
          <Button disabled={saving || !reason.trim()} onClick={flag}>
            {saving ? 'Saving…' : 'Hold for review'}
          </Button>
        </div>
      </Modal>
    </Card>
  )
}

export function SimulatorControls() {
  const { simulatorEnabled, simulate, busy, currentPlayer, machineState, machine, isAdmin } =
    useApp()
  if (!simulatorEnabled || !isAdmin) return null
  const simulated = machine.health?.source === 'simulator'
  return (
    <Card className="simulator-card">
      <h2>Development simulator</h2>
      <p>
        Test the queue and player notifications. No ESP32 is controlled. Simulator scores have their
        own leaderboard.
      </p>
      <p>
        Set simulator ready, then use Call next player on the Queue page. Start the test round, then
        choose Finish: win or Finish: loss to deliver the result to the player’s ticket.
      </p>
      <div className="simulator-actions">
        <Button
          tone="light"
          disabled={busy || Boolean(currentPlayer)}
          onClick={() => simulate('ready')}
        >
          Set simulator ready
        </Button>
        <Button
          tone="light"
          disabled={busy || !simulated || machineState !== 'reserved'}
          onClick={() => simulate('start')}
        >
          Start test round
        </Button>
        <Button
          tone="light"
          disabled={busy || !simulated || machineState !== 'playing'}
          onClick={() => simulate('win')}
        >
          Finish: win
        </Button>
        <Button
          tone="light"
          disabled={busy || !simulated || machineState !== 'playing'}
          onClick={() => simulate('loss')}
        >
          Finish: loss
        </Button>
        <Button
          tone="light"
          disabled={busy || !currentPlayer || !simulated}
          onClick={() => simulate('release')}
        >
          Release test ticket
        </Button>
      </div>
    </Card>
  )
}
export default function Machines() {
  const { machineState, machine, currentPlayer, game } = useApp()
  const simulated = machine.health?.source === 'simulator'
  return (
    <>
      <PageHeading
        title="Cabinet status"
        description="Authenticated heartbeat and game-session state."
      />
      <div className="two-column">
        <Card className="cabinet-card">
          <CardHeader
            title="Cabinet 01"
            subtitle="ESP32 · LED matrix · physical button"
            icon={Layers3}
          />
          <Matrix large level={0} columns={game?.columns} levels={game?.levels} />
          <p className="field-help">Board illustration. Live row telemetry is not connected.</p>
        </Card>
        <Card>
          <CardHeader
            title="Connection & readiness"
            subtitle="Last observed server state"
            icon={Radio}
            action={<Badge dot>{stateLabels[machineState]}</Badge>}
          />
          <dl className="device-facts">
            <div>
              <dt>Source</dt>
              <dd>{simulated ? 'Development simulator' : 'Physical device'}</dd>
            </div>
            <div>
              <dt>Wi-Fi signal</dt>
              <dd>{machine.health?.rssi != null ? `${machine.health.rssi} dBm` : 'Unknown'}</dd>
            </div>
            <div>
              <dt>Last heartbeat</dt>
              <dd>
                {machine.lastSeen
                  ? new Date(machine.lastSeen).toLocaleTimeString()
                  : 'Not received'}
              </dd>
            </div>
            <div>
              <dt>Firmware</dt>
              <dd>{machine.firmware || 'Not connected'}</dd>
            </div>
            <div>
              <dt>Active player</dt>
              <dd>{currentPlayer?.code || 'None'}</dd>
            </div>
            <div>
              <dt>Ruleset</dt>
              <dd>{gameLabel(game)} · play-testing pending</dd>
            </div>
          </dl>
        </Card>
      </div>
      <InfoNote>
        {simulated
          ? 'The simulator is active. This does not verify physical hardware.'
          : 'A fresh device heartbeat is required before calling a player. Missing readings remain unknown.'}
      </InfoNote>
      <DeviceCommands />
      <NoShowRelease />
      <DeviceRecovery />
      <SimulatorControls />
    </>
  )
}
