import { useApp } from '../state/AppContext'

export default function UpdateStatus() {
  const { liveStatus, lastUpdated, connectionError } = useApp()
  const time = lastUpdated
    ? new Date(lastUpdated).toLocaleTimeString('en-PH', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
    : null
  return (
    <span className="subtle" title="Updates resume automatically when your connection returns.">
      {connectionError
        ? 'Connection interrupted'
        : liveStatus === 'live'
          ? 'Live updates'
          : 'Checking for updates'}
      {time && ` · Updated ${time}`}
    </span>
  )
}
