# Local React and backend setup

**New laptop or fresh clone?** Use [SETUP.md](../SETUP.md) and `npm run setup`; it installs and configures everything below. This page keeps the details and the history of the original machine.

Node.js **24.22.3**, npm **11.19.1** and Python **3.13.17** are installed for the local Windows user. The backend has a regular virtual environment at `D:\iot-dashboard\backend\.venv` with the pinned requirements installed. The frontend uses its package.json scripts and an npm lockfile. React and Vite dependencies are project dependencies, not global commands.

After this first setup, close and reopen the terminal application (including VS Code/Codex if using its integrated terminals) so it receives the updated user PATH. Check with `node --version`, `npm --version` and `python --version`.

## Start development

Start **MySQL** in XAMPP after each computer restart. Then use one PowerShell terminal:

```powershell
cd D:\iot-dashboard
npm run dev
```

`npm run dev` also works from `D:\iot-dashboard\frontend`. The combined Node launcher starts FastAPI on port 8000, waits for a successful API/database readiness response, then starts Vite on port 5173. It checks for missing dependencies/configuration and occupied ports, and reuses a healthy current backend. It does not provision/reset the database, start XAMPP or modify credentials. Keep the terminal open; Ctrl+C stops only the server processes this invocation started, including the Uvicorn reloader. A reused backend remains owned by its original terminal.

Open [admin login](http://localhost:5173/admin/login). The standalone `.cmd` entry points use the same launcher or your installed Node; they no longer depend on a versioned Codex runtime path or leave newly launched servers hidden in the background.

### Separate terminals (optional)

Backend, from the project root:

```powershell
cd D:\iot-dashboard
npm run dev:backend
```

Frontend only, in another terminal:

```powershell
cd D:\iot-dashboard
npm run dev:frontend
```

The frontend folder also supports `npm run dev:frontend`. For a direct Python command without Node orchestration:

```powershell
cd D:\iot-dashboard\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --no-access-log
```

PowerShell activation is unnecessary because the command uses the project's Python executable directly. Do not start a second combined launcher while Vite already occupies port 5173.

## Connection problems after a reboot

`ECONNREFUSED 127.0.0.1:8000` means no API was accepting connections at that address when Vite tried to proxy the request. Previously `frontend/npm run dev` started Vite alone; shutting down Windows stopped the separately launched backend. Start XAMPP MySQL and use the combined command above. A 30-second backend readiness timeout now prevents Vite from starting against an unavailable API/database.

`GET /api/admin/session` returning 401 is expected before sign-in or after session expiry. The later 200 responses in the supplied logs show successful requests at those times; they do not prove the backend remained running afterward. Use the same browser hostname for login and dashboard. If port 8000 is occupied by a backend started before the new health identity field was added, stop that backend once with Ctrl+C and restart it. Do not regenerate secrets or delete the database to repair a missing process.

## Reinstall dependencies when needed

Frontend, from its folder: `npm ci`. Backend, from its folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On a new computer, install [Node.js LTS](https://nodejs.org/en/download) and [Python](https://www.python.org/downloads/windows/) first, then follow [backend database setup](../backend/README.md). Keep backend `.env`, the virtual environment, database contents and credentials private and outside source control/Graphify.

The current Node installation is independent of Codex's bundled runtime and is on the user's PATH. PowerShell uses npm's Windows `.cmd` entry point through the local `Programs\NodeCommands` directory; its script execution policy was not changed. The root package requires no additional npm dependencies; frontend dependencies remain pinned in `frontend/package-lock.json`.

The startup changes were reviewed from source only. No tests, builds, live API/database requests or browser checks were run, following the user's instruction to test the application themselves.


## Audited readiness and origin configuration — 19 November 2026

The health endpoint now checks required tables, applied migration filenames and initial event/cabinet/rules configuration. An incomplete setup returns 503 rather than claiming readiness. Apply pending migrations with the existing setup command; do not reset data or regenerate keys. Database connect/read/write waits are bounded at five seconds. Browser API requests are cancellable and bounded at 15 seconds (25 for assistant queries); after a timed-out action, check its latest state before retrying.

For a LAN or HTTPS hostname, configure `STACK_PUBLIC_URL` or comma-separated `STACK_ALLOWED_ORIGINS` in the private backend environment and restart. The incoming Host header alone does not authorize writes or WebSockets. Development loopback aliases remain supported. Vite preview now honours `STACK_API_TARGET`, like the development server. Combined local startup still uses API 8000 and Vite 5173.

The [quality audit](quality-audit.md) supersedes earlier source-only verification notes. Dedicated browser checks wait for API readiness before launching Vite. The running user servers were preserved; tests used only disposable databases and ports 8001/5174.
