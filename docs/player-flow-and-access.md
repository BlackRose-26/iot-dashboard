# QR entry, queue, results and administrator access

Implementation update: 15 November 2026. This document supersedes older preview-only descriptions and public-dashboard/public-leaderboard assumptions. The user's latest decisions require player-only QR entry, admin login and neutral admin light/dark themes. The colorful Sourcio-derived player experience remains.

## Implemented journey

| Route | Who can use it | Behavior |
|---|---|---|
| `/` or `/scan` | Anyone | Camera and QR-image upload options using the html5-qrcode API; no dashboard link |
| `/join/:token` | Anyone | Opens the same scanner; opening or pasting this URL alone creates no entry grant. A successful camera/image detection is checked by the backend before a two-hour HttpOnly grant unlocks registration or an existing active ticket |
| `/register` | Browser with an unused entry grant, or its existing active player | Required nickname, private student ID and notice acknowledgement; server saves the player and FIFO ticket |
| `/ticket` | Owner of a valid player session | Own position, called/playing status, cancellation while waiting, completed win/loss result and notification |
| `/leaderboard/acs-day` | Player whose latest ticket has a completed round | Best valid result per player, source cohort matching their device or simulator round |
| `/admin/login` | Anyone | Administrator sign-in; no public signup |
| `/admin/*` | Authenticated staff | Dashboard, analytics, queue controls, results, machine and QR display |

The server independently authorizes each protected API. Player endpoints never accept another player's ID as a ticket selector. A player code is public display data, not authentication. The scanner uses the existing html5-qrcode API, not a custom decoder. Only a detected, registered game QR for the event website is exchanged for an entry grant in the normal player flow. QR content remains a public capability: a browser/server cannot cryptographically establish that a person physically scanned it. See [scanner behavior and API contract](qr-scanner.md).

Registration checks admissions in the same transaction as ticket creation. Student IDs stay private, encrypted at rest and absent from all ticket/leaderboard/admin snapshot responses. Returning players in their authenticated browser can scan again after a finished or cancelled round; a different browser cannot recover an identity merely by knowing its student ID. The notice is versioned `2026-11-v1`. Retention deadlines are recorded but automated deletion and staffed recovery remain future operations.

Queue assignment is FIFO, serialized by database locks, additionally protected by uniqueness constraints and call-next idempotency receipts. Calls fail if the cabinet lacks a fresh ready heartbeat, the queue is empty, admissions are paused or a round is active. A called ticket remains assigned until resolved; it is not silently dropped. A waiting player can cancel only their own place. Admin skips require a reason and are audited.

Registration does not automatically call a player or start a game. The authenticated player's context includes `cabinetState` and `queueState` (`paused`, `offline`, `busy` or `awaiting_operator`); the ticket explains the waiting reason without exposing other players. Position 1 means first in line, not a cabinet reservation. The operator uses **Call next player** in the admin Queue page once the cabinet is ready, then the player starts the reserved game with the physical button.

For local development without a connected ESP32, the admin Queue page also exposes the existing simulator when enabled: **Set simulator ready → Call next player → Start test round → Finish: win / Finish: loss**. These actions remain authenticated, explicit and server-validated; no page automatically runs a round. The player's open ticket receives the saved result through polling. **Release test ticket** releases only a simulator reservation; it is not recovery for an unresolved physical-device round.

Player views poll private state every two seconds and on window focus. Waiting, called, playing and completed states persist across reloads. Both win and loss produce a durable notification in the result transaction. The ticket shows the result alert and a leaderboard button automatically. Optional browser alerts are requested only after a click, with an in-page fallback. There is no claim of closed-tab push or guaranteed background delivery. [MDN Notifications API](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API).

## Administrator design

Light mode uses white/slate surfaces; dark mode uses charcoal surfaces with readable gray text and restrained blue-gray chart series. The theme toggle is available on login and all admin screens. Only the theme preference is saved to localStorage. Admin styling is scoped to `html[data-admin-theme]`, including dialog/menu portals; navigating to a player page removes that scope. Registration, ticket, results and leaderboard retain the supplied reference's gray canvas, rounded white cards, lime and soft blue. All UI symbols remain locally hosted Font Awesome webfonts; charts are data graphics and QR rendering uses canvas.

The supplied [Sourcio reference](https://dribbble.com/shots/22063014-Smart-Home-Dashboard-Energy-Analytics-Sourcio) and attached image continue to guide layout, spacing and the player visual language. The latest request changes the administrator palette. Security decisions follow server-side session controls and cookie practices described by [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html). The Dribbble page could not be retrieved during this update; the already supplied image and existing design documentation were used.

## Storage and interfaces

The schema baseline is `backend/migrations/001_initial.sql`, copied from the proposed schema. `002_player_flow.sql` adds QR links, entry grants, login throttling, player notifications and `game_sessions.result_source`. `schema_migrations` records applied versions. `setup_local.py` is repeatable and provisions only the project database. The runtime account has SELECT/INSERT/UPDATE/DELETE access on that database only. Secrets and generated administrator credentials are excluded from Git and Graphify.

Implemented API groups:

- Admin: `POST /api/admin/login`, `GET /session`, `POST /logout`, `GET /snapshot`, `POST /admissions`, `POST /queue/call-next`, `POST /queue/{ticket}/skip`, `POST /simulator/{action}`.
- Player: `POST /api/player/entry`, `GET /context`, `POST /register`, `POST /cancel`, `GET /leaderboard`.
- Device integration boundary: `POST /api/device/heartbeat`, `POST /sessions/{session}/start`, `POST /sessions/{session}/result`; every device call requires `X-Device-Token`. This boundary is tested with synthetic requests; no physical ESP32 is claimed connected.

Player/admin writes send `X-CSRF-Token` from their own context/session response. Admin call-next additionally sends a UUID `Idempotency-Key`. All routes operate on the initial single event/cabinet; multi-event administration is not implemented. The exact JSON fields and validation models are in `backend/app/main.py`, with replay rules in `backend/app/game.py` and a matching example contract in `contracts/game-result.example.json`.

The development simulator exists only for authorized admins when enabled. It never submits browser-chosen scores: server-generated placement evidence is replayed through the same scorer. Its results are visibly marked and kept out of the device player leaderboard. Disable it before a real event. Aggregate dashboard totals currently include all saved sources and are labelled as such; source-specific production analytics remain a follow-up.

See [backend startup and operational limits](../backend/README.md) for phone networking, HTTPS, test commands and remaining device/recovery work.
