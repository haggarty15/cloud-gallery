#!/usr/bin/env pwsh
# Check Phone Connection Status

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Pixel 7a Connection Checker" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Set ADB path
$adb = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"

# Check if ADB exists
Write-Host "[CHECK] ADB installation..." -ForegroundColor Yellow
if (Test-Path $adb) {
    Write-Host "   [OK] ADB found at: $adb" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] ADB not found!" -ForegroundColor Red
    Write-Host "   Expected location: $adb" -ForegroundColor Yellow
    Write-Host "   Install Android SDK Platform Tools" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Restart ADB server
Write-Host "[ACTION] Restarting ADB server..." -ForegroundColor Yellow
& $adb kill-server | Out-Null
Start-Sleep -Seconds 1
& $adb start-server | Out-Null
Write-Host "   [OK] ADB server restarted" -ForegroundColor Green
Write-Host ""

# List devices
Write-Host "[CHECK] Connected devices..." -ForegroundColor Yellow
$deviceList = & $adb devices
Write-Host $deviceList

# Parse device list
$devices = & $adb devices | Select-String "device$" | Where-Object { $_ -notmatch "List of devices" }

if ($devices) {
    Write-Host ""
    Write-Host "   [OK] Device(s) connected!" -ForegroundColor Green
    Write-Host ""

    # Get device details
    Write-Host "[INFO] Device details:" -ForegroundColor Cyan
    $model = & $adb shell getprop ro.product.model 2>$null
    $android = & $adb shell getprop ro.build.version.release 2>$null
    $sdk = & $adb shell getprop ro.build.version.sdk 2>$null

    if ($model) {
        Write-Host "   Model: $model" -ForegroundColor White
        Write-Host "   Android: $android (API $sdk)" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "[OK] Your phone is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Yellow
    Write-Host "  1. Run app from Android Studio" -ForegroundColor White
    Write-Host "  2. Or run: .\check-and-run.ps1 -Build -Run" -ForegroundColor White
    Write-Host "======================================" -ForegroundColor Cyan

} else {
    Write-Host ""
    Write-Host "   [WARN] No devices detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "On your Pixel 7a:" -ForegroundColor Cyan
    Write-Host "  1. Go to Settings > About phone" -ForegroundColor White
    Write-Host "  2. Tap 'Build number' 7 times rapidly" -ForegroundColor White
    Write-Host "  3. Go to Settings > System > Developer options" -ForegroundColor White
    Write-Host "  4. Enable 'USB debugging'" -ForegroundColor White
    Write-Host ""
    Write-Host "On your computer:" -ForegroundColor Cyan
    Write-Host "  5. Unplug and replug USB cable" -ForegroundColor White
    Write-Host "  6. On phone, tap 'Allow' when prompted" -ForegroundColor White
    Write-Host "  7. Check 'Always allow from this computer'" -ForegroundColor White
    Write-Host "  8. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Cyan
    Write-Host "  • Try a different USB cable" -ForegroundColor Gray
    Write-Host "  • Try a different USB port (plug directly, avoid hubs)" -ForegroundColor Gray
    Write-Host "  • Swipe down on phone > tap 'USB charging' > select 'File Transfer'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Full guide: CONNECT_PHONE.md" -ForegroundColor Yellow
    Write-Host "======================================" -ForegroundColor Cyan
}

Write-Host ""

