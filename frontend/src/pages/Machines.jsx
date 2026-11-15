import { useApp } from '../state/AppContext'
import { Card, CardHeader, PageHeading, Badge, Button, InfoNote } from '../components/ui'
import { Matrix, stateLabels } from '../components/LiveRound'
import { Radio, Layers3 } from '../components/icons'

export function SimulatorControls() {
  const { simulatorEnabled, simulate, busy, currentPlayer, machineState, machine } = useApp()
  if (!simulatorEnabled) return null
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
  const { machineState, machine, currentPlayer } = useApp()
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
          <Matrix large level={0} />
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
              <dd>Classic v1 · proposed</dd>
            </div>
          </dl>
        </Card>
      </div>
      <InfoNote>
        {simulated
          ? 'The simulator is active. This does not verify physical hardware.'
          : 'A fresh device heartbeat is required before calling a player. Missing readings remain unknown.'}
      </InfoNote>
      <SimulatorControls />
    </>
  )
}
