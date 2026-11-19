import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useLiveUpdates } from './useLiveUpdates'

let sockets
class FakeSocket {
  constructor(url) {
    this.url = url
    sockets.push(this)
  }
  frame(type, revision) {
    this.onmessage?.({ data: JSON.stringify({ type, revision }) })
  }
  close() {
    this.closed = true
    this.onclose?.()
  }
}
beforeEach(() => {
  sockets = []
  vi.useFakeTimers()
  vi.stubGlobal('WebSocket', FakeSocket)
})
afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('authorized live invalidations', () => {
  it('refetches on handshake, revision gaps and reconnect, ignoring duplicate hints', () => {
    const refresh = vi.fn()
    const { result, unmount } = renderHook(() => useLiveUpdates('player', refresh))
    expect(sockets[0].url).toMatch(/\/api\/live\/player$/)
    act(() => sockets[0].frame('ready', 4))
    expect(result.current).toBe('live')
    act(() => {
      sockets[0].frame('invalidate', 4)
      sockets[0].frame('invalidate', 9)
    })
    expect(refresh).toHaveBeenCalledTimes(2)
    act(() => sockets[0].close())
    expect(result.current).toBe('polling')
    act(() => vi.advanceTimersByTime(1300))
    act(() => sockets[1].frame('ready', 9))
    expect(result.current).toBe('live')
    expect(refresh).toHaveBeenCalledTimes(4)
    unmount()
    expect(sockets[1].closed).toBe(true)
    act(() => vi.advanceTimersByTime(60000))
    expect(sockets).toHaveLength(2)
  })

  it('closes a stalled stream and recovers when the network returns', () => {
    const refresh = vi.fn()
    const { result } = renderHook(() => useLiveUpdates('admin', refresh))
    act(() => sockets[0].frame('ready', 1))
    act(() => vi.advanceTimersByTime(35001))
    expect(result.current).toBe('polling')
    act(() => window.dispatchEvent(new Event('online')))
    expect(sockets).toHaveLength(2)
    act(() => sockets[1].frame('ready', 1))
    expect(result.current).toBe('live')
  })

  it('cleans up the staff stream when switching to a player or guest', () => {
    const refresh = vi.fn()
    const { rerender } = renderHook(({ role }) => useLiveUpdates(role, refresh), {
      initialProps: { role: 'admin' },
    })
    rerender({ role: 'player' })
    expect(sockets[0].closed).toBe(true)
    expect(sockets[1].url).toMatch(/\/api\/live\/player$/)
    rerender({ role: null })
    expect(sockets[1].closed).toBe(true)
    act(() => vi.advanceTimersByTime(60000))
    expect(sockets).toHaveLength(2)
  })

  it('ignores malformed frames and opens no unauthenticated channel', () => {
    const refresh = vi.fn()
    const { rerender } = renderHook(({ role }) => useLiveUpdates(role, refresh), {
      initialProps: { role: null },
    })
    expect(sockets).toHaveLength(0)
    rerender({ role: 'player' })
    act(() => {
      sockets[0].onmessage({ data: 'bad json' })
      sockets[0].frame('ready', -1)
      sockets[0].frame('queue', 4)
    })
    expect(refresh).not.toHaveBeenCalled()
  })
})
