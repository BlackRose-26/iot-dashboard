param([Parameter(Mandatory=$true)][string]$PublicUrl)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
$previous=@{}
foreach ($name in @('STACK_PUBLIC_URL','STACK_COOKIE_SECURE','STACK_ENV','STACK_SIMULATOR_ENABLED','STACK_FRONTEND_DIST')) {
  $previous[$name]=[Environment]::GetEnvironmentVariable($name,'Process')
}
$publicOrigin=[uri]$PublicUrl
if ($publicOrigin.Scheme -ne 'https' -or $publicOrigin.AbsolutePath -ne '/' -or $publicOrigin.Query -or $publicOrigin.Fragment -or $publicOrigin.UserInfo) {
  throw 'Use the HTTPS origin only, for example https://your-event.example.com'
}
Push-Location $projectRoot
try {
  npm.cmd --prefix frontend run build
  if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
  $env:STACK_PUBLIC_URL=$PublicUrl.TrimEnd('/')
  $env:STACK_COOKIE_SECURE='true'
  $env:STACK_ENV='production'
  $env:STACK_SIMULATOR_ENABLED='false'
  $env:STACK_FRONTEND_DIST=Join-Path $projectRoot 'frontend\dist'
  & backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --workers 1 --no-access-log
} finally {
  foreach ($name in $previous.Keys) { [Environment]::SetEnvironmentVariable($name,$previous[$name],'Process') }
  Pop-Location
}
