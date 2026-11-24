import { MemoryRouter } from 'react-router-dom'
import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Settings from './Settings'
import AdminAssistant from '../components/AdminAssistant'
import { AssistantProvider } from '../state/AssistantContext'
const mocks = vi.hoisted(() => ({ api: vi.fn(), queries: [], isAdmin: true, notify: vi.fn() }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({
    admin: { csrf: 'synthetic', role: mocks.isAdmin ? 'admin' : 'operator' },
    isAdmin: mocks.isAdmin,
    notify: mocks.notify,
    theme: 'light',
    setTheme: vi.fn(),
    refresh: vi.fn(),
  }),
}))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../components/AssistantTrainingReview', () => ({ default: () => null }))
beforeEach(() => {
  mocks.queries.length = 0
  mocks.isAdmin = true
  mocks.notify.mockClear()
  mocks.api.mockImplementation(async (path, options = {}) => {
    if (path.endsWith('/memory')) return { available: true, context: null, remembered: 0 }
    if (path.endsWith('/status')) return { available: true, reason: 'ready' }
    if (path === '/admin/staff' && !options.method)
      return {
        staff: [
          { id: 1, username: 'admin', role: 'admin', enabled: true },
          { id: 2, username: 'booth-1', role: 'operator', enabled: true },
        ],
      }
    if (path === '/admin/staff')
      return {
        staff: { id: 3, username: options.body.username, role: 'operator', enabled: true },
        password: 'abcd-efgh-jkmn-pqrs',
      }
    if (path === '/admin/staff/2/enabled')
      return { staff: { id: 2, username: 'booth-1', role: 'operator', enabled: false } }
    if (path.endsWith('/query')) {
      mocks.queries.push(options.body)
      return { status: 'conversation', answer: 'Hello from the event assistant.' }
    }
    throw Error('Unexpected test endpoint')
  })
})
it('places diagnostics, memory and review management in Settings', async () => {
  render(
    <MemoryRouter>
      <AssistantProvider>
        <Settings />
      </AssistantProvider>
    </MemoryRouter>,
  )
  expect(await screen.findByText('Local model ready')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Check connection' })).toBeInTheDocument()
  expect(screen.getByRole('checkbox', { name: 'Use private memory' })).toBeChecked()
  expect(screen.getByRole('button', { name: 'Forget saved memory' })).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Review questions' })).toHaveAttribute(
    'href',
    '/admin/question-review',
  )
  expect(screen.getByRole('button', { name: 'Training examples' })).toBeInTheDocument()
})
it('applies the Settings memory toggle to the shared chat session', async () => {
  const user = userEvent.setup()
  render(
    <MemoryRouter>
      <AssistantProvider>
        <Settings />
        <AdminAssistant />
      </AssistantProvider>
    </MemoryRouter>,
  )
  await screen.findByText('Local model ready')
  await user.click(screen.getByRole('checkbox', { name: 'Use private memory' }))
  await user.click(screen.getByRole('button', { name: /Stack Intelligence/ }))
  await user.type(screen.getByLabelText('Ask Stack Intelligence'), 'hello')
  await user.click(screen.getByRole('button', { name: 'Send question' }))
  await screen.findByText('Hello from the event assistant.')
  expect(mocks.queries[0].use_memory).toBe(false)
  expect(screen.queryByText('Review for training')).not.toBeInTheDocument()
})
it('lets an administrator add an operator, see the one-time password and switch an account off', async () => {
  const user = userEvent.setup()
  render(
    <MemoryRouter>
      <AssistantProvider>
        <Settings />
      </AssistantProvider>
    </MemoryRouter>,
  )
  const list = await screen.findByRole('list', { name: 'Staff accounts' })
  expect(list).toHaveTextContent('admin')
  expect(screen.queryByRole('button', { name: 'Switch off admin' })).not.toBeInTheDocument()
  await user.type(screen.getByLabelText('New operator username'), 'gate-2')
  await user.click(screen.getByRole('button', { name: 'Add operator' }))
  expect(mocks.api).toHaveBeenCalledWith('/admin/staff', {
    method: 'POST',
    csrf: 'synthetic',
    body: { username: 'gate-2' },
  })
  expect(await screen.findByRole('dialog')).toHaveTextContent('abcd-efgh-jkmn-pqrs')
  await user.click(screen.getByRole('button', { name: 'Done' }))
  expect(screen.queryByText('abcd-efgh-jkmn-pqrs')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Switch off booth-1' }))
  expect(await screen.findByText('Switched off')).toBeInTheDocument()
  expect(mocks.notify).toHaveBeenCalledWith('booth-1 is switched off and signed out.')
})
it('hides staff accounts, training and question review from operators', async () => {
  mocks.isAdmin = false
  render(
    <MemoryRouter>
      <AssistantProvider>
        <Settings />
      </AssistantProvider>
    </MemoryRouter>,
  )
  expect(await screen.findByText('Local model ready')).toBeInTheDocument()
  expect(screen.getByRole('checkbox', { name: 'Use private memory' })).toBeInTheDocument()
  expect(screen.queryByText('Staff accounts')).not.toBeInTheDocument()
  expect(screen.queryByRole('link', { name: 'Review questions' })).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Training examples' })).not.toBeInTheDocument()
  expect(mocks.api).not.toHaveBeenCalledWith('/admin/staff')
})
