#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start the Cloud Gallery backend server with all prerequisites

.DESCRIPTION
    This script:
    1. Checks if PostgreSQL is running (optional - warns but continues)
    2. Activates Python virtual environment
    3. Verifies required packages are installed
    4. Starts Flask development server

.EXAMPLE
    .\start-backend.ps1
#>

param(
    [switch]$SkipChecks = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Cloud Gallery Backend Server" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
$BackendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $BackendDir
Write-Host "📁 Working directory: $BackendDir" -ForegroundColor Gray
Write-Host ""

# Check if .venv exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "🐍 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check Python version
$PythonVersion = python --version
Write-Host "   Python version: $PythonVersion" -ForegroundColor Gray
Write-Host ""

if (-not $SkipChecks) {
    # Check if required packages are installed
    Write-Host "📦 Checking required packages..." -ForegroundColor Yellow

    $RequiredPackages = @(
        "flask",
        "flask-cors",
        "flask-sqlalchemy",
        "opencv-python",
        "scikit-learn",
        "firebase-admin"
    )

    $MissingPackages = @()

    foreach ($Package in $RequiredPackages) {
        $Installed = pip list 2>$null | Select-String -Pattern "^$Package\s" -Quiet
        if (-not $Installed) {
            $MissingPackages += $Package
        }
    }

    if ($MissingPackages.Count -gt 0) {
        Write-Host "   ⚠️  Missing packages: $($MissingPackages -join ', ')" -ForegroundColor Yellow
        Write-Host "   Installing from requirements.txt..." -ForegroundColor Yellow
        pip install -r requirements.txt -q
        Write-Host "   ✅ Packages installed" -ForegroundColor Green
    } else {
        Write-Host "   ✅ All required packages installed" -ForegroundColor Green
    }
    Write-Host ""

    # Check PostgreSQL (optional - warn but don't fail)
    Write-Host "🗄️  Checking PostgreSQL..." -ForegroundColor Yellow
    $PostgresService = Get-Service -Name "*postgres*" -ErrorAction SilentlyContinue

    if ($PostgresService -and $PostgresService.Status -eq "Running") {
        Write-Host "   ✅ PostgreSQL is running" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  PostgreSQL not running (database features will be limited)" -ForegroundColor Yellow
        Write-Host "   Backend will still start but database operations will fail" -ForegroundColor Gray
    }
    Write-Host ""

    # Check .env file
    Write-Host "⚙️  Checking configuration..." -ForegroundColor Yellow
    if (Test-Path ".env") {
        Write-Host "   ✅ .env file found" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  .env file not found - using defaults" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Start Flask server
Write-Host "🌐 Starting Flask server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "Server will start on:" -ForegroundColor Green
Write-Host "  • Local:   http://127.0.0.1:8080" -ForegroundColor White
Write-Host "  • Network: http://0.0.0.0:8080" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Run Flask server
try {
    python run.py
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped with error: $_" -ForegroundColor Red
    exit 1
}

