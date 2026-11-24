import { useEffect, useState } from 'react'
import { api } from '../state/api'
import * as ui from './siteStyles'

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

const tile =
  'tw:border-[1.5px] tw:border-solid tw:border-night/16 tw:rounded-[22px] tw:px-4 tw:py-[14px] tw:max-[600px]:p-3 tw:flex tw:flex-col tw:gap-0.5 tw:min-w-0'
const tileLabel = 'tw:text-[13px] tw:font-semibold tw:text-night/68'
const tileValue =
  'tw:text-[24px] tw:max-[600px]:text-[20px] tw:font-extrabold tw:flex tw:items-center tw:gap-2'

export function LiveTiles() {
  const lobby = useLobby()
  if (!lobby) return null
  const paused = !lobby.admissionsOpen
  const ready = lobby.cabinet === 'ready'
  return (
    <div
      className={`tw:grid tw:grid-cols-3 tw:gap-2.5 tw:max-w-[540px] ${ui.enter} ${ui.delays[3]}`}
      role="status"
      aria-live="polite"
      aria-label="Live line status"
    >
      <div className={tile}>
        <small className={tileLabel}>In line</small>
        <strong className={tileValue}>{lobby.inLine}</strong>
      </div>
      <div className={tile}>
        <small className={tileLabel}>Wait</small>
        <strong className={tileValue}>
          {paused ? 'Paused' : lobby.inLine ? `~${Math.max(1, lobby.waitMinutes)} min` : 'None'}
        </strong>
      </div>
      <div className={tile}>
        <small className={tileLabel}>Cabinet</small>
        <strong className="tw:text-[17px] tw:max-[430px]:text-[15px] tw:pt-[5px] tw:font-extrabold tw:flex tw:items-center tw:gap-2">
          {ready ? (
            <span
              className="tw:w-2.5 tw:h-2.5 tw:flex-none tw:rounded-[5px] tw:bg-night tw:outline-[3px] tw:outline-solid tw:outline-lime tw:motion-safe:animate-ready-ring"
              aria-hidden="true"
            />
          ) : (
            <span
              className="tw:w-2.5 tw:h-2.5 tw:flex-none tw:rounded-[5px] tw:border-2 tw:border-solid tw:border-night"
              aria-hidden="true"
            />
          )}
          {cabinetLabels[lobby.cabinet] || 'Checking'}
        </strong>
      </div>
    </div>
  )
}

export function TodayStrip() {
  const lobby = useLobby()
  if (!lobby) return null
  const stat = 'tw:m-0 tw:flex tw:items-baseline tw:gap-2 tw:text-[15px]'
  return (
    <div className="tw:border-[1.5px] tw:border-solid tw:border-night tw:rounded-[28px] tw:px-6 tw:py-[18px] tw:flex tw:flex-wrap tw:gap-x-8 tw:gap-y-3 tw:items-center tw:justify-between">
      <h2 className="tw:m-0 tw:text-[20px] tw:font-extrabold">Today at the cabinet</h2>
      {lobby.bestToday == null ? (
        <p className={stat}>No rounds finished yet today. The first score could be yours.</p>
      ) : (
        <>
          <p className={stat}>
            <strong className="tw:text-[26px]">{lobby.bestToday}</strong>
            best score so far
          </p>
          <p className={stat}>
            <strong className="tw:text-[26px]">{lobby.topCount}</strong>
            {lobby.topCount === 1 ? 'player' : 'players'} reached all {lobby.levels} levels
          </p>
        </>
      )}
      <span className="tw:text-[14px] tw:font-bold tw:bg-lime tw:rounded-full tw:px-3.5 tw:py-2">
        Leaderboard unlocks after your round
      </span>
    </div>
  )
}

export function GameBand() {
  const lobby = useLobby()
  const levels = lobby?.levels ?? 15
  const seconds = lobby?.roundSeconds ?? 60
  return (
    <div className={ui.band}>
      <h2 id="rules" className={ui.bandTitle}>
        Stack it to the top.
      </h2>
      <div>
        <b className={ui.bandValue}>{levels}</b>
        <span className={ui.bandLabel}>levels to the top</span>
      </div>
      <div>
        <b className={ui.bandValue}>{seconds}s</b>
        <span className={ui.bandLabel}>on the clock</span>
      </div>
      <div>
        <b className={ui.bandValue}>1</b>
        <span className={ui.bandLabel}>point per level kept</span>
      </div>
    </div>
  )
}
