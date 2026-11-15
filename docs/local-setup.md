# Local React and backend setup

Node.js **24.22.3**, npm **11.19.1** and Python **3.13.17** are installed for the local Windows user. The backend has a regular virtual environment at `D:\iot-dashboard\backend\.venv` with the pinned requirements installed. The frontend uses its package.json scripts and an npm lockfile. React and Vite dependencies are project dependencies, not global commands.

After this first setup, close and reopen the terminal application (including VS Code/Codex if using its integrated terminals) so it receives the updated user PATH. Check with `node --version`, `npm --version` and `python --version`.

## Start development

Start **MySQL** in XAMPP. Open two PowerShell terminals.

Frontend:

```powershell
cd D:\iot-dashboard\frontend
npm run dev
```

Backend:

```powershell
cd D:\iot-dashboard\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --no-access-log
```

Open [admin login](http://localhost:5173/admin/login). Press **Ctrl+C** in each terminal to stop its server. The backend command directly uses the project's Python environment, so PowerShell activation is unnecessary. Neither command starts the XAMPP database or changes database credentials.

## Reinstall dependencies when needed

Frontend, from its folder: `npm ci`. Backend, from its folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On a new computer, install [Node.js LTS](https://nodejs.org/en/download) and [Python](https://www.python.org/downloads/windows/) first, then follow [backend database setup](../backend/README.md). Keep backend `.env`, the virtual environment, database contents and credentials private and outside source control/Graphify.

The current Node installation is independent of Codex's bundled runtime and is on the user's PATH. PowerShell uses npm's Windows `.cmd` entry point through the local `Programs\NodeCommands` directory; its script execution policy was not changed. The old project launchers remain optional, but normal npm and Python commands above are the primary workflow.
