import { useState } from 'react'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import { Card, CardHeader, Button, InfoNote, Modal } from './ui'

const actions = {
  fence: [
    'Request device stop',
    'The device must save a permanent stop marker for this session. The reservation stays held until its receipt is reviewed.',
  ],
  recover_result: [
    'Recover recorded result',
    'Validate and record the saved terminal trace. This awards the replayed score and sends the player their result once.',
  ],
  release_unstarted: [
    'Release unstarted round',
    'The device confirmed this accepted round never started and is fenced. Close this ticket without a score. The player must scan again to rejoin.',
  ],
  void_interrupted: [
    'Void interrupted round',
    'The device confirmed this session is fenced. Close the interrupted ticket without a score. The player must scan again to rejoin.',
  ],
}

export default function DeviceRecovery() {
  const { currentPlayer, deviceRecovery, admin, isAdmin, refresh, notify, busy } = useApp()
  // Operators may release a no-show (no score is kept); voiding or recovering a score is admin-only.
  const allowed = deviceRecovery?.allowedActions || []
  const visibleActions = isAdmin ? allowed : allowed.filter((a) => a === 'release_unstarted')
  const needsAdministrator = visibleActions.length < allowed.length
  const [target, setTarget] = useState(null)
  const [reason, setReason] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  if (currentPlayer?.source !== 'device') return null

  function open(action) {
    setTarget({
      action,
      session: currentPlayer.sessionId,
      revision: deviceRecovery.revision,
      evidence: deviceRecovery.evidenceId,
      key: crypto.randomUUID(),
    })
    setReason('')
    setError('')
  }

  async function submit() {
    setSaving(true)
    setError('')
    try {
      await api(
        `/admin/sessions/${target.session}/${target.action === 'fence' ? 'fence' : 'resolve'}`,
        {
          method: 'POST',
          csrf: admin.csrf,
          key: target.key,
          body: {
            expectedRevision: target.revision,
            reason: reason.trim(),
            ...(target.action === 'fence'
              ? {}
              : { evidenceId: target.evidence, action: target.action }),
          },
        },
      )
      setTarget(null)
      notify(
        target.action === 'fence'
          ? 'Stop requested. The round stays held until the device receipt is reviewed.'
          : 'Recovery saved. A fresh ready heartbeat is required before the next turn.',
      )
      await refresh()
    } catch (failure) {
      setError(failure.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card className="tw:mt-6 tw:p-7">
      <CardHeader
        title="Device recovery"
        subtitle="Boot-bound evidence and audited operator decisions"
      />
      {!deviceRecovery?.bootId ? (
        <InfoNote>
          A boot journal has not been registered. Keep this reservation held; legacy heartbeats
          cannot authorize recovery.
        </InfoNote>
      ) : (
        <>
          <dl className="tw:m-0 tw:p-0">
            {[
              ['Current boot', deviceRecovery.bootId],
              [
                'Latest recovery evidence',
                deviceRecovery.phase?.replaceAll('_', ' ') || 'Awaiting device evidence',
              ],
              ['Round revision', deviceRecovery.revision],
            ].map(([label, value]) => (
              <div
                key={label}
                className="tw:flex tw:justify-between tw:gap-5 tw:border-b tw:border-line tw:py-3 tw:text-xs tw:leading-normal tw:last:border-0"
              >
                <dt className="tw:min-w-0 tw:wrap-anywhere tw:text-muted">{label}</dt>
                <dd className="tw:m-0 tw:min-w-0 tw:max-w-[65%] tw:wrap-anywhere tw:text-right tw:font-medium">
                  {value}
                </dd>
              </div>
            ))}
          </dl>
          {deviceRecovery.quarantined && (
            <InfoNote>
              Conflicting evidence was recorded. Recovery is blocked for investigation; this cabinet
              remains reserved.
            </InfoNote>
          )}
          <div className="tw:mt-5 tw:flex tw:flex-wrap tw:gap-2.5">
            {deviceRecovery.canFence && (
              <Button
                className="tw:max-[700px]:flex-[1_1_44%]"
                tone="light"
                disabled={busy || saving}
                onClick={() => open('fence')}
              >
                Request device stop
              </Button>
            )}
            {visibleActions.map((action) => (
              <Button
                key={action}
                className="tw:max-[700px]:flex-[1_1_44%]"
                tone="light"
                disabled={busy || saving}
                onClick={() => open(action)}
              >
                {actions[action]?.[0] || action}
              </Button>
            ))}
          </div>
          {needsAdministrator && (
            <InfoNote>
              This round&apos;s score must be decided by an administrator. Ask them to sign in and
              resolve it here.
            </InfoNote>
          )}
          <p className="field-help">
            A timeout cannot release the cabinet. Device receipts are software evidence; physical
            ESP32 recovery has not yet been tested.
          </p>
        </>
      )}
      <Modal
        title={target ? actions[target.action][0] : 'Device recovery'}
        description={target ? actions[target.action][1] : ''}
        open={Boolean(target)}
        onOpenChange={(open) => {
          if (!open && !saving) setTarget(null)
        }}
      >
        <label className="field-label" htmlFor="recovery-reason">
          Reason for this decision
        </label>
        <textarea
          id="recovery-reason"
          className="text-input"
          maxLength={160}
          value={reason}
          disabled={saving}
          onChange={(event) => {
            setReason(event.target.value)
            setTarget((previous) => ({ ...previous, key: crypto.randomUUID() }))
          }}
        />
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
        <div className="modal-actions">
          <Button disabled={saving || !reason.trim()} onClick={submit}>
            {saving ? 'Saving…' : 'Confirm decision'}
          </Button>
        </div>
      </Modal>
    </Card>
  )
}
