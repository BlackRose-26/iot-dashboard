import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
import { api } from './api'
import { useApp } from './AppContext'

const Context = createContext(null)
export function AssistantProvider({ children }) {
  const { admin } = useApp()
  const [useMemory, setUseMemory] = useState(true)
  const [memory, setMemory] = useState(null)
  const [memoryBusy, setMemoryBusy] = useState(false)
  const [memoryError, setMemoryError] = useState('')
  const [forgetRevision, setForgetRevision] = useState(0)
  const [pending, setPending] = useState(false)
  const [candidate, setCandidate] = useState(null)
  const [service, setService] = useState({ reason: 'checking', available: false })
  const controller = useRef(null)
  const timer = useRef(null)
  const memoryGeneration = useRef(0)
  const loadMemory = useCallback(async () => {
    const generation = memoryGeneration.current
    try {
      const state = await api('/admin/assistant/memory')
      if (generation !== memoryGeneration.current) return null
      setMemory(state)
      setMemoryError('')
      return state
    } catch {
      if (generation === memoryGeneration.current)
        setMemoryError('Saved memory is unavailable. You can still chat.')
      return null
    }
  }, [])
  const checkConnection = useCallback(
    async (prepare = true) => {
      controller.current?.abort()
      clearTimeout(timer.current)
      const request = new AbortController()
      controller.current = request
      setService({ reason: 'checking', available: false })
      async function inspect(allowPrepare) {
        try {
          let state = await api('/admin/assistant/status', { signal: request.signal })
          if (allowPrepare && state.installed && !state.available && state.reason !== 'warming') {
            state = await api('/admin/assistant/prepare', {
              method: 'POST',
              csrf: admin?.csrf,
              signal: request.signal,
            })
          }
          if (controller.current !== request || request.signal.aborted) return
          setService(state)
          if (state.reason === 'warming')
            timer.current = setTimeout(() => void inspect(false), 1500)
        } catch (error) {
          if (
            controller.current === request &&
            !request.signal.aborted &&
            error.name !== 'AbortError'
          )
            setService({ reason: 'ollama_unavailable', available: false })
        }
      }
      await inspect(prepare)
    },
    [admin?.csrf],
  )
  useEffect(
    () => () => {
      controller.current?.abort()
      clearTimeout(timer.current)
      memoryGeneration.current++
    },
    [],
  )
  async function forgetMemory() {
    memoryGeneration.current++
    setMemoryBusy(true)
    setMemoryError('')
    try {
      const cleared = await api('/admin/assistant/memory', { method: 'DELETE', csrf: admin?.csrf })
      memoryGeneration.current++
      setMemory(cleared)
      setCandidate(null)
      setForgetRevision((value) => value + 1)
    } catch {
      setMemoryError('Could not forget saved memory. Please try again.')
    } finally {
      setMemoryBusy(false)
    }
  }
  return (
    <Context.Provider
      value={{
        useMemory,
        setUseMemory,
        memory,
        setMemory,
        loadMemory,
        memoryBusy,
        memoryError,
        forgetMemory,
        forgetRevision,
        service,
        setService,
        checkConnection,
        pending,
        setPending,
        candidate,
        setCandidate,
      }}
    >
      {children}
    </Context.Provider>
  )
}
export const useAssistant = () => useContext(Context)
export const assistantStatus = {
  ready: 'Local model ready',
  model_missing: 'Download the configured model in Ollama',
  ollama_unavailable: 'Open Ollama to use the assistant',
  disabled: 'Assistant disabled',
  checking: 'Checking local model…',
  not_loaded: 'Local model needs loading',
  not_prepared: 'Local model needs preparation',
  warming: 'Loading local model…',
  warmup_failed: 'Model loading failed; check connection to retry',
}
