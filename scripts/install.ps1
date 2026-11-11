# agent-revert installer — Windows (PowerShell 5.1+)
# Usage (PowerShell):
#   irm https://raw.githubusercontent.com/kaia-cod/agent-revert/main/scripts/install.ps1 | iex
#   # or local:
#   powershell -ExecutionPolicy Bypass -File scripts\install.ps1 [-VenvDir <dir>] [-Help]
# Parameters:
#   -VenvDir <dir>  Install into a Python venv at <dir> (default: %LOCALAPPDATA%\agent-revert\venv)
#   -Help, -h       Show this help and exit 0
# Exit codes: 0 = success, 1 = python-not-found/install failure.
param(
  [string]$VenvDir = "$env:LOCALAPPDATA\agent-revert\venv",
  [switch]$Help
)
$ErrorActionPreference = "Stop"

function Show-Usage {
  Write-Host "agent-revert installer — Windows (PowerShell 5.1+)"
  Write-Host "  irm https://raw.githubusercontent.com/kaia-cod/agent-revert/main/scripts/install.ps1 | iex"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\install.ps1 [-VenvDir <dir>] [-Help]"
  Write-Host "  -VenvDir <dir>  Install into a Python venv at <dir> (default: %LOCALAPPDATA%\agent-revert\venv)"
  Write-Host "  -Help, -h       Show this help and exit 0"
}
if ($Help) { Show-Usage; exit 0 }

Write-Host "== agent-revert installer (Windows) =="

# --- 1. Find Python 3.10+ (py launcher > python) ---
$pyCmd = $null
foreach ($cand in @(@("py","-3"), @("python"))) {
  try {
    $v = & $cand[0] @($cand[1..($cand.Length-1)]) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
    if ($v) {
      $parts = $v.Trim().Split('.')
      if ([int]$parts[0] -ge 3 -and [int]$parts[1] -ge 10) { $pyCmd = $cand; break }
    }
  } catch {}
}
if (-not $pyCmd) {
  Write-Host "ERROR: Python >= 3.10 not found." -ForegroundColor Red
  Write-Host "  Download from https://www.python.org/downloads/ (check 'Add python.exe to PATH'), then re-run this script."
  exit 1
}
$pyVer = & $pyCmd[0] @($pyCmd[1..($pyCmd.Length-1)]) --version
Write-Host "Python: $pyVer"

# --- 2. Install into a venv (no admin rights needed) ---
Write-Host "Installing into venv: $VenvDir"
& $pyCmd[0] @($pyCmd[1..($pyCmd.Length-1)]) -m venv $VenvDir
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: failed to create venv at $VenvDir" -ForegroundColor Red; exit 1 }
$venvPy = Join-Path $VenvDir "Scripts\python.exe"
$venvBin = Join-Path $VenvDir "Scripts"
& $venvPy -m pip install --quiet --upgrade pip
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: pip upgrade failed" -ForegroundColor Red; exit 1 }
& $venvPy -m pip install --quiet "agent-revert @ git+https://github.com/kaia-cod/agent-revert"
  if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: pip install of agent-revert failed" -ForegroundColor Red; exit 1 }
}

$exe = Join-Path $venvBin "agent-revert.exe"
if (Test-Path $exe) {
  Write-Host "OK: installed. Launcher: $exe" -ForegroundColor Green
  & $exe --help | Select-Object -First 1
} else {
  Write-Host "Installed. Launcher: $(Join-Path $venvBin 'agent-revert')"
}
Write-Host ""
Write-Host "To use it everywhere, add to PATH (one-time, current user):"
Write-Host "  [Environment]::SetEnvironmentVariable('Path', `"$venvBin;`$env:Path`", 'User')"
Write-Host "Then open a NEW PowerShell and run:  agent-revert --help"
