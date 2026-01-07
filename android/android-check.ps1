#!/usr/bin/env pwsh
# Android App - Prerequisites Check and Run Script
# Usage: .\android-check.ps1 [-Build] [-Run]

param(
    [switch]$Build = $false,
    [switch]$Run = $false
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Cloud Gallery Android - Startup Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Change to android directory
$AndroidDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $AndroidDir
Write-Host "[INFO] Working directory: $AndroidDir" -ForegroundColor Gray
Write-Host ""

# Check for google-services.json
Write-Host "[CHECK] Firebase configuration..." -ForegroundColor Yellow
if (Test-Path "app\google-services.json") {
    $FileSize = (Get-Item "app\google-services.json").Length
    Write-Host "   [OK] google-services.json found ($FileSize bytes)" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] google-services.json NOT FOUND!" -ForegroundColor Red
    Write-Host "   This file is required for Firebase authentication" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check for local.properties
Write-Host "[CHECK] Android SDK configuration..." -ForegroundColor Yellow
if (Test-Path "local.properties") {
    $SdkPath = Get-Content "local.properties" | Select-String "sdk.dir" | ForEach-Object { $_.ToString().Split('=')[1] }
    if ($SdkPath) {
        Write-Host "   [OK] Android SDK found" -ForegroundColor Green
    } else {
        Write-Host "   [WARN] SDK path not found in local.properties" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [WARN] local.properties not found" -ForegroundColor Yellow
    Write-Host "   Android Studio should create this automatically" -ForegroundColor Gray
}
Write-Host ""

# Check and set JAVA_HOME
Write-Host "[CHECK] Java..." -ForegroundColor Yellow
if (-not $env:JAVA_HOME) {
    # Try to find Android Studio's bundled JDK
    $JdkPaths = @(
        "C:\Program Files\Android\Android Studio\jbr",
        "C:\Program Files\Android\Android Studio\jre"
    )

    foreach ($JdkPath in $JdkPaths) {
        if (Test-Path $JdkPath) {
            $env:JAVA_HOME = $JdkPath
            Write-Host "   [OK] Set JAVA_HOME to: $JdkPath" -ForegroundColor Green
            break
        }
    }

    if (-not $env:JAVA_HOME) {
        Write-Host "   [ERROR] JAVA_HOME not set and could not find JDK!" -ForegroundColor Red
        Write-Host "   Please install Android Studio or set JAVA_HOME manually" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "   [OK] JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Green
}
Write-Host ""

# Check Gradle wrapper
Write-Host "[CHECK] Gradle..." -ForegroundColor Yellow
if (Test-Path "gradlew.bat") {
    Write-Host "   [OK] Gradle wrapper found" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] gradlew.bat not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check for connected devices if adb available
if ($env:ANDROID_HOME) {
    Write-Host "[CHECK] Connected devices..." -ForegroundColor Yellow
    $AdbPath = Join-Path $env:ANDROID_HOME "platform-tools\adb.exe"
    if (Test-Path $AdbPath) {
        $Devices = & $AdbPath devices 2>&1 | Select-String "device$" | Where-Object { $_ -notmatch "List of devices" }

        if ($Devices) {
            Write-Host "   [OK] Device(s) connected" -ForegroundColor Green
            $Devices | ForEach-Object {
                Write-Host "      - $_" -ForegroundColor Gray
            }
        } else {
            Write-Host "   [WARN] No devices connected" -ForegroundColor Yellow
            Write-Host "   Connect a device or start an emulator in Android Studio" -ForegroundColor Gray
        }
    }
    Write-Host ""
}

# Build if requested
if ($Build) {
    Write-Host "[BUILD] Building debug APK..." -ForegroundColor Cyan
    Write-Host "   (This may take a few minutes)" -ForegroundColor Gray
    Write-Host ""

    & .\gradlew.bat assembleDebug

    if ($LASTEXITCODE -eq 0) {
        $ApkPath = "app\build\outputs\apk\debug\app-debug.apk"
        if (Test-Path $ApkPath) {
            $ApkSize = [math]::Round((Get-Item $ApkPath).Length / 1MB, 2)
            Write-Host ""
            Write-Host "   [OK] APK built: $ApkSize MB" -ForegroundColor Green
            Write-Host "   Location: $ApkPath" -ForegroundColor Gray
        }
    } else {
        Write-Host ""
        Write-Host "   [ERROR] Build failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Run if requested
if ($Run) {
    if (-not $Build) {
        Write-Host "[BUILD] Building before running..." -ForegroundColor Cyan
        & .\gradlew.bat assembleDebug
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   [ERROR] Build failed!" -ForegroundColor Red
            exit 1
        }
    }

    Write-Host "[RUN] Installing and launching app..." -ForegroundColor Cyan
    & .\gradlew.bat installDebug

    if ($LASTEXITCODE -eq 0) {
        if ($env:ANDROID_HOME) {
            $AdbPath = Join-Path $env:ANDROID_HOME "platform-tools\adb.exe"
            & $AdbPath shell am start -n com.cloudgallery.portfolio/.MainActivity
        }
        Write-Host "   [OK] App launched" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] Installation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
if (-not $Build -and -not $Run) {
    Write-Host "[OK] Prerequisites check complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To build and run from command line:" -ForegroundColor Yellow
    Write-Host "  .\android-check.ps1 -Build -Run" -ForegroundColor White
    Write-Host ""
    Write-Host "Or open in Android Studio and click Run" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Done!" -ForegroundColor Green
}
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

