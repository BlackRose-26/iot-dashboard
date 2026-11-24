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

const focus =
  'tw:focus-visible:outline-[3px] tw:focus-visible:outline-solid tw:focus-visible:outline-night tw:focus-visible:outline-offset-[3px]'
const navLink = `tw:flex tw:items-center tw:min-h-11 tw:max-[760px]:min-h-12 tw:px-4 tw:py-2.5 tw:max-[760px]:px-[18px] tw:max-[760px]:py-0 tw:rounded-full tw:max-[760px]:rounded-2xl tw:max-[760px]:border-[1.5px] tw:max-[760px]:border-solid tw:max-[760px]:border-night/14 tw:text-[15px] tw:motion-safe:transition-colors tw:motion-safe:duration-[120ms] ${focus}`
const navIdle = 'tw:text-night tw:font-semibold tw:hover:bg-night/6'
const navActive = 'tw:bg-night tw:text-cloud tw:font-bold'
const ctaClass = `tw:flex tw:items-center tw:min-h-11 tw:bg-lime tw:text-night tw:font-extrabold tw:text-[15px] tw:max-[760px]:text-[14px] tw:max-[430px]:text-[13px] tw:px-5 tw:py-[11px] tw:max-[760px]:px-3.5 tw:max-[760px]:py-[9px] tw:max-[430px]:px-3 tw:max-[430px]:py-2 tw:rounded-full tw:border-2 tw:border-solid tw:border-night tw:hover:bg-night tw:hover:text-lime tw:motion-safe:transition-colors tw:motion-safe:duration-[120ms] ${focus}`

export default function SiteHeader() {
  const { ticket } = useApp()
  const { pathname } = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)
  useEffect(() => setMenuOpen(false), [pathname])
  const home = ['/', '/scan'].includes(pathname)
  const cta = ticket
    ? { to: '/ticket', label: 'My ticket', className: ctaClass }
    : { to: '/scan', label: 'Scan to play', className: ctaClass }
  return (
    <>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <header className="tw:sticky tw:top-0 tw:z-50 tw:bg-cloud tw:border-0 tw:border-b tw:border-solid tw:border-night/12">
        <div className="tw:flex tw:flex-wrap tw:items-center tw:justify-between tw:gap-4 tw:max-[430px]:gap-2.5 tw:py-4 tw:max-[760px]:py-3">
          <Link
            to="/"
            className={`tw:flex tw:items-center tw:gap-2.5 tw:max-[430px]:gap-2 tw:text-night tw:font-extrabold tw:text-[20px] tw:max-[760px]:text-[18px] tw:max-[430px]:text-[16px] tw:tracking-[-0.5px] ${focus}`}
            aria-label="Stack Moko Baby home"
          >
            <i
              className="fa-solid fa-layer-group tw:text-[24px] tw:max-[430px]:text-[20px]"
              aria-hidden="true"
            />
            <span>
              stack moko baby<span>.</span>
            </span>
          </Link>
          <nav
            aria-label="Main"
            id="site-nav"
            className={`tw:flex tw:gap-1.5 tw:max-[760px]:order-3 tw:max-[760px]:w-full tw:max-[760px]:flex-col tw:max-[760px]:pb-1.5 ${menuOpen ? 'tw:max-[760px]:flex tw:max-[760px]:motion-safe:animate-fade-in' : 'tw:max-[760px]:hidden'}`}
          >
            {links.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                end
                className={({ isActive }) =>
                  `${navLink} ${isActive || (to === '/' && home) ? `active ${navActive}` : navIdle}`
                }
                {...(to === '/' && pathname === '/scan' ? { 'aria-current': 'page' } : {})}
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="tw:flex tw:items-center tw:gap-2">
            <Link to={cta.to} className={cta.className}>
              {cta.label}
            </Link>
            <button
              type="button"
              className={`tw:hidden tw:max-[760px]:grid tw:place-items-center tw:w-11 tw:h-11 tw:border-[1.5px] tw:border-solid tw:border-night tw:rounded-[22px] tw:bg-transparent tw:text-night tw:cursor-pointer tw:text-[17px] ${focus}`}
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
