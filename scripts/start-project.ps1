$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$pythonPath = Join-Path $projectRoot 'backend\.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $pythonPath)) { $pythonPath = Join-Path $projectRoot '.tools\backend-venv\Scripts\python.exe' }
$runtimeRoot = 'C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1112-737-0_26.1112.737.0_x64__3k8sg7r9htsxt\dependencies'
$nodePath = Join-Path $runtimeRoot 'node\bin\node.exe'
if (Get-Command node -ErrorAction SilentlyContinue) { $nodePath = (Get-Command node).Source }
if (!(Test-Path -LiteralPath $pythonPath)) { throw 'Backend environment missing. Follow backend/README.md.' }
if (!(Test-Path -LiteralPath (Join-Path $projectRoot 'backend\.env'))) { throw 'Run backend/setup_local.py first. See backend/README.md.' }
$runDirectory = Join-Path $projectRoot '.tools\run'
New-Item -ItemType Directory -Path $runDirectory -Force | Out-Null
try { $null = Invoke-RestMethod 'http://127.0.0.1:8000/api/health' -TimeoutSec 2 } catch {
    Start-Process -FilePath $pythonPath -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000','--no-access-log' -WorkingDirectory (Join-Path $projectRoot 'backend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runDirectory 'api.out.log') -RedirectStandardError (Join-Path $runDirectory 'api.err.log')
}
try { $null = Invoke-WebRequest 'http://127.0.0.1:5173' -UseBasicParsing -TimeoutSec 2 } catch {
    Start-Process -FilePath $nodePath -ArgumentList 'node_modules/vite/bin/vite.js','--host','0.0.0.0','--port','5173','--strictPort' -WorkingDirectory (Join-Path $projectRoot 'frontend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runDirectory 'frontend.out.log') -RedirectStandardError (Join-Path $runDirectory 'frontend.err.log')
}
Write-Host 'Open http://127.0.0.1:5173/admin/login. Keep XAMPP MySQL running.'
Write-Host 'Administrator credentials: backend/.admin-credentials.txt. Phone QR links require a reachable event address.'
