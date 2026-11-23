import { MemoryRouter } from 'react-router-dom'
import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Settings from './Settings'
import AdminAssistant from '../components/AdminAssistant'
import { AssistantProvider } from '../state/AssistantContext'
const mocks = vi.hoisted(() => ({ api: vi.fn(), queries: [] }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({
    admin: { csrf: 'synthetic' },
    theme: 'light',
    setTheme: vi.fn(),
    refresh: vi.fn(),
  }),
}))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('../components/AssistantTrainingReview', () => ({ default: () => null }))
beforeEach(() => {
  mocks.queries.length = 0
  mocks.api.mockImplementation(async (path, options = {}) => {
    if (path.endsWith('/memory')) return { available: true, context: null, remembered: 0 }
    if (path.endsWith('/status')) return { available: true, reason: 'ready' }
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
