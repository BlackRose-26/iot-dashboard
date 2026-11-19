import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import Registration from './Registration'

const state = vi.hoisted(() => ({
  ready: true,
  admissionsOpen: true,
  player: { canRegister: true },
  ticket: null,
  joinQueue: vi.fn(),
}))
vi.mock('../state/AppContext', () => ({ useApp: () => state }))
function setup() {
  render(
    <MemoryRouter>
      <Registration />
    </MemoryRouter>,
  )
  return userEvent.setup()
}
beforeEach(() => {
  state.player.canRegister = true
  state.ticket = null
  state.joinQueue.mockReset()
  localStorage.clear()
  sessionStorage.clear()
})
describe('private player registration', () => {
  it('preserves a review-held ticket after scanning again', () => {
    state.ticket = { status: 'review' }
    setup()
    expect(screen.getByRole('link', { name: 'View my ticket' })).toBeVisible()
    expect(screen.queryByLabelText(/^Student ID/)).not.toBeInTheDocument()
  })
  it('focuses the first invalid field and describes all errors', async () => {
    const user = setup()
    await user.click(screen.getByRole('button', { name: 'Let’s stack' }))
    expect(screen.getByLabelText(/^Nickname/)).toHaveFocus()
    expect(screen.getAllByRole('alert')).toHaveLength(3)
  })
  it('masks the ID, sends it only to registration and clears it after a failure', async () => {
    state.joinQueue.mockRejectedValue(new Error('Admissions paused.'))
    const user = setup()
    const input = screen.getByLabelText(/^Student ID/)
    expect(input).toHaveAttribute('type', 'password')
    await user.type(screen.getByLabelText(/^Nickname/), 'Test Player')
    await user.type(input, 'DUMMY-TEST-0026')
    await user.click(screen.getByRole('checkbox'))
    await user.click(screen.getByRole('button', { name: 'Let’s stack' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Admissions paused.')
    expect(input).toHaveValue('')
    expect(state.joinQueue).toHaveBeenCalledWith('Test Player', 'DUMMY-TEST-0026', true)
    expect(localStorage.length + sessionStorage.length).toBe(0)
  })
  it('requires a server-issued QR entry before showing the form', () => {
    state.player.canRegister = false
    setup()
    expect(screen.queryByRole('form')).not.toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Your game starts with a scan.' }),
    ).toBeInTheDocument()
  })
})
