import { NavLink, Link, Outlet, useLocation } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react'
import { QRCodeCanvas } from 'qrcode.react'
import { QrCode, X, Check, ChevronRight, Menu as MenuIcon } from './icons'
import { Logo, IconButton, Modal, Badge } from './ui'
import { useApp } from '../state/AppContext'
import { ThemeSwitch } from '../pages/AdminLogin'
import AdminAssistant from './AdminAssistant'
import { AssistantProvider } from '../state/AssistantContext'
import UpdateStatus from './UpdateStatus'

const tabs = [
  ['overview', 'Overview'],
  ['analytics', 'Analytics'],
  ['queue', 'Queue'],
  ['sessions', 'Sessions'],
  ['machines', 'Machine'],
  ['settings', 'Settings'],
]
export function RegistrationQR() {
  const { qrPath } = useApp()
  const canvas = useRef(null)
  const [base, setBase] = useState(import.meta.env.VITE_PUBLIC_BASE_URL || window.location.origin)
  const url = (() => {
    try {
      const u = new URL(base)
      return ['http:', 'https:'].includes(u.protocol) && qrPath
        ? new URL(qrPath, u.origin).href
        : null
    } catch {
      return null
    }
  })()
  function download() {
    const image = canvas.current?.querySelector('canvas')
    if (!image) return
    const link = document.createElement('a')
    link.href = image.toDataURL('image/png')
    link.download = 'stack-moko-baby-registration-qr.png'
    link.click()
  }
  return (
    <Modal
      title="Scan. Register. Stack."
      description="Player entry · ACS Carnival · Cabinet 01"
      trigger={
        <button className="button light qr-trigger">
          <QrCode size={17} />
          <span>Registration QR</span>
        </button>
      }
    >
      <div className="qr-wrap" ref={canvas}>
        {url ? (
          <QRCodeCanvas
            value={url}
            size={480}
            level="M"
            marginSize={4}
            title="Scan to join the player queue"
          />
        ) : (
          <p>The event QR is unavailable.</p>
        )}
      </div>
      <label className="field-label" htmlFor="event-url">
        Event website address
      </label>
      <input
        className="text-input"
        id="event-url"
        type="url"
        value={base}
        onChange={(e) => setBase(e.target.value)}
      />
      <p className="field-help">
        Use the address players can reach on carnival Wi-Fi. A localhost QR works only on this
        computer. Use HTTPS for real registrations. Players choose Use camera or Upload QR image on
        the scan page. Configure this address as STACK_PUBLIC_URL or STACK_ALLOWED_ORIGINS in the
        backend before sharing a new hostname.
      </p>
      {url && (
        <div className="modal-actions">
          <button className="button light" onClick={download}>
            Download QR
          </button>
          <a className="button dark" href={url} target="_blank" rel="noreferrer">
            Test player entry
            <i className="fa-solid fa-arrow-up-right-from-square" aria-hidden="true" />
          </a>
        </div>
      )}
    </Modal>
  )
}
export default function Shell() {
  const { pathname } = useLocation()
  const [mobileNav, setMobileNav] = useState(false)
  const { toast, setToast, logout, admin, machine } = useApp()
  useEffect(() => {
    setMobileNav(false)
    window.scrollTo(0, 0)
  }, [pathname])
  useEffect(() => {
    if (!toast) return
    const t = setTimeout(() => setToast(''), 7000)
    return () => clearTimeout(t)
  }, [toast, setToast])
  return (
    <AssistantProvider>
      <div className="app-shell">
        <a className="skip-link" href="#main-content">
          Skip to content
        </a>
        <header className="app-header">
          <Logo />
          <nav
            className={mobileNav ? 'primary-nav open' : 'primary-nav'}
            aria-label="Main navigation"
          >
            {tabs.map(([path, label]) => (
              <NavLink to={`/admin/${path}`} key={path}>
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="header-actions">
            <ThemeSwitch />
            <span className="operator-avatar" aria-label={`Signed in as ${admin.username}`}>
              AD
            </span>
            <IconButton label="Sign out" onClick={() => logout().catch((e) => setToast(e.message))}>
              <i className="fa-solid fa-right-from-bracket" aria-hidden="true" />
            </IconButton>
            <IconButton
              label={mobileNav ? 'Close navigation' : 'Open navigation'}
              className="mobile-menu"
              onClick={() => setMobileNav(!mobileNav)}
            >
              {mobileNav ? <X size={21} /> : <MenuIcon size={21} />}
            </IconButton>
          </div>
        </header>
        <div className="scope-bar">
          <span>
            <span className="scope-dot" />
            ACS Carnival
            <ChevronRight size={13} />
            <span>Classic v1</span>
          </span>
          <Badge tone="soft">
            {machine.health?.source === 'simulator'
              ? 'Simulator active · no ESP32'
              : 'Database connected · hardware status below'}
          </Badge>
        </div>
        <main id="main-content" className="main-content">
          <Outlet />
        </main>
        <footer className="app-footer">
          <Logo compact />
          <span>Stack Moko Baby · Event operations</span>
          <UpdateStatus />
        </footer>
        <AdminAssistant />
        {toast && (
          <div className="toast" role="status">
            <Check size={19} />
            <span>{toast}</span>
            <button aria-label="Dismiss notification" onClick={() => setToast('')}>
              <X size={17} />
            </button>
          </div>
        )}
      </div>
    </AssistantProvider>
  )
}
