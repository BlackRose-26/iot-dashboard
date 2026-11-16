$ErrorActionPreference = 'Stop'
$nodeCommand = Get-Command node -ErrorAction SilentlyContinue
if (!$nodeCommand) { throw 'Install Node.js and reopen your terminal. See docs/local-setup.md.' }
& $nodeCommand.Source (Join-Path $PSScriptRoot 'dev.mjs')
exit $LASTEXITCODE
