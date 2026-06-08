# One-time install script — no Activate.ps1 needed
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Upgrading pip..."
& $py -m pip install --upgrade pip

Write-Host "Installing PyTorch 2.8 (CPU) — avoids torchcodec on Windows..."
& $py -m pip install "torch>=2.8,<2.9" "torchaudio>=2.8,<2.9" --index-url https://download.pytorch.org/whl/cpu

Write-Host "Installing backend dependencies..."
& $py -m pip install -r requirements.txt

Write-Host "Pinning compatible transformers version..."
& $py -m pip install "transformers>=4.57.5,<5.1"

if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
}

Write-Host ""
Write-Host "Done. Start the server with:  .\run-server.ps1"
