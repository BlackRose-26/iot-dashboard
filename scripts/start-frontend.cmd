@echo off
setlocal
cd /d "%~dp0..\frontend"
set "STACK_NODE=C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1112-737-0_26.1112.737.0_x64__3k8sg7r9htsxt\dependencies\node\bin\node.exe"
where node >nul 2>nul
if not errorlevel 1 set "STACK_NODE=node"
if not exist "node_modules\vite\bin\vite.js" (
  echo Frontend dependencies missing. Follow frontend\README.md.
  exit /b 1
)
echo Starting frontend at http://127.0.0.1:5173/admin/login
echo Press Ctrl+C to stop this server.
"%STACK_NODE%" "node_modules\vite\bin\vite.js" --host 0.0.0.0 --port 5173 --strictPort
