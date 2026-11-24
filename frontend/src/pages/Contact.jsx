import { PublicHeader } from './Leaderboard'
import RobotIcon from '../components/RobotIcon'
import { openRobotChat } from '../components/SiteSections'

// Optional event details, set at build time; nothing here is secret.
const location = import.meta.env.VITE_EVENT_LOCATION || 'Next to Cabinet 01'
const hours = import.meta.env.VITE_EVENT_HOURS || ''
const email = import.meta.env.VITE_ORGANISER_EMAIL || ''

export default function Contact() {
  return (
    <div className="public-shell">
      <PublicHeader />
      <main id="main-content" className="contact-layout">
        <section className="contact-intro">
          <span className="site-pill">CONTACT</span>
          <h1 className="site-h1">Need a hand? We’re right by the cabinet.</h1>
          <p className="site-lead">
            For anything during the event, the fastest help is an operator at the booth. Quick
            questions? The robot in the corner answers right away.
          </p>
          <button type="button" className="site-button dark" onClick={openRobotChat}>
            <span className="robot-chip">
              <RobotIcon size={26} tone="ink" />
            </span>
            Ask the robot
          </button>
        </section>
        <section className="contact-cards" aria-label="Ways to get help">
          <article className="site-box">
            <h2>Find us</h2>
            <p>
              Cabinet 01 · {location}
              {hours && (
                <>
                  <br />
                  {hours}
                </>
              )}
            </p>
          </article>
          <article className="site-box">
            <h2>Lost your ticket?</h2>
            <p>An operator can show you a one-time re-entry QR. Your place in line is kept.</p>
          </article>
          <article className="site-box">
            <h2>Missed your turn?</h2>
            <p>Tell an operator. You can scan the QR again to rejoin the end of the line.</p>
          </article>
          <article className="site-box">
            <h2>Organisers</h2>
            <p>
              ACS Carnival team
              <br />
              {email ? (
                <a href={`mailto:${email}`}>{email}</a>
              ) : (
                'Ask at the booth for the organisers.'
              )}
            </p>
          </article>
          <article className="site-box contact-privacy">
            <h2>Privacy</h2>
            <p>Never send your student ID by message or chat. We will never ask for it here.</p>
          </article>
        </section>
      </main>
      <footer className="public-footer">Stack Moko Baby · ACS Carnival</footer>
    </div>
  )
}
