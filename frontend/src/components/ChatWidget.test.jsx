import { beforeEach, expect, it, vi } from 'vitest'
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import ChatWidget, { chatContext } from './ChatWidget'
import { openRobotChat } from './SiteSections'
import SiteHeader from './SiteHeader'

const mocks = vi.hoisted(() => ({ api: vi.fn(), ticket: null }))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../state/AppContext', () => ({ useApp: () => ({ ticket: mocks.ticket }) }))

function show(path = '/') {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <ChatWidget />
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  mocks.ticket = null
  mocks.api.mockResolvedValue({
    answer: 'Press the big button.',
    source: 'Game rules',
    suggestions: [],
  })
})

it('opens from the robot, answers, and closes back to the robot', async () => {
  const user = userEvent.setup()
  show()
  const launcher = screen.getByRole('button', { name: 'Open Stack Intelligence' })
  expect(launcher).toHaveAttribute('aria-expanded', 'false')
  expect(screen.getByText(/Questions while you wait/)).toBeInTheDocument()
  await user.click(launcher)
  expect(screen.getByRole('dialog', { name: 'Stack Intelligence' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Close Stack Intelligence' })).toHaveAttribute(
    'aria-expanded',
    'true',
  )
  expect(screen.queryByText(/Questions while you wait/)).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'How do I play?' }))
  expect(await screen.findByText('Press the big button.')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Close chat' }))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Open Stack Intelligence' })).toHaveFocus()
})

it('remembers a dismissed greeting and closes with Escape', async () => {
  const user = userEvent.setup()
  const { unmount } = show()
  await user.click(screen.getByRole('button', { name: 'Dismiss greeting' }))
  expect(screen.queryByText(/Questions while you wait/)).not.toBeInTheDocument()
  unmount()
  show()
  expect(screen.queryByText(/Questions while you wait/)).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Open Stack Intelligence' }))
  await user.keyboard('{Escape}')
  await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
})

it('opens from an "Ask the robot" button and stays quiet on the registration form', () => {
  show('/register')
  expect(screen.queryByText(/Questions while you wait/)).not.toBeInTheDocument()
  act(() => openRobotChat())
  expect(screen.getByRole('dialog', { name: 'Stack Intelligence' })).toBeInTheDocument()
})

it('suggestions follow the ticket', () => {
  expect(chatContext(null).suggestions).toContain('How long is the wait?')
  expect(chatContext({ status: 'waiting', position: 3 }).greeting).toContain('#3')
  expect(chatContext({ status: 'called' }).suggestions[0]).toBe('What do I do now?')
  expect(chatContext({ status: 'completed' }).suggestions[0]).toBe('How did I do?')
})

it('header shows Home, About and Contact, and a phone menu', async () => {
  const user = userEvent.setup()
  render(
    <MemoryRouter initialEntries={['/about']}>
      <SiteHeader />
    </MemoryRouter>,
  )
  const nav = screen.getByRole('navigation', { name: 'Main' })
  expect(nav).toHaveTextContent('HomeAboutContact')
  expect(screen.getByRole('link', { name: 'About' })).toHaveAttribute('aria-current', 'page')
  expect(screen.getByRole('link', { name: 'Scan to play' })).toHaveAttribute('href', '/scan')
  const menu = screen.getByRole('button', { name: 'Menu' })
  await user.click(menu)
  expect(menu).toHaveAttribute('aria-expanded', 'true')
})
