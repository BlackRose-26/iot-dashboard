@echo off
setlocal
cd /d "%~dp0.."
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is not on PATH. See docs\local-setup.md for the direct Python command.
  exit /b 1
)
node scripts\dev.mjs --backend-only
