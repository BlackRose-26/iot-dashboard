import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NoShowRelease from './NoShowRelease'

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

const called = (recovery = {}) => ({
  currentPlayer: {
    source: 'device',
    status: 'reserved',
    sessionId: 'synthetic-session',
    nickname: 'Synthetic Ana',
  },
  deviceRecovery: {
    bootId: 'synthetic-boot',
    revision: 4,
    canFence: true,
    allowedActions: [],
    evidenceId: null,
    quarantined: false,
    ...recovery,
  },
})

beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockResolvedValue({ ok: true })
  mocks.refresh.mockResolvedValue(undefined)
  mocks.state = called()
})

it('is hidden for simulator rounds and when nobody is called', () => {
  mocks.state = { ...called(), currentPlayer: { ...called().currentPlayer, source: 'simulator' } }
  const { container, rerender } = render(<NoShowRelease />)
  expect(container).toBeEmptyDOMElement()
  mocks.state = { currentPlayer: null, deviceRecovery: null }
  rerender(<NoShowRelease />)
  expect(container).toBeEmptyDOMElement()
})

it('stops first and releases only after the cabinet confirms the game never started', async () => {
  const user = userEvent.setup()
  const { rerender } = render(<NoShowRelease />)
  await user.click(screen.getByRole('button', { name: /player didn't come/i }))
  expect(screen.getByLabelText(/reason/i)).toHaveValue('Player did not come to the cabinet')
  await user.click(screen.getByRole('button', { name: 'Stop and release' }))
  await waitFor(() =>
    expect(mocks.api).toHaveBeenCalledWith(
      '/admin/sessions/synthetic-session/fence',
      expect.objectContaining({
        method: 'POST',
        body: { expectedRevision: 4, reason: 'Player did not come to the cabinet' },
      }),
    ),
  )
  expect(mocks.api).toHaveBeenCalledOnce()
  expect(screen.getByText(/waiting for the cabinet to confirm/i)).toBeInTheDocument()

  mocks.state = called({
    revision: 5,
    allowedActions: ['release_unstarted'],
    evidenceId: 'synthetic-evidence',
  })
  rerender(<NoShowRelease />)
  await waitFor(() =>
    expect(mocks.api).toHaveBeenLastCalledWith(
      '/admin/sessions/synthetic-session/resolve',
      expect.objectContaining({
        body: {
          expectedRevision: 5,
          reason: 'Player did not come to the cabinet',
          evidenceId: 'synthetic-evidence',
          action: 'release_unstarted',
        },
      }),
    ),
  )
  await waitFor(() => expect(mocks.notify).toHaveBeenCalledWith(expect.stringMatching(/no score/)))
})

it('never releases a round the cabinet reports as started', async () => {
  const user = userEvent.setup()
  const { rerender } = render(<NoShowRelease />)
  await user.click(screen.getByRole('button', { name: /player didn't come/i }))
  await user.click(screen.getByRole('button', { name: 'Stop and release' }))
  await waitFor(() => expect(mocks.api).toHaveBeenCalledOnce())
  mocks.state = called({
    revision: 5,
    allowedActions: ['void_interrupted'],
    evidenceId: 'synthetic-evidence',
  })
  rerender(<NoShowRelease />)
  expect(await screen.findByText(/had already started/i)).toBeInTheDocument()
  expect(mocks.api).toHaveBeenCalledOnce()
})

it('releases directly when the stop was already confirmed', async () => {
  mocks.state = called({
    revision: 6,
    allowedActions: ['release_unstarted'],
    evidenceId: 'synthetic-evidence',
  })
  const user = userEvent.setup()
  render(<NoShowRelease />)
  await user.click(screen.getByRole('button', { name: /player didn't come/i }))
  await user.click(screen.getByRole('button', { name: 'Stop and release' }))
  await waitFor(() => expect(mocks.api).toHaveBeenCalledOnce())
  expect(mocks.api.mock.calls[0][0]).toBe('/admin/sessions/synthetic-session/resolve')
})
