import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import DeviceRecovery from './DeviceRecovery'

const mocks = vi.hoisted(() => ({ api: vi.fn(), refresh: vi.fn(), notify: vi.fn(), state: {} }))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({
    ...mocks.state,
    admin: { csrf: 'synthetic' },
    refresh: mocks.refresh,
    notify: mocks.notify,
  }),
}))
beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockResolvedValue({ ok: true })
  mocks.state = {
    currentPlayer: { source: 'device', sessionId: 'synthetic-session' },
    deviceRecovery: {
      bootId: 'synthetic-boot',
      revision: 4,
      canFence: true,
      allowedActions: [],
      evidenceId: null,
    },
  }
})

it('offers no release without evidence and requires a reason for a stop request', async () => {
  const user = userEvent.setup()
  render(<DeviceRecovery />)
  expect(screen.queryByRole('button', { name: /release/i })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Request device stop' }))
  expect(screen.getByRole('button', { name: 'Confirm decision' })).toBeDisabled()
  await user.type(screen.getByLabelText('Reason for this decision'), 'Investigate frozen panel')
  await user.click(screen.getByRole('button', { name: 'Confirm decision' }))
  await waitFor(() => expect(mocks.refresh).toHaveBeenCalledOnce())
  expect(mocks.api).toHaveBeenCalledWith(
    '/admin/sessions/synthetic-session/fence',
    expect.objectContaining({
      method: 'POST',
      csrf: 'synthetic',
      key: expect.any(String),
      body: { reason: 'Investigate frozen panel', expectedRevision: 4 },
    }),
  )
})

it('keeps stale evidence errors visible and retries an unchanged action with its original key', async () => {
  mocks.state.deviceRecovery = {
    bootId: 'synthetic-boot',
    revision: 8,
    canFence: false,
    evidenceId: 'synthetic-evidence',
    allowedActions: ['release_unstarted'],
    phase: 'fenced_unstarted',
  }
  mocks.api.mockRejectedValue(new Error('The round or recovery evidence changed.'))
  const user = userEvent.setup()
  render(<DeviceRecovery />)
  await user.click(screen.getByRole('button', { name: 'Release unstarted round' }))
  await user.type(screen.getByLabelText('Reason for this decision'), 'Reviewed saved stop receipt')
  await user.click(screen.getByRole('button', { name: 'Confirm decision' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('evidence changed')
  await user.click(screen.getByRole('button', { name: 'Confirm decision' }))
  await waitFor(() => expect(mocks.api).toHaveBeenCalledTimes(2))
  expect(mocks.api.mock.calls[1][1]).toEqual(mocks.api.mock.calls[0][1])
  expect(mocks.notify).not.toHaveBeenCalled()
})

it('shows quarantine and legacy-device holds without a recovery action', () => {
  mocks.state.deviceRecovery = {
    bootId: 'synthetic-boot',
    revision: 9,
    quarantined: true,
    allowedActions: [],
    canFence: false,
  }
  const { rerender } = render(<DeviceRecovery />)
  expect(screen.getByText(/Conflicting evidence was recorded/)).toBeVisible()
  expect(screen.queryByRole('button')).not.toBeInTheDocument()
  mocks.state.deviceRecovery = null
  rerender(<DeviceRecovery />)
  expect(screen.getByText(/legacy heartbeats cannot authorize recovery/)).toBeVisible()
})

it('leaves score decisions to an administrator when an operator is signed in', () => {
  const evidence = {
    allowedActions: ['void_interrupted'],
    canFence: false,
    evidenceId: 'synthetic-evidence',
  }
  mocks.state = {
    ...mocks.state,
    isAdmin: false,
    deviceRecovery: { ...mocks.state.deviceRecovery, ...evidence },
  }
  const { rerender } = render(<DeviceRecovery />)
  expect(screen.queryByRole('button', { name: /void/i })).not.toBeInTheDocument()
  expect(screen.getByText(/must be decided by an administrator/)).toBeInTheDocument()
  mocks.state = { ...mocks.state, isAdmin: true }
  rerender(<DeviceRecovery />)
  expect(screen.getByRole('button', { name: /void/i })).toBeInTheDocument()
  expect(screen.queryByText(/must be decided by an administrator/)).not.toBeInTheDocument()
})
