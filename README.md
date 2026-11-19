# Stack Moko Baby

![Status: local development](https://img.shields.io/badge/status-local_development-64748b)
![React 19](https://img.shields.io/badge/React-19-149eca?logo=react&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-JSX-f7df1e?logo=javascript&logoColor=black)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi&logoColor=white)
![XAMPP MariaDB](https://img.shields.io/badge/database-XAMPP_MariaDB-fb7a24?logo=xampp&logoColor=white)
![ESP32 integration planned](https://img.shields.io/badge/ESP32-integration_planned-64748b)

An IoT carnival LED-matrix stacking game with a private player queue and an administrator dashboard. Players scan the event QR, register, wait for their turn, play at the physical cabinet and receive a win/loss result with leaderboard access. The ESP32 and physical button own gameplay timing; the backend owns queue assignment and validated scores.

## Current implementation

- **Player flow:** camera or image QR scanning through html5-qrcode, required private student ID, registration, persistent personal ticket, FIFO position, turn/result updates and post-game leaderboard.
- **Administration:** session-based login, neutral light/dark dashboard, cards and charts, queue/admissions controls, saved sessions/results, cabinet status and registration QR download.
- **Backend:** FastAPI, transactional MariaDB persistence, migrations, CSRF protection, encrypted student IDs and server-side score replay.
- **Live updates:** authenticated staff/player notifications, durable post-commit outbox, revisioned snapshots, reconnect recovery and polling fallback; no public stream. See [behavior and limits](docs/live-updates.md).
- **Device command boundary:** authenticated polling and durable receipts, receipt-required start, a command emulator and review-hold diagnostics. Physical firmware and guarded reconciliation remain pending.
- **Development simulator:** explicit admin controls for readiness, start and win/loss results; simulator scores are labelled and separated from device rankings.
- **Stack Intelligence:** local Ollama system conversation, private per-admin topic/preferences memory, read-only analytics and factual English/Taglish answers with scope/evidence. Memory improves continuity; selected sanitized routing examples can be reviewed and exported for later fine-tuning. Model weights are not automatically retrained. Local loading, English/Taglish routing and synthetic browser flows have been checked; broader release acceptance remains pending. See [AI setup and review checklist](docs/admin-assistant.md).

Physical ESP32 firmware and end-to-end hardware integration remain pending. Closed-tab push, automated retention/recovery and production deployment hardening are also pending. This repository is a local development implementation; proposed numeric game settings still need play-testing.

The [19 November quality audit](docs/quality-audit.md) records security/correctness fixes, current automated/browser checks, local restart/load/restore evidence and the remaining release limits. New roadmap features are paused.

## Technology

| Layer | Stack |
|---|---|
| Frontend | React 19, JavaScript/JSX, Vite, React Router |
| UI / visualization | Shared CSS tokens, Radix primitives, Recharts, Font Awesome webfonts |
| Backend | Python 3.13, FastAPI, SQLAlchemy Core |
| Database | XAMPP MySQL service — local installation uses MariaDB 10.11.16 |
| Planned cabinet | ESP32, LED matrix, physical button |
| Project map | Graphify |

## Install once

Windows prerequisites: [Node.js](https://nodejs.org/en/download) **22.12 or newer** (the local environment uses Node 24), [Python 3.13](https://www.python.org/downloads/windows/) and [XAMPP](https://www.apachefriends.org/). Open a new terminal after installation. Start **MySQL** in the XAMPP Control Panel.

From your checkout (shown here as `D:\iot-dashboard`):

```powershell
cd D:\iot-dashboard
npm --prefix frontend ci
python -m venv backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\backend\.venv\Scripts\python.exe backend\setup_local.py
```

The setup script provisions the project database, applies migrations and creates local configuration and administrator credentials. It preserves existing data and passwords on reruns. For an existing password-protected XAMPP root account, follow [backend setup](backend/README.md); do not change your database root password to match this project.

Local administrator credentials are written to `backend/.admin-credentials.txt`. Keep that file and `backend/.env` private. Neither belongs in Git, screenshots or chat.

## Run after each restart

1. Start **MySQL** in XAMPP.
2. Run:

```powershell
cd D:\iot-dashboard
npm run dev
```

The same `npm run dev` command also works from `frontend`. It starts FastAPI, waits for API/database readiness, then starts Vite. Keep this terminal open. **Ctrl+C** stops the servers started by this launcher; XAMPP and any reused backend remain running.

Open [administrator login](http://localhost:5173/admin/login). Players enter through the administrator's registration QR and have no dashboard access. Keep using one hostname consistently in your browser because `localhost` and `127.0.0.1` have separate session cookies.

For separate terminals, run `npm run dev:backend` and `npm run dev:frontend` from the project root. The frontend-only command requires a running API on port 8000. Existing `.cmd` launchers are available under `scripts`.

No ESP32 connected yet? In **Admin → Queue**, use **Set simulator ready → Call next player → Start test round → Finish: win / loss**. These are development simulations, not physical rounds.

## Troubleshooting

| Message | What to do |
|---|---|
| `ECONNREFUSED 127.0.0.1:8000` | The API is not listening. Stop an old frontend-only terminal and use the combined `npm run dev`. Keep its terminal open. |
| API/database not ready | Start MySQL in XAMPP. If it is already running, inspect the backend error and [local setup](docs/local-setup.md). Do not reset or delete the database. |
| Port 5173 already in use | Stop the old Vite terminal with Ctrl+C before starting another copy. |
| Port 8000 occupied by an old/unready API | Stop its original terminal and retry. The launcher reuses a healthy current API and never kills an unrelated server. |
| `/api/admin/session` returns `401` | Sign in. This is the expected response without a valid admin session; it is not a database connection error. |
| Player remains waiting | The operator must call the next player when the cabinet is ready. Registration alone does not start a game. |

Phones need a reachable event address and trusted HTTPS for camera access and real identity collection. A QR containing `localhost` only works on the computer hosting the app. See [QR scanner setup](docs/qr-scanner.md).

## Repository layout

```text
backend/       FastAPI application, migrations and local setup
frontend/      React application
contracts/     Game-result contract examples
docs/          Internal project guide, specifications and setup
scripts/       Development launcher and Graphify tools
graphify-out/  Generated project knowledge graph
```

## Documentation and contributing

**Always read [docs/README.md](docs/README.md) before project work.** It remains the internal guide and specification index. This root README is the public introduction and installation guide.

- [Daily setup and connection troubleshooting](docs/local-setup.md)
- [Player flow and access](docs/player-flow-and-access.md)
- [Architecture](docs/tech-stack.md) and [database schema](docs/schema.md)
- [Dashboard design](docs/dashboard-design.md) and [Stack Intelligence](docs/admin-assistant.md)
- [AI system rules](docs/ai-system-rules.md) and [implementation plan](docs/implementation-plan.md)

Follow `AGENTS.md`, keep private identities/configuration out of commits and refresh Graphify after changes. Test commands and their isolated data requirements are documented in the frontend/backend READMEs. No CI, deployment or hardware verification is implied by the badges above.
