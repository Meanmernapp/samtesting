# Start backend — no Activate.ps1 needed
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "Run .\install.ps1 first."
    exit 1
}

$env:COQUI_TOS_AGREED = "1"
& $py run.py
