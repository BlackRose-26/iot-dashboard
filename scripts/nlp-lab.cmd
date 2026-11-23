@echo off
setlocal
set "STACK_LAB_ROOT=%~dp0.."
set "STACK_LAB_PY=%STACK_LAB_ROOT%\.tools\nlp-lab-venv\Scripts\python.exe"
if not exist "%STACK_LAB_PY%" (
  echo Offline lab environment is missing. See docs/nlp-offline-experiment.md.
  exit /b 1
)
cd /d "%STACK_LAB_ROOT%"
"%STACK_LAB_PY%" "%STACK_LAB_ROOT%\backend\nlp_lab\run.py" %*
