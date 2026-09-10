param()

# run_local.ps1 — helper to install deps, migrate, and run Django dev server
# Usage: Open PowerShell in this folder and run .\run_local.ps1

$ErrorActionPreference = 'Stop'

# ensure script runs from this file's directory (manage.py is here)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "Working directory: $PWD"

# find Python launcher
$pyCmd = Get-Command py -ErrorAction SilentlyContinue
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pyCmd) { $launcher = 'py' }
elseif ($pythonCmd) { $launcher = 'python' }
else {
    Write-Error "Python not found. Please install Python 3.11+ and ensure 'py' or 'python' is in PATH."
    exit 1
}

function Run([string[]]$commandArgs) {
    Write-Host "=> $($commandArgs -join ' ')"
    if ($launcher -eq 'py') { & py -3 @commandArgs }
    else { & python @commandArgs }
}

# install dependencies
Write-Host "Installing dependencies from requirements.txt..."
try {
    if ($launcher -eq 'py') { & py -3 -m pip install --upgrade pip }
    else { & python -m pip install --upgrade pip }
} catch {
    Write-Warning "Could not upgrade pip (continuing)."
}

if ($launcher -eq 'py') { & py -3 -m pip install -r requirements.txt } else { & python -m pip install -r requirements.txt }

# apply migrations
Write-Host "Applying migrations..."
Run @('manage.py', 'migrate')

# create superuser prompt (optional)
Write-Host "If you need a superuser, run: manage.py createsuperuser"

# run server
Write-Host "Starting Django development server on port 8000..."
Run @('manage.py', 'runserver', '0.0.0.0:8000')
