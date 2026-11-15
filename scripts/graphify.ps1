param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GraphifyArguments)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$graphifyExe = Join-Path $projectRoot '.tools\graphify-venv\Scripts\graphify.exe'
if (-not (Test-Path -LiteralPath $graphifyExe)) {
    throw 'Graphify environment is missing. Recreate it using docs/graphify-setup.md.'
}
Push-Location -LiteralPath $projectRoot
try {
    & $graphifyExe @GraphifyArguments
    $graphifyExit = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $graphifyExit
