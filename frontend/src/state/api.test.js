import { afterEach, expect, it, vi } from 'vitest'
import { api } from './api'

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})
it('bounds a stalled request and allows a later request to succeed', async () => {
  vi.useFakeTimers()
  vi.stubGlobal(
    'fetch',
    vi.fn(
      (url, options) =>
        new Promise((resolve, reject) => {
          options.signal.addEventListener('abort', () =>
            reject(new DOMException('aborted', 'AbortError')),
          )
        }),
    ),
  )
  const pending = api('/player/context')
  const failure = expect(pending).rejects.toThrow('timed out')
  await vi.advanceTimersByTimeAsync(15001)
  await failure
  fetch.mockResolvedValue({ ok: true, json: async () => ({ revision: 2 }) })
  expect(await api('/player/context')).toEqual({ revision: 2 })
  expect(vi.getTimerCount()).toBe(0)
})

it('preserves explicit caller cancellation and removes its timer', async () => {
  vi.useFakeTimers()
  vi.stubGlobal(
    'fetch',
    vi.fn(
      (url, options) =>
        new Promise((resolve, reject) => {
          options.signal.addEventListener('abort', () =>
            reject(new DOMException('aborted', 'AbortError')),
          )
        }),
    ),
  )
  const controller = new AbortController()
  const pending = api('/admin/assistant/query', { signal: controller.signal })
  const failure = expect(pending).rejects.toMatchObject({ name: 'AbortError' })
  controller.abort()
  await failure
  expect(vi.getTimerCount()).toBe(0)
})

it('rejects invalid JSON and scalar payloads instead of corrupting application state', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => {
        throw new SyntaxError()
      },
    }),
  )
  await expect(api('/admin/snapshot')).rejects.toThrow('invalid response')
  fetch.mockResolvedValue({ ok: true, status: 200, json: async () => null })
  await expect(api('/admin/snapshot')).rejects.toThrow('invalid response')
})
