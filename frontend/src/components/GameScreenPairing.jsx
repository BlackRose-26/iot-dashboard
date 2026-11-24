import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import { ScreenDevice } from '../screen/deviceClient'
import { Badge, Button, Card, CardHeader, InfoNote, Modal } from './ui'

// The game runs on the web game screen by default (since 25 Nov 2026); the LED cabinet is still
// supported. Cabinet 01 has one device at a time, chosen here by an administrator.
export default function GameScreenPairing() {
  const { admin, machine } = useApp()
  const navigate = useNavigate()
  const [confirm, setConfirm] = useState(null) // 'screen' | 'led'
  const [error, setError] = useState('')
  const [working, setWorking] = useState(false)
  const firmware = machine?.firmware || ''
  const current = firmware.startsWith('web-screen')
    ? 'Web game screen'
    : firmware
      ? 'LED cabinet'
      : 'No device has connected yet'

  async function run() {
    setWorking(true)
    setError('')
    try {
      if (confirm === 'screen') {
        const { deviceToken } = await api('/admin/screen/pair', {
          method: 'POST',
          csrf: admin.csrf,
        })
        new ScreenDevice().pair(deviceToken)
        navigate('/screen')
      } else {
        await api('/admin/screen/use-led-cabinet', { method: 'POST', csrf: admin.csrf })
        setConfirm(null)
      }
    } catch (failure) {
      setError(failure.message)
      setConfirm(null)
    } finally {
      setWorking(false)
    }
  }

  return (
    <Card>
      <CardHeader
        title="Game screen"
        subtitle="Where the stacking game is played: the web game screen (default) or the LED cabinet."
      />
      <p className="tw:my-4 tw:flex tw:flex-wrap tw:items-center tw:gap-2 tw:text-[13px] tw:text-muted">
        Last connected: <Badge tone="soft">{current}</Badge>
      </p>
      <p className="tw:text-muted tw:text-[13px] tw:leading-[1.7] tw:mb-4">
        Pair the screen on the screen laptop, in Chrome or Edge opened at the event&apos;s HTTPS
        address, with the ESP32 button bridge plugged in. You can sign out afterwards; the screen
        keeps working.
      </p>
      <div className="tw:flex tw:flex-wrap tw:gap-2">
        <Button onClick={() => setConfirm('screen')} disabled={working}>
          Use this laptop as the game screen
        </Button>
        <Button tone="light" onClick={() => setConfirm('led')} disabled={working}>
          Use the LED cabinet instead
        </Button>
      </div>
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <Modal
        title={
          confirm === 'led'
            ? 'Switch back to the LED cabinet?'
            : 'Pair this laptop as the game screen?'
        }
        description={
          confirm === 'led'
            ? 'The ESP32 game firmware works again with its configured token. Any paired game screen stops working.'
            : 'Any other game screen, and the LED cabinet firmware, stop working until switched back.'
        }
        open={Boolean(confirm)}
        onOpenChange={(open) => !open && setConfirm(null)}
      >
        <InfoNote>Switching is refused while a player is called or playing.</InfoNote>
        <div className="modal-actions">
          <Button tone="light" onClick={() => setConfirm(null)}>
            Cancel
          </Button>
          <Button onClick={() => void run()} disabled={working}>
            {working
              ? 'Switching…'
              : confirm === 'led'
                ? 'Use the LED cabinet'
                : 'Pair and open the game screen'}
          </Button>
        </div>
      </Modal>
    </Card>
  )
}
