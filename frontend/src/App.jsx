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
import About from './pages/About'
import Contact from './pages/Contact'
import GameScreen from './pages/GameScreen'
import ChatWidget from './components/ChatWidget'
import { useApp } from './state/AppContext'
import { EmptyState } from './components/ui'

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
function AdministratorsOnly({ children }) {
  const { isAdmin } = useApp()
  if (isAdmin) return children
  return (
    <EmptyState
      headingAs="h1"
      title="Administrators only"
      description="Practice-question review is done by the event administrator. Your operator account runs the queue and the cabinet."
    />
  )
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
  // The game screen (Plan B) is a full-screen kiosk page: no chat robot or connection banner.
  const isScreen = pathname === '/screen'
  useLayoutEffect(() => {
    if (isAdmin) document.documentElement.dataset.adminTheme = theme
    else delete document.documentElement.dataset.adminTheme
    // The player website uses its own three-colour theme (Tailwind tokens in styles/tailwind.css).
    if (isAdmin) delete document.documentElement.dataset.site
    else document.documentElement.dataset.site = 'player'
    document.title = `${isAdmin ? 'Admin' : isScreen ? 'Game screen' : 'Play'} · Stack Moko Baby`
  }, [isAdmin, isScreen, theme])
  return (
    <>
      {connectionError && !isScreen && (
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
          <Route
            path="question-review"
            element={
              <AdministratorsOnly>
                <QuestionReview />
              </AdministratorsOnly>
            }
          />
        </Route>
        <Route path="/join/:token" element={<Entry />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/reenter" element={<Reenter />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/screen" element={<GameScreen />} />
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
      {!isAdmin && !isScreen && <ChatWidget />}
    </>
  )
}
