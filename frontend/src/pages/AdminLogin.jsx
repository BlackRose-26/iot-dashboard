import { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useApp } from '../state/AppContext'
import { Logo, Card, Button, IconButton } from '../components/ui'

export function ThemeSwitch() {
  const { theme, setTheme } = useApp()
  return (
    <IconButton
      label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      <i className={`fa-solid fa-${theme === 'dark' ? 'sun' : 'moon'}`} aria-hidden="true" />
    </IconButton>
  )
}
export default function AdminLogin() {
  const { admin, login, connectionError } = useApp()
  const navigate = useNavigate()
  const destination =
    useLocation().state?.reviewQuestions === true ? '/admin/question-review' : '/admin/overview'
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  if (admin) return <Navigate to={destination} replace />
  async function submit(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      await login(username, password)
      setPassword('')
      navigate(destination, { replace: true })
    } catch (e) {
      setError(e.message)
      setPassword('')
    } finally {
      setSubmitting(false)
    }
  }
  return (
    <div className="admin-login">
      <header>
        <Logo destination="/admin/login" />
        <ThemeSwitch />
      </header>
      <main id="main-content">
        <Card className="login-card">
          <span className="login-lock">
            <i className="fa-solid fa-lock" aria-hidden="true" />
          </span>
          <span className="eyebrow">OPERATOR ACCESS</span>
          <h1>Welcome back.</h1>
          <p>Sign in to manage the carnival.</p>
          <form className="tw:min-w-0" onSubmit={submit} aria-label="Admin sign in">
            <label className="field-label" htmlFor="admin-username">
              Username
            </label>
            <input
              id="admin-username"
              className="text-input tw:w-full tw:text-ink"
              autoComplete="username"
              required
              maxLength={80}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={submitting}
            />
            <label className="field-label" htmlFor="admin-password">
              Password
            </label>
            <input
              id="admin-password"
              className="text-input tw:w-full tw:text-ink"
              type="password"
              autoComplete="current-password"
              required
              maxLength={200}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={submitting}
            />
            {(error || connectionError) && (
              <p className="field-error" role="alert">
                {error || connectionError}
              </p>
            )}
            <Button type="submit" className="full-width" disabled={submitting}>
              {submitting ? 'Signing in…' : 'Sign in'}
              <i className="fa-solid fa-arrow-right" aria-hidden="true" />
            </Button>
          </form>
          <p className="field-help">Players: scan the QR code at the cabinet to join.</p>
        </Card>
      </main>
      <footer>Stack Moko Baby · Administrator portal</footer>
    </div>
  )
}
