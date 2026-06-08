# Repair known dependency issues (run after stopping the server)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "Run .\install.ps1 first."
    exit 1
}

Write-Host "Pinning PyTorch 2.8 (no torchcodec needed)..."
& $py -m pip install "torch>=2.8,<2.9" "torchaudio>=2.8,<2.9" --index-url https://download.pytorch.org/whl/cpu

Write-Host "Pinning compatible transformers..."
& $py -m pip install "transformers>=4.57.5,<5.1"

Write-Host "Done. Restart with: .\run-server.ps1"
