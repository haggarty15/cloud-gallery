#!/usr/bin/env pwsh
# Automatic Android Project Setup and Build Script
# This script handles ALL prerequisites before running the app

param(
    [switch]$SkipBuild = $false
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   ANDROID PROJECT AUTO-SETUP & BUILD                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check backend
Write-Host "[1/6] Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "      ✓ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Backend is NOT running!" -ForegroundColor Red
    Write-Host "      Starting backend..." -ForegroundColor Yellow

    $backendPath = Join-Path (Split-Path $PSScriptRoot -Parent) "backend"
    $venvPath = Join-Path $backendPath ".venv"

    if (Test-Path $venvPath) {
        Start-Process powershell -ArgumentList @(
            "-NoExit",
            "-Command",
            "cd '$backendPath'; .\.venv\Scripts\Activate.ps1; `$env:FLASK_APP='app'; python -m flask run --host=0.0.0.0 --port=8080"
        ) -WindowStyle Normal
        Write-Host "      Backend starting in new window..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    } else {
        Write-Host "      ⚠ Backend venv not found. Please start manually." -ForegroundColor Yellow
    }
}

# Step 2: Find Android SDK
Write-Host ""
Write-Host "[2/6] Locating Android SDK..." -ForegroundColor Yellow

$sdkPaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "$env:USERPROFILE\AppData\Local\Android\Sdk",
    "C:\Android\Sdk",
    "$env:ANDROID_HOME",
    "$env:ANDROID_SDK_ROOT"
)

$androidSdk = $null
foreach ($path in $sdkPaths) {
    if ($path -and (Test-Path $path)) {
        $androidSdk = $path
        Write-Host "      ✓ Found Android SDK: $androidSdk" -ForegroundColor Green
        break
    }
}

if (-not $androidSdk) {
    Write-Host "      ⚠ Android SDK not found automatically" -ForegroundColor Yellow
    Write-Host "      Android Studio will prompt for SDK location on first run" -ForegroundColor Gray
} else {
    # Create local.properties with SDK path
    $localPropsPath = Join-Path $PSScriptRoot "local.properties"
    $sdkPathNormalized = $androidSdk -replace '\\', '/'
    "sdk.dir=$sdkPathNormalized" | Out-File -FilePath $localPropsPath -Encoding utf8 -Force
    Write-Host "      ✓ Created local.properties with SDK path" -ForegroundColor Green
}

# Step 3: Check Java/JDK
Write-Host ""
Write-Host "[3/6] Checking Java..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    Write-Host "      ✓ $javaVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Java not found! Install JDK 17 or higher" -ForegroundColor Red
    Write-Host "      Android Studio includes JDK, so this should work from IDE" -ForegroundColor Yellow
}

# Step 4: Verify Gradle wrapper
Write-Host ""
Write-Host "[4/6] Verifying Gradle wrapper..." -ForegroundColor Yellow

if (Test-Path ".\gradlew.bat") {
    Write-Host "      ✓ Gradle wrapper exists" -ForegroundColor Green
} else {
    Write-Host "      ✗ Gradle wrapper missing!" -ForegroundColor Red
    exit 1
}

# Step 5: Check project structure
Write-Host ""
Write-Host "[5/6] Verifying project structure..." -ForegroundColor Yellow

$requiredFiles = @(
    "build.gradle",
    "settings.gradle",
    "app\build.gradle",
    "app\src\main\AndroidManifest.xml",
    "app\src\main\java\com\cloudgallery\portfolio\di\NetworkModule.kt"
)

$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "      ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Missing: $file" -ForegroundColor Red
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Host ""
    Write-Host "      Project structure incomplete!" -ForegroundColor Red
    exit 1
}

# Step 6: Build the project
if (-not $SkipBuild) {
    Write-Host ""
    Write-Host "[6/6] Building project with Gradle..." -ForegroundColor Yellow
    Write-Host "      This will download dependencies (first time: 5-10 minutes)" -ForegroundColor Gray
    Write-Host ""

    # Run Gradle build
    Write-Host "      Running: .\gradlew.bat assembleDebug" -ForegroundColor Gray
    Write-Host ""

    $buildProcess = Start-Process -FilePath ".\gradlew.bat" -ArgumentList "assembleDebug", "--stacktrace" -NoNewWindow -Wait -PassThru

    if ($buildProcess.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "      ✓ BUILD SUCCESSFUL!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "      ✗ Build failed with exit code: $($buildProcess.ExitCode)" -ForegroundColor Red
        Write-Host ""
        Write-Host "      Common issues:" -ForegroundColor Yellow
        Write-Host "      - Missing Android SDK (set in Android Studio)" -ForegroundColor Gray
        Write-Host "      - Missing SDK components (install via SDK Manager)" -ForegroundColor Gray
        Write-Host "      - Internet connection required for first build" -ForegroundColor Gray
        Write-Host ""
        Write-Host "      Try running the app from Android Studio instead:" -ForegroundColor Yellow
        Write-Host "      1. Open project in Android Studio" -ForegroundColor White
        Write-Host "      2. Wait for indexing to complete" -ForegroundColor White
        Write-Host "      3. Click green ▶ Run button" -ForegroundColor White
        Write-Host ""
        exit $buildProcess.ExitCode
    }
} else {
    Write-Host ""
    Write-Host "[6/6] Skipping build (use -SkipBuild `$false to build)" -ForegroundColor Gray
}

# Final summary
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   SETUP COMPLETE - READY TO RUN!                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if ($buildProcess -and $buildProcess.ExitCode -eq 0) {
    Write-Host "✓ All prerequisites completed" -ForegroundColor Green
    Write-Host "✓ Project built successfully" -ForegroundColor Green
    Write-Host "✓ APK ready to install" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps in Android Studio:" -ForegroundColor Yellow
    Write-Host "  1. Project is already synced and built" -ForegroundColor White
    Write-Host "  2. Click the green ▶ Run button" -ForegroundColor White
    Write-Host "  3. Select your emulator or device" -ForegroundColor White
    Write-Host "  4. App will install and launch!" -ForegroundColor White
    Write-Host ""
    Write-Host "APK location: .\app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor Gray
} else {
    Write-Host "Project structure verified" -ForegroundColor Green
    Write-Host ""
    Write-Host "Run from Android Studio:" -ForegroundColor Yellow
    Write-Host "  1. Open this project in Android Studio" -ForegroundColor White
    Write-Host "  2. Click ▶ Run (it will auto-sync and build)" -ForegroundColor White
    Write-Host "  3. Select emulator/device" -ForegroundColor White
}

Write-Host ""

