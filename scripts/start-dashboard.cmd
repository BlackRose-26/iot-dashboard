@echo off
setlocal
cd /d "%~dp0.."
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is not on PATH. Install Node.js and reopen your terminal. See docs\local-setup.md.
  exit /b 1
)
node scripts\dev.mjs
