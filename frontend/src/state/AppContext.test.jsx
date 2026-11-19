import { act, renderHook, waitFor } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import { AppProvider, useApp } from './AppContext'
import { api } from './api'

vi.mock('./api', () => ({ api: vi.fn() }))
vi.mock('./useLiveUpdates', () => ({ useLiveUpdates: () => 'polling' }))
afterEach(() => vi.clearAllMocks())
const denied = () => Promise.reject(Object.assign(new Error('sign in'), { status: 401 }))
const wrapper = ({ children }) => <AppProvider>{children}</AppProvider>

it('coalesces hints arriving during a fetch into a follow-up snapshot', async () => {
  let release
  const held = new Promise((resolve) => {
    release = resolve
  })
  let reads = 0
  api.mockImplementation((path) => {
    if (path === '/admin/session') return denied()
    return ++reads === 1 ? held : Promise.resolve({ revision: 2, ticket: { id: 'own-ticket' } })
  })
  const { result } = renderHook(useApp, { wrapper })
  act(() => {
    void result.current.refresh()
    void result.current.refresh()
  })
  await act(async () => release({ revision: 1, ticket: null }))
  await waitFor(() => expect(result.current.player.revision).toBe(2))
  expect(reads).toBe(2)
})

it('keeps the newest committed view when an older response arrives later', async () => {
  let rev = 5
  api.mockImplementation((path) =>
    path === '/admin/session'
      ? denied()
      : Promise.resolve({
          revision: rev,
          ticket: { id: 'own-ticket', status: rev === 5 ? 'completed' : 'playing' },
        }),
  )
  const { result } = renderHook(useApp, { wrapper })
  await waitFor(() => expect(result.current.ready).toBe(true))
  rev = 4
  await act(async () => result.current.refreshPlayer())
  expect(result.current.ticket.status).toBe('completed')
  expect(result.current.revision).toBe(5)
})
