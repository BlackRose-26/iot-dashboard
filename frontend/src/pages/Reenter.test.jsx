import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { StrictMode } from 'react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import Reenter from './Reenter'

const mocks = vi.hoisted(() => ({ api: vi.fn(), refreshPlayer: vi.fn() }))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../state/AppContext', () => ({ useApp: () => ({ refreshPlayer: mocks.refreshPlayer }) }))
vi.mock('./Leaderboard', () => ({ PublicHeader: () => null }))

const TOKEN = 'S'.repeat(43)

function open(hash) {
  window.history.replaceState(null, '', `/reenter${hash}`)
  return render(
    <StrictMode>
      <MemoryRouter initialEntries={['/reenter']}>
        <Routes>
          <Route path="/reenter" element={<Reenter />} />
          <Route path="/ticket" element={<p>Ticket page</p>} />
        </Routes>
      </MemoryRouter>
    </StrictMode>,
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockResolvedValue({ ok: true })
  mocks.refreshPlayer.mockResolvedValue(undefined)
})

it('redeems the code once, clears it from the address bar and opens the ticket', async () => {
  open(`#${TOKEN}`)
  expect(window.location.hash).toBe('')
  expect(await screen.findByText('Ticket page')).toBeInTheDocument()
  expect(mocks.api).toHaveBeenCalledTimes(1)
  expect(mocks.api).toHaveBeenCalledWith('/player/reenter', {
    method: 'POST',
    body: { token: TOKEN },
  })
  expect(mocks.refreshPlayer).toHaveBeenCalled()
})

it('explains an expired or incomplete code and points back to the cabinet QR', async () => {
  mocks.api.mockRejectedValue(new Error('This re-entry code has expired or was already used.'))
  open(`#${TOKEN}`)
  expect(await screen.findByText(/expired or was already used/)).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /scan the cabinet qr/i })).toHaveAttribute(
    'href',
    '/scan',
  )

  mocks.api.mockClear()
  open('#short')
  await waitFor(() => expect(screen.getByText(/link is incomplete/)).toBeInTheDocument())
  expect(mocks.api).not.toHaveBeenCalled()
})
