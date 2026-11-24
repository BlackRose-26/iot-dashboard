import { PublicHeader } from './Leaderboard'
import RobotIcon from '../components/RobotIcon'
import { openRobotChat } from '../components/SiteSections'
import * as ui from '../components/siteStyles'

// Optional event details, set at build time; nothing here is secret.
const location = import.meta.env.VITE_EVENT_LOCATION || 'Next to Cabinet 01'
const hours = import.meta.env.VITE_EVENT_HOURS || ''
const email = import.meta.env.VITE_ORGANISER_EMAIL || ''

const card = `${ui.box} ${ui.enter}`
const cardTitle = 'tw:m-0 tw:text-[17px] tw:font-extrabold'

export default function Contact() {
  return (
    <div className="public-shell">
      <PublicHeader />
      <main
        id="main-content"
        className="tw:grid tw:grid-cols-[repeat(auto-fit,minmax(min(100%,420px),1fr))] tw:gap-10 tw:items-start tw:pt-14 tw:pb-6"
      >
        <section className="tw:flex tw:flex-col tw:gap-[18px] tw:items-start">
          <span className={`${ui.pill} ${ui.enter}`}>CONTACT</span>
          <h1 className={`${ui.h1} ${ui.enter} ${ui.delays[1]}`}>
            Need a hand? We’re right by the cabinet.
          </h1>
          <p className={`${ui.lead} ${ui.enter} ${ui.delays[2]}`}>
            For anything during the event, the fastest help is an operator at the booth. Quick
            questions? The robot in the corner answers right away.
          </p>
          <button
            type="button"
            className={`${ui.buttonDark} ${ui.enter} ${ui.delays[3]}`}
            onClick={openRobotChat}
          >
            <span className={ui.robotChip}>
              <RobotIcon size={26} tone="ink" />
            </span>
            Ask the robot
          </button>
        </section>
        <section
          className="tw:grid tw:grid-cols-[repeat(auto-fit,minmax(min(100%,220px),1fr))] tw:gap-3"
          aria-label="Ways to get help"
        >
          <article className={`${card} ${ui.delays[1]}`}>
            <h2 className={cardTitle}>Find us</h2>
            <p className={ui.boxText}>
              Cabinet 01 · {location}
              {hours && (
                <>
                  <br />
                  {hours}
                </>
              )}
            </p>
          </article>
          <article className={`${card} ${ui.delays[2]}`}>
            <h2 className={cardTitle}>Lost your ticket?</h2>
            <p className={ui.boxText}>
              An operator can show you a one-time re-entry QR. Your place in line is kept.
            </p>
          </article>
          <article className={`${card} ${ui.delays[3]}`}>
            <h2 className={cardTitle}>Missed your turn?</h2>
            <p className={ui.boxText}>
              Tell an operator. You can scan the QR again to rejoin the end of the line.
            </p>
          </article>
          <article className={`${card} ${ui.delays[4]}`}>
            <h2 className={cardTitle}>Organisers</h2>
            <p className={ui.boxText}>
              ACS Carnival team
              <br />
              {email ? (
                <a className="tw:text-night tw:font-bold" href={`mailto:${email}`}>
                  {email}
                </a>
              ) : (
                'Ask at the booth for the organisers.'
              )}
            </p>
          </article>
          <article className={`${card} ${ui.delays[4]} tw:bg-night tw:border-night`}>
            <h2 className={`${cardTitle} tw:text-lime`}>Privacy</h2>
            <p className="tw:m-0 tw:text-[15px] tw:leading-[1.55] tw:text-cloud/86">
              Never send your student ID by message or chat. We will never ask for it here.
            </p>
          </article>
        </section>
      </main>
      <footer className="public-footer">Stack Moko Baby · ACS Carnival</footer>
    </div>
  )
}
