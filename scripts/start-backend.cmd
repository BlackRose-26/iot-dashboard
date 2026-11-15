@echo off
setlocal
cd /d "%~dp0..\backend"
set "STACK_PYTHON=%~dp0..\backend\.venv\Scripts\python.exe"
if not exist "%STACK_PYTHON%" set "STACK_PYTHON=%~dp0..\.tools\backend-venv\Scripts\python.exe"
if not exist "%STACK_PYTHON%" (
  echo Backend environment missing. Follow backend\README.md.
  exit /b 1
)
if not exist ".env" (
  echo Backend configuration missing. Run backend\setup_local.py first.
  exit /b 1
)
echo Starting backend at http://127.0.0.1:8000
echo Keep XAMPP MySQL running. Press Ctrl+C to stop this server.
"%STACK_PYTHON%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
