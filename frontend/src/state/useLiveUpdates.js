import { useEffect, useState } from 'react'

// Frames only invalidate REST state; they never supply queue, score or identity data.
export function useLiveUpdates(role, refresh) {
  const [status, setStatus] = useState('polling')
  useEffect(() => {
    if (!role || !window.WebSocket) {
      setStatus('polling')
      return
    }
    let disposed = false
    let socket
    let reconnect
    let watchdog
    let attempts = 0
    let revision = -1
    function connect() {
      if (disposed) return
      setStatus('connecting')
      const url = new URL(`/api/live/${role}`, window.location.href)
      url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
      try {
        socket = new window.WebSocket(url.href)
      } catch {
        retry()
        return
      }
      socket.onmessage = ({ data }) => {
        let frame
        try {
          frame = JSON.parse(data)
        } catch {
          return
        }
        if (
          !['ready', 'invalidate', 'heartbeat'].includes(frame.type) ||
          !Number.isSafeInteger(frame.revision) ||
          frame.revision < 0
        )
          return
        clearTimeout(watchdog)
        watchdog = setTimeout(() => socket.close(), 35000)
        setStatus('live')
        attempts = 0
        // Every handshake refetches, including after a dispatcher/server restart.
        if (frame.type === 'ready' || frame.revision > revision) refresh()
        revision = Math.max(revision, frame.revision)
      }
      socket.onclose = retry
      socket.onerror = () => socket.close()
      watchdog = setTimeout(() => socket.close(), 10000)
    }
    function retry() {
      clearTimeout(watchdog)
      if (disposed) return
      setStatus('polling')
      refresh()
      clearTimeout(reconnect)
      reconnect = setTimeout(connect, Math.min(30000, 1000 * 2 ** attempts++) + Math.random() * 250)
    }
    const reconnectOnNetwork = () => {
      clearTimeout(reconnect)
      clearTimeout(watchdog)
      if (socket) {
        socket.onclose = null
        socket.onerror = null
        socket.onmessage = null
        socket.close()
      }
      attempts = 0
      connect()
    }
    window.addEventListener('online', reconnectOnNetwork)
    connect()
    return () => {
      disposed = true
      clearTimeout(reconnect)
      clearTimeout(watchdog)
      window.removeEventListener('online', reconnectOnNetwork)
      if (socket) {
        socket.onclose = null
        socket.onerror = null
        socket.onmessage = null
        socket.close()
      }
    }
  }, [role, refresh])
  return status
}
