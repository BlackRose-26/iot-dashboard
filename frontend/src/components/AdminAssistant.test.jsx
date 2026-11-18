import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AdminAssistant from './AdminAssistant'
import { AssistantProvider } from '../state/AssistantContext'

const mocks = vi.hoisted(() => ({ api: vi.fn(), queries: [] }))
vi.mock('../state/AppContext', () => ({
  useApp: () => ({ admin: { csrf: 'synthetic-only' }, refresh: vi.fn() }),
}))
vi.mock('../state/api', () => ({ api: (...args) => mocks.api(...args) }))
vi.mock('./AssistantTrainingReview', () => ({ default: () => null }))
beforeEach(() => {
  mocks.queries.length = 0
  mocks.api.mockImplementation(async (path, options = {}) => {
    if (path.endsWith('/memory')) return { context: null, available: true }
    if (path.endsWith('/status')) return { reason: 'ready', available: true }
    if (path.endsWith('/query')) {
      mocks.queries.push(options.body)
      if (options.body.question === 'What is our accuracy?')
        return {
          status: 'needs_clarification',
          answer: 'I can read that two ways.',
          reason: 'two_interpretations',
          interpretations: [
            { label: 'Overall game accuracy', question: 'Show overall overlap accuracy.' },
            { label: 'Accuracy by level', question: 'Show overlap accuracy by level.' },
          ],
        }
      return { status: 'conversation', answer: 'Hi! How can I help?' }
    }
    throw new Error('Unexpected test endpoint')
  })
})
async function openChat() {
  const user = userEvent.setup()
  render(
    <AssistantProvider>
      <AdminAssistant />
    </AssistantProvider>,
  )
  await user.click(screen.getByRole('button', { name: /Stack Intelligence/ }))
  expect(screen.queryByText('Check connection')).not.toBeInTheDocument()
  return user
}
it('answers a greeting without interpretation choices or context dropdowns', async () => {
  const user = await openChat()
  await user.type(screen.getByLabelText('Ask Stack Intelligence'), 'hello')
  await user.click(screen.getByRole('button', { name: 'Send question' }))
  await screen.findByText('Hi! How can I help?')
  expect(screen.queryByLabelText('Choose the intended meaning')).not.toBeInTheDocument()
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  expect(mocks.queries[0]).not.toHaveProperty('period')
  expect(mocks.queries[0]).not.toHaveProperty('source')
})
it('offers exactly two interpretations and sends the chosen question', async () => {
  const user = await openChat()
  await user.type(screen.getByLabelText('Ask Stack Intelligence'), 'What is our accuracy?')
  await user.click(screen.getByRole('button', { name: 'Send question' }))
  const choices = await screen.findByLabelText('Choose the intended meaning')
  expect(within(choices).getAllByRole('button')).toHaveLength(2)
  await user.click(within(choices).getByRole('button', { name: 'Accuracy by level' }))
  await screen.findByText('Hi! How can I help?')
  expect(mocks.queries[1].question).toBe('Show overlap accuracy by level.')
})
