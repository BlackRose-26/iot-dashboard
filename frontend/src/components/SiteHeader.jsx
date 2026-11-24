import { useEffect, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'
import { useApp } from '../state/AppContext'

// Player-site header: Home, About, Contact and one call to action.
// On phones the links fold into a menu button.
const links = [
  ['/', 'Home'],
  ['/about', 'About'],
  ['/contact', 'Contact'],
]

export default function SiteHeader() {
  const { ticket } = useApp()
  const { pathname } = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)
  useEffect(() => setMenuOpen(false), [pathname])
  const home = ['/', '/scan'].includes(pathname)
  const cta = ticket
    ? { to: '/ticket', label: 'My ticket' }
    : { to: '/scan', label: 'Scan to play' }
  return (
    <>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <header className="site-header">
        <div className="site-header-bar">
          <Link to="/" className="site-brand" aria-label="Stack Moko Baby home">
            <i className="fa-solid fa-layer-group site-brand-mark" aria-hidden="true" />
            <span>
              stack moko baby<span className="site-brand-dot">.</span>
            </span>
          </Link>
          <nav aria-label="Main" className={`site-nav ${menuOpen ? 'open' : ''}`} id="site-nav">
            {links.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                end
                className={({ isActive }) => (isActive || (to === '/' && home) ? 'active' : '')}
                {...(to === '/' && pathname === '/scan' ? { 'aria-current': 'page' } : {})}
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="site-header-actions">
            <Link to={cta.to} className="site-cta">
              {cta.label}
            </Link>
            <button
              type="button"
              className="site-menu-button"
              aria-label="Menu"
              aria-expanded={menuOpen}
              aria-controls="site-nav"
              onClick={() => setMenuOpen((open) => !open)}
            >
              <i className={`fa-solid ${menuOpen ? 'fa-xmark' : 'fa-bars'}`} aria-hidden="true" />
            </button>
          </div>
        </div>
      </header>
    </>
  )
}
