@echo off
setlocal
set "GRAPHIFY_PROJECT_ROOT=%~dp0.."
pushd "%GRAPHIFY_PROJECT_ROOT%"
if not exist ".tools\graphify-venv\Scripts\graphify.exe" (
  echo Graphify environment is missing. See docs\graphify-setup.md.
  popd
  exit /b 1
)
".tools\graphify-venv\Scripts\graphify.exe" %*
set "GRAPHIFY_EXIT=%ERRORLEVEL%"
popd
exit /b %GRAPHIFY_EXIT%
