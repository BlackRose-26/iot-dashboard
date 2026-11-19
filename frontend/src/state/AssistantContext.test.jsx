import { act, renderHook } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import { AssistantProvider, useAssistant } from './AssistantContext'
import { api } from './api'
vi.mock('./api', () => ({ api: vi.fn() }))
vi.mock('./AppContext', () => ({ useApp: () => ({ admin: { csrf: 'synthetic' } }) }))
afterEach(() => vi.clearAllMocks())
const wrapper = ({ children }) => <AssistantProvider>{children}</AssistantProvider>

it('does not restore an older memory read after Forget succeeds', async () => {
  let release
  const held = new Promise((resolve) => {
    release = resolve
  })
  api.mockImplementation((path, options = {}) =>
    options.method === 'DELETE' ? Promise.resolve({ remembered: 0, context: null }) : held,
  )
  const { result } = renderHook(useAssistant, { wrapper })
  let loading
  act(() => {
    loading = result.current.loadMemory()
  })
  await act(async () => result.current.forgetMemory())
  await act(async () => {
    release({ remembered: 7, context: { tools: ['get_queue_summary'] } })
    await loading
  })
  expect(result.current.memory).toMatchObject({ remembered: 0, context: null })
})

it('ignores a late failure from an obsolete model-status check', async () => {
  let rejectFirst
  const held = new Promise((resolve, reject) => {
    rejectFirst = reject
  })
  api.mockReturnValueOnce(held).mockResolvedValue({ reason: 'ready', available: true })
  const { result } = renderHook(useAssistant, { wrapper })
  let first
  act(() => {
    first = result.current.checkConnection(false)
  })
  await act(async () => result.current.checkConnection(false))
  await act(async () => {
    rejectFirst(new Error('old failure'))
    await first
  })
  expect(result.current.service).toMatchObject({ reason: 'ready', available: true })
})
