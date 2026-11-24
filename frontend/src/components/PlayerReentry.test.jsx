import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PlayerReentry from './PlayerReentry'

const mocks = vi.hoisted(() => ({ api: vi.fn(), notify: vi.fn() }))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({ admin: { csrf: 'synthetic' }, notify: mocks.notify }),
}))

const TOKEN = 'S'.repeat(43)

beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockImplementation(async (path) => {
    if (path.startsWith('/admin/players?'))
      return {
        players: [
          {
            id: 'synthetic-player',
            nickname: 'Synthetic Ana',
            code: 'SMB-0001',
            ticket: 'waiting',
          },
        ],
      }
    return { path: `/reenter#${TOKEN}`, expiresAt: '2026-11-24T10:10:00Z', minutes: 10 }
  })
})

it('finds a player and shows a one-time QR without exposing the code as text', async () => {
  const user = userEvent.setup()
  render(<PlayerReentry />)
  await user.type(screen.getByLabelText('Find a player to restore'), 'Ana')
  expect(await screen.findByText('Synthetic Ana')).toBeInTheDocument()
  expect(screen.getByText(/SMB-0001 · In line/)).toBeInTheDocument()
  expect(mocks.api).toHaveBeenCalledWith('/admin/players?search=Ana')

  await user.click(screen.getByRole('button', { name: 'Show re-entry QR for Synthetic Ana' }))
  await waitFor(() =>
    expect(mocks.api).toHaveBeenCalledWith('/admin/players/synthetic-player/reentry', {
      method: 'POST',
      csrf: 'synthetic',
    }),
  )
  const dialog = await screen.findByRole('dialog')
  expect(dialog).toHaveTextContent('Re-entry for Synthetic Ana')
  expect(dialog).toHaveTextContent(/works once/i)
  expect(dialog.textContent).not.toContain(TOKEN)

  await user.click(screen.getByRole('button', { name: 'Done' }))
  await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
  expect(mocks.notify).toHaveBeenCalledWith(expect.stringContaining('Synthetic Ana'))
})

it('shows the server error when a code cannot be issued', async () => {
  mocks.api.mockImplementation(async (path) => {
    if (path.startsWith('/admin/players?'))
      return {
        players: [{ id: 'gone', nickname: 'Synthetic Ben', code: 'SMB-0002', ticket: null }],
      }
    throw new Error('Player not found.')
  })
  const user = userEvent.setup()
  render(<PlayerReentry />)
  await user.type(screen.getByLabelText('Find a player to restore'), 'Ben')
  expect(await screen.findByText(/No ticket yet/)).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: /re-entry qr for synthetic ben/i }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Player not found.')
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
})
