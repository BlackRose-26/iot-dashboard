import QuestionReview from './pages/QuestionReview'
import { useLayoutEffect } from 'react'
import { Routes, Route, Navigate, Outlet, useLocation } from 'react-router-dom'
import Shell from './components/Shell'
import Overview from './pages/Overview'
import Analytics from './pages/Analytics'
import Queue from './pages/Queue'
import Sessions from './pages/Sessions'
import Machines from './pages/Machines'
import Settings from './pages/Settings'
import Registration from './pages/Registration'
import Leaderboard from './pages/Leaderboard'
import Ticket from './pages/Ticket'
import AdminLogin from './pages/AdminLogin'
import Entry, { ScanGate } from './pages/Entry'
import Reenter from './pages/Reenter'
import { useApp } from './state/AppContext'

function AdminOnly() {
  const { admin, ready } = useApp()
  const { pathname } = useLocation()
  if (!ready)
    return (
      <div className="page-loading" role="status">
        Checking your session…
      </div>
    )
  if (!admin)
    return (
      <Navigate
        to="/admin/login"
        state={{ reviewQuestions: pathname === '/admin/question-review' }}
        replace
      />
    )
  return <Shell />
}
function PlayerOnly({ completed = false }) {
  const { player, ready } = useApp()
  if (!ready)
    return (
      <div className="page-loading" role="status">
        Finding your ticket…
      </div>
    )
  if (!player.ticket) return <ScanGate />
  if (completed && player.ticket.status !== 'completed') return <Navigate to="/ticket" replace />
  return <Outlet />
}
export default function App() {
  const { pathname } = useLocation()
  const { theme, connectionError } = useApp()
  const isAdmin = pathname.startsWith('/admin')
  useLayoutEffect(() => {
    if (isAdmin) document.documentElement.dataset.adminTheme = theme
    else delete document.documentElement.dataset.adminTheme
    document.title = `${isAdmin ? 'Admin' : 'Play'} · Stack Moko Baby`
  }, [isAdmin, theme])
  return (
    <>
      {connectionError && (
        <div className="connection-banner" role="alert">
          {connectionError}
        </div>
      )}
      <Routes>
        <Route path="/" element={<ScanGate />} />
        <Route path="/scan" element={<ScanGate />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<AdminOnly />}>
          <Route index element={<Navigate to="overview" replace />} />
          <Route path="overview" element={<Overview />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="queue" element={<Queue />} />
          <Route path="sessions" element={<Sessions />} />
          <Route path="machines" element={<Machines />} />
          <Route path="settings" element={<Settings />} />
          <Route path="question-review" element={<QuestionReview />} />
        </Route>
        <Route path="/join/:token" element={<Entry />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/reenter" element={<Reenter />} />
        <Route path="/register/:eventCode/:machineCode" element={<ScanGate />} />
        <Route element={<PlayerOnly />}>
          <Route path="/ticket" element={<Ticket />} />
        </Route>
        <Route element={<PlayerOnly completed />}>
          <Route path="/leaderboard/acs-day" element={<Leaderboard />} />
        </Route>
        <Route
          path="*"
          element={
            <ScanGate message="This page is unavailable. Scan the current cabinet QR code to continue." />
          }
        />
      </Routes>
    </>
  )
}
