import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DeviceCommands } from './Machines'

const mocks = vi.hoisted(() => ({ api: vi.fn(), refresh: vi.fn(), notify: vi.fn(), current: null }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({
    admin: { csrf: 'synthetic-csrf' },
    currentPlayer: mocks.current,
    refresh: mocks.refresh,
    notify: mocks.notify,
    deviceCommands: [
      {
        id: 'synthetic-command',
        type: 'reserve',
        source: 'device',
        status: 'accepted',
        createdAt: '2026-11-19T00:00:00Z',
      },
    ],
  }),
}))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockResolvedValue({ ok: true })
  mocks.current = {
    source: 'device',
    sessionId: 'synthetic-session',
    status: 'reserved',
    revision: 3,
    reviewRequired: true,
  }
})

it('shows a durable receipt without claiming a physical start and requires a reason', async () => {
  const user = userEvent.setup()
  render(<DeviceCommands />)
  expect(screen.getByText('accepted')).toBeVisible()
  expect(screen.getByText(/These states do not verify physical hardware/)).toBeVisible()
  expect(screen.getByText(/timeout does not release/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Flag round for review' }))
  expect(screen.getByRole('button', { name: 'Hold for review' })).toBeDisabled()
  await user.type(
    screen.getByLabelText('Reason for review'),
    'Synthetic check of uncertain device state',
  )
  await user.click(screen.getByRole('button', { name: 'Hold for review' }))
  await waitFor(() => expect(mocks.refresh).toHaveBeenCalledOnce())
  expect(mocks.api).toHaveBeenCalledWith('/admin/sessions/synthetic-session/review', {
    method: 'POST',
    csrf: 'synthetic-csrf',
    body: {
      expectedRevision: 3,
      reason: 'Synthetic check of uncertain device state',
    },
  })
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
})

it('keeps stale revision failures visible rather than claiming review was saved', async () => {
  mocks.api.mockRejectedValue(new Error('The round changed. Refresh and review it again.'))
  const user = userEvent.setup()
  render(<DeviceCommands />)
  await user.click(screen.getByRole('button', { name: 'Flag round for review' }))
  await user.type(screen.getByLabelText('Reason for review'), 'Synthetic reason')
  await user.click(screen.getByRole('button', { name: 'Hold for review' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('The round changed')
  expect(screen.getByRole('dialog')).toBeVisible()
  expect(mocks.notify).not.toHaveBeenCalled()
})

it('keeps reviewed rounds held and offers no release or repeat-review control', () => {
  mocks.current.status = 'review'
  render(<DeviceCommands />)
  expect(screen.getByRole('status')).toHaveTextContent('Review hold active')
  expect(screen.queryByRole('button', { name: /review/i })).not.toBeInTheDocument()
})
