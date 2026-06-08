# VoiceAI backend launcher (Windows) — delegates to install + run-server
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
& "$PSScriptRoot\install.ps1"
& "$PSScriptRoot\run-server.ps1"
