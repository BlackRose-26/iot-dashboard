import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PlayerAssistant, { LobbyStatus } from './PlayerAssistant'

const mocks = vi.hoisted(() => ({ api: vi.fn() }))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))

beforeEach(() => {
  vi.clearAllMocks()
  mocks.api.mockImplementation(async (path, options = {}) => {
    if (path === '/player/lobby')
      return { inLine: 4, cabinet: 'ready', admissionsOpen: true, waitMinutes: 6 }
    return {
      answer: `Answer to: ${options.body.question}`,
      source: 'Game rules',
      suggestions: ['Top score today?', 'How do I play?'],
    }
  })
})

it('asks a suggested question, shows the sourced answer and hides that suggestion', async () => {
  const user = userEvent.setup()
  render(
    <PlayerAssistant
      greeting="Hi there!"
      suggestions={['How do I play?', 'How long is the wait?']}
    />,
  )
  expect(screen.getByRole('log')).toHaveTextContent('Hi there!')
  await user.click(screen.getByRole('button', { name: 'How do I play?' }))
  expect(mocks.api).toHaveBeenCalledWith('/player/assistant', {
    method: 'POST',
    body: { question: 'How do I play?' },
  })
  expect(await screen.findByText('Answer to: How do I play?')).toBeInTheDocument()
  expect(screen.getByText('Game rules')).toBeInTheDocument()
  // The server's suggestions replace the starters; ones already asked stay hidden.
  expect(screen.getByRole('button', { name: 'Top score today?' })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'How do I play?' })).not.toBeInTheDocument()
})

it('sends typed questions, ignores blanks and shows errors without losing the chat', async () => {
  const user = userEvent.setup()
  render(<PlayerAssistant suggestions={[]} />)
  const send = screen.getByRole('button', { name: 'Send question' })
  expect(send).toBeDisabled()
  await user.type(
    screen.getByLabelText('Ask Stack Intelligence a question'),
    'Paano maglaro?{Enter}',
  )
  expect(await screen.findByText('Answer to: Paano maglaro?')).toBeInTheDocument()
  expect(screen.getByLabelText('Ask Stack Intelligence a question')).toHaveValue('')

  mocks.api.mockRejectedValueOnce(new Error('That’s a lot of questions! Try again in a minute.'))
  await user.type(screen.getByLabelText('Ask Stack Intelligence a question'), 'hi{Enter}')
  expect(await screen.findByRole('alert')).toHaveTextContent('a lot of questions')
  expect(screen.getByText('Answer to: Paano maglaro?')).toBeInTheDocument()
})

it('compact mode shows only the latest exchange', async () => {
  const user = userEvent.setup()
  render(<PlayerAssistant compact greeting="Welcome" suggestions={['One?', 'Two?']} />)
  await user.click(screen.getByRole('button', { name: 'One?' }))
  await screen.findByText('Answer to: One?')
  await user.click(screen.getByRole('button', { name: 'Top score today?' }))
  await screen.findByText('Answer to: Top score today?')
  expect(screen.queryByText('Welcome')).not.toBeInTheDocument()
  expect(screen.queryByText('Answer to: One?')).not.toBeInTheDocument()
})

it('shows the live line, and says when joining is paused', async () => {
  const { unmount } = render(<LobbyStatus />)
  expect(await screen.findByText('4 in line')).toBeInTheDocument()
  expect(screen.getByText('Cabinet ready')).toBeInTheDocument()
  expect(screen.getByText('About 6 min wait')).toBeInTheDocument()
  unmount()
  mocks.api.mockResolvedValueOnce({
    inLine: 2,
    cabinet: 'ready',
    admissionsOpen: false,
    waitMinutes: 3,
  })
  render(<LobbyStatus />)
  await waitFor(() => expect(screen.getByText('Line paused')).toBeInTheDocument())
})
