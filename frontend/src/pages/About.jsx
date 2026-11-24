import { PublicHeader } from './Leaderboard'
import { GameBand, steps } from '../components/SiteSections'
import * as ui from '../components/siteStyles'

const facts = [
  [
    'The game runs in the cabinet',
    'An ESP32 inside the cabinet runs every round, so your button timing never waits for the internet.',
  ],
  [
    'A fair, first-come line',
    'Scan, pick a nickname and you’re in. Players are called strictly in the order they joined.',
  ],
  [
    'Every score is checked',
    'The cabinet sends each placement, and the server replays the round before your score is saved.',
  ],
]

const faq = [
  [
    'Do I need an app or an account?',
    'No. Scan the QR with your phone camera and pick a nickname.',
  ],
  [
    'Can I play more than once?',
    'Yes. After your round, scan the QR again to rejoin the end of the line.',
  ],
  [
    'What if I miss my turn?',
    'When you’re called you have about 3 minutes to reach the cabinet and press the button. If you can’t make it, tell an operator.',
  ],
  [
    'I lost my ticket. What now?',
    'Ask an operator at the booth. They can show you a one-time re-entry QR that brings your ticket back.',
  ],
]

export default function About() {
  return (
    <div className="public-shell">
      <PublicHeader />
      <main id="main-content">
        <section className="tw:flex tw:flex-col tw:gap-[18px] tw:pt-14 tw:pb-7">
          <span className={`${ui.pill} ${ui.enter}`}>ABOUT THE GAME</span>
          <h1 className={`${ui.h1} ${ui.enter} ${ui.delays[1]}`}>
            A carnival stacker, with a fair line and a friendly robot.
          </h1>
          <p className={`${ui.lead} ${ui.enter} ${ui.delays[2]}`}>
            Stack Moko Baby is an LED stacking game built for the ACS Carnival. Time your button
            presses to stack each row on the last. Your phone keeps your place in line, and Stack
            Intelligence answers your questions while you wait.
          </p>
        </section>
        <section className={ui.section} aria-labelledby="works">
          <h2 id="works" className={ui.h2}>
            How the cabinet works
          </h2>
          <div className={ui.grid}>
            {facts.map(([title, text], index) => (
              <article key={title} className={`${ui.box} ${ui.enter} ${ui.delays[index]}`}>
                <span className={ui.num}>{index + 1}</span>
                <h3 className={ui.boxTitle}>{title}</h3>
                <p className={ui.boxText}>{text}</p>
              </article>
            ))}
          </div>
        </section>
        <section className={ui.section} aria-label="Game rules">
          <GameBand />
        </section>
        <section className={ui.section} aria-labelledby="privacy">
          <div className={`${ui.band} tw:items-start`}>
            <div>
              <span className={`${ui.tag} tw:text-[15px]`}>PRIVACY</span>
              <h2 id="privacy" className={ui.bandTitle}>
                Your student ID stays private.
              </h2>
            </div>
            <ul className="tw:m-0 tw:p-0 tw:list-none tw:flex tw:flex-col tw:gap-3 tw:text-[16px] tw:leading-normal tw:text-cloud/86">
              <li>It’s encrypted and only used so each student holds one place in line.</li>
              <li>It never appears on your ticket, the leaderboard or in the chat.</li>
              <li>It’s deleted after the event. Nicknames and scores stay.</li>
              <li>
                Stack Intelligence only reads the rules, the line and scores. It can’t change your
                place.
              </li>
            </ul>
          </div>
        </section>
        <section className={ui.section} aria-labelledby="steps">
          <h2 id="steps" className={ui.h2}>
            Three steps to play
          </h2>
          <ol className={ui.grid}>
            {steps.map(([title, text], index) => (
              <li key={title} className={ui.box}>
                <span className={ui.num}>{index + 1}</span>
                <h3 className={ui.boxTitle}>{title}</h3>
                <p className={ui.boxText}>{text}</p>
              </li>
            ))}
          </ol>
        </section>
        <section className={ui.section} aria-labelledby="faq">
          <h2 id="faq" className={ui.h2}>
            Questions
          </h2>
          <div className={ui.faqList}>
            {faq.map(([question, answer]) => (
              <details key={question} className={ui.faqItem}>
                <summary className={ui.faqQuestion}>{question}</summary>
                <p className={ui.faqAnswer}>{answer}</p>
              </details>
            ))}
          </div>
        </section>
      </main>
      <footer className="public-footer">Stack Moko Baby · ACS Carnival</footer>
    </div>
  )
}
