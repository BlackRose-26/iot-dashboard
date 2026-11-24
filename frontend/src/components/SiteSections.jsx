import { useEffect, useState } from 'react'
import { api } from '../state/api'

// Shared pieces of the player website (Home, About). Live numbers come from the public,
// aggregate-only /api/player/lobby endpoint; nothing here shows another player's data.
export const OPEN_CHAT_EVENT = 'smb:open-chat'
export function openRobotChat() {
  window.dispatchEvent(new Event(OPEN_CHAT_EVENT))
}

export const steps = [
  ['Scan the code', 'Use the QR on the screen beside Cabinet 01. No app, no account.'],
  ['Save your spot', 'Pick a nickname. Your ticket shows your place and the wait.'],
  ['Play when called', 'Your phone tells you when it’s your turn. Press the big button.'],
]

let shared = null
const listeners = new Set()
let timer = null
function load() {
  api('/player/lobby')
    .then((data) => {
      shared = data
      listeners.forEach((listener) => listener(data))
    })
    .catch(() => {})
}

// One request every 15 s, shared by every component that shows lobby numbers.
export function useLobby() {
  const [lobby, setLobby] = useState(shared)
  useEffect(() => {
    listeners.add(setLobby)
    if (listeners.size === 1) {
      load()
      timer = setInterval(load, 15000)
    } else if (shared) setLobby(shared)
    return () => {
      listeners.delete(setLobby)
      if (!listeners.size) {
        clearInterval(timer)
        timer = null
      }
    }
  }, [])
  return lobby
}

const cabinetLabels = { ready: 'Ready', busy: 'Busy', offline: 'Offline' }

export function LiveTiles() {
  const lobby = useLobby()
  if (!lobby) return null
  const paused = !lobby.admissionsOpen
  return (
    <div className="live-tiles" role="status" aria-live="polite" aria-label="Live line status">
      <div>
        <small>In line</small>
        <strong>{lobby.inLine}</strong>
      </div>
      <div>
        <small>Wait</small>
        <strong>
          {paused ? 'Paused' : lobby.inLine ? `~${Math.max(1, lobby.waitMinutes)} min` : 'None'}
        </strong>
      </div>
      <div>
        <small>Cabinet</small>
        <strong className="state">
          <span
            className={`live-dot ${lobby.cabinet === 'ready' ? '' : 'off'}`}
            aria-hidden="true"
          />
          {cabinetLabels[lobby.cabinet] || 'Checking'}
        </strong>
      </div>
    </div>
  )
}

export function TodayStrip() {
  const lobby = useLobby()
  if (!lobby) return null
  return (
    <div className="today-strip">
      <h2>Today at the cabinet</h2>
      {lobby.bestToday == null ? (
        <p>No rounds finished yet today. The first score could be yours.</p>
      ) : (
        <>
          <p>
            <strong>{lobby.bestToday}</strong>
            best score so far
          </p>
          <p>
            <strong>{lobby.topCount}</strong>
            {lobby.topCount === 1 ? 'player' : 'players'} reached all {lobby.levels} levels
          </p>
        </>
      )}
      <span className="tag">Leaderboard unlocks after your round</span>
    </div>
  )
}

export function GameBand() {
  const lobby = useLobby()
  const levels = lobby?.levels ?? 15
  const seconds = lobby?.roundSeconds ?? 60
  return (
    <div className="site-band">
      <h2 id="rules">Stack it to the top.</h2>
      <div>
        <b>{levels}</b>
        <span>levels to the top</span>
      </div>
      <div>
        <b>{seconds}s</b>
        <span>on the clock</span>
      </div>
      <div>
        <b>1</b>
        <span>point per level kept</span>
      </div>
    </div>
  )
}
