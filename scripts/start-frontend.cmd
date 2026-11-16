@echo off
setlocal
cd /d "%~dp0..\frontend"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is not on PATH. Install Node.js and reopen your terminal. See docs\local-setup.md.
  exit /b 1
)
if not exist "node_modules\vite\bin\vite.js" (
  echo Frontend dependencies missing. Run npm ci in frontend.
  exit /b 1
)
echo Starting frontend only. Keep the backend and XAMPP MySQL running.
node node_modules\vite\bin\vite.js --host 0.0.0.0 --port 5173 --strictPort
