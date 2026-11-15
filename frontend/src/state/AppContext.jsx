import { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react'
import { summarize } from '../data/demo'
import { api } from './api'

const AppContext = createContext(null)
const EMPTY = {
  queue: [],
  rounds: [],
  machineState: 'offline',
  admissionsOpen: false,
  currentPlayer: null,
  machine: {},
  qrPath: null,
}
export function AppProvider({ children }) {
  const [admin, setAdmin] = useState(null)
  const [ready, setReady] = useState(false)
  const [snapshot, setSnapshot] = useState(EMPTY)
  const [player, setPlayer] = useState({ ticket: null, canRegister: false, notifications: [] })
  const [connectionError, setConnectionError] = useState('')
  const [toast, setToast] = useState('')
  const [busy, setBusy] = useState(false)
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('smb-admin-theme') || 'light'
    } catch {
      return 'light'
    }
  })
  const notify = useCallback((message) => setToast(message), [])
  const checking = useRef(false)
  const refreshPlayer = useCallback(async () => {
    const data = await api('/player/context')
    setPlayer(data)
    return data
  }, [])
  const refresh = useCallback(async () => {
    if (checking.current) return
    checking.current = true
    try {
      const data = await api('/player/context')
      setPlayer(data)
      try {
        const auth = await api('/admin/session')
        setAdmin(auth)
        setSnapshot(await api('/admin/snapshot'))
      } catch (error) {
        if (error.status !== 401) throw error
        setAdmin(null)
        setSnapshot(EMPTY)
      }
      setConnectionError('')
    } catch (error) {
      setConnectionError(error.message)
    } finally {
      setReady(true)
      checking.current = false
    }
  }, [])
  useEffect(() => {
    refresh()
    const timer = setInterval(refresh, 2000)
    const focus = () => refresh()
    window.addEventListener('focus', focus)
    return () => {
      clearInterval(timer)
      window.removeEventListener('focus', focus)
    }
  }, [refresh])
  useEffect(() => {
    try {
      localStorage.setItem('smb-admin-theme', theme)
    } catch {}
  }, [theme])
  async function login(username, password) {
    const auth = await api('/admin/login', { method: 'POST', body: { username, password } })
    setAdmin(auth)
    setSnapshot(await api('/admin/snapshot'))
    setConnectionError('')
  }
  async function logout() {
    await api('/admin/logout', { method: 'POST', csrf: admin?.csrf })
    setAdmin(null)
    setSnapshot(EMPTY)
  }
  async function action(path, body, message) {
    if (busy) return
    setBusy(true)
    try {
      await api(path, { method: 'POST', body, csrf: admin?.csrf, key: crypto.randomUUID() })
      setSnapshot(await api('/admin/snapshot'))
      if (message) notify(message)
    } catch (error) {
      notify(error.message)
      if (error.status === 401) {
        setAdmin(null)
        setSnapshot(EMPTY)
      }
    } finally {
      setBusy(false)
    }
  }
  async function joinQueue(nickname, studentId, acknowledged) {
    await api('/player/register', {
      method: 'POST',
      body: { nickname, studentId, acknowledged },
      csrf: player.csrf,
    })
    await refreshPlayer()
  }
  async function cancelTicket() {
    await api('/player/cancel', { method: 'POST', csrf: player.csrf })
    await refreshPlayer()
  }
  return (
    <AppContext.Provider
      value={{
        ...snapshot,
        admin,
        ready,
        player,
        ticket: player.ticket,
        admissionsOpen: admin ? snapshot.admissionsOpen : player.admissionsOpen,
        login,
        logout,
        joinQueue,
        cancelTicket,
        refresh,
        refreshPlayer,
        theme,
        setTheme,
        busy,
        connectionError,
        toast,
        setToast,
        notify,
        callNext: () => action('/admin/queue/call-next', null, 'The next player has been called.'),
        skipPlayer: (id, reason) =>
          action(`/admin/queue/${id}/skip`, { reason }, 'Player removed from the waiting queue.'),
        setAdmissionsOpen: (open) => action('/admin/admissions', { open }),
        simulate: (name) =>
          action(
            `/admin/simulator/${name}`,
            null,
            `Simulator: ${name}. No physical device command sent.`,
          ),
        stats: summarize(snapshot.rounds),
      }}
    >
      {children}
    </AppContext.Provider>
  )
}
export function useApp() {
  return useContext(AppContext)
}
