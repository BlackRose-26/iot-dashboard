import { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react'
import { summarize } from '../data/demo'
import { api } from './api'
import { useLiveUpdates } from './useLiveUpdates'
import { CLASSIC_GAME } from './game'

const AppContext = createContext(null)
function newest(previous, data) {
  if ((previous.revision ?? -1) > data.revision) return previous
  if (previous.revision === data.revision && previous.generatedAt > data.generatedAt)
    return previous
  return data
}
const EMPTY = {
  queue: [],
  rounds: [],
  machineState: 'offline',
  admissionsOpen: false,
  currentPlayer: null,
  deviceCommands: [],
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
  const pending = useRef(false)
  const authEpoch = useRef(0)
  const acceptPlayer = useCallback((data) => {
    setPlayer((previous) => newest(previous, data))
  }, [])
  const acceptSnapshot = useCallback((data) => {
    setSnapshot((previous) => newest(previous, data))
  }, [])
  const refreshPlayer = useCallback(async () => {
    const data = await api('/player/context')
    acceptPlayer(data)
    return data
  }, [acceptPlayer])
  const refresh = useCallback(async () => {
    pending.current = true
    if (checking.current) return checking.current
    const work = async () => {
      do {
        pending.current = false
        const epoch = authEpoch.current
        try {
          const data = await api('/player/context')
          acceptPlayer(data)
          try {
            const auth = await api('/admin/session')
            const latest = await api('/admin/snapshot')
            if (epoch === authEpoch.current) {
              setAdmin(auth)
              acceptSnapshot(latest)
            }
          } catch (error) {
            if (error.status !== 401) throw error
            if (epoch === authEpoch.current) {
              setAdmin(null)
              setSnapshot(EMPTY)
            }
          }
          setConnectionError('')
        } catch (error) {
          setConnectionError(error.message)
        } finally {
          setReady(true)
        }
      } while (pending.current)
    }
    checking.current = work()
    try {
      await checking.current
    } finally {
      checking.current = false
    }
  }, [acceptPlayer, acceptSnapshot])
  const liveStatus = useLiveUpdates(admin ? 'admin' : player.ticket ? 'player' : null, refresh)
  useEffect(() => {
    refresh()
    const timer = setInterval(refresh, liveStatus === 'live' ? 15000 : 2000)
    const focus = () => refresh()
    window.addEventListener('focus', focus)
    return () => {
      clearInterval(timer)
      window.removeEventListener('focus', focus)
    }
  }, [refresh, liveStatus])
  useEffect(() => {
    try {
      localStorage.setItem('smb-admin-theme', theme)
    } catch {}
  }, [theme])
  async function login(username, password) {
    authEpoch.current++
    const auth = await api('/admin/login', { method: 'POST', body: { username, password } })
    authEpoch.current++
    setAdmin(auth)
    acceptSnapshot(await api('/admin/snapshot'))
    setConnectionError('')
  }
  async function logout() {
    authEpoch.current++
    await api('/admin/logout', { method: 'POST', csrf: admin?.csrf })
    authEpoch.current++
    setAdmin(null)
    setSnapshot(EMPTY)
  }
  async function action(path, body, message) {
    if (busy) return
    setBusy(true)
    try {
      await api(path, { method: 'POST', body, csrf: admin?.csrf, key: crypto.randomUUID() })
      await refresh()
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
        game: (admin ? snapshot.game : player.game) || CLASSIC_GAME,
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
        liveStatus,
        revision: admin ? snapshot.revision : player.revision,
        lastUpdated: admin ? snapshot.generatedAt : player.generatedAt,
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
