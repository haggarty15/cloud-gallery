#!/usr/bin/env pwsh
# Quick Firebase Authentication Test Script

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Firebase Authentication Status" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Firebase Project Info
Write-Host "Firebase Project:" -ForegroundColor Yellow
Write-Host "  Project ID: image-gallery-481812" -ForegroundColor White
Write-Host "  Console: https://console.firebase.google.com/project/image-gallery-481812" -ForegroundColor White
Write-Host ""

# Check what's in the logs
Write-Host "Checking device logs for auth attempts..." -ForegroundColor Yellow
$adb = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"

if (Test-Path $adb) {
    $authLogs = & $adb logcat -d | Select-String -Pattern "FirebaseAuth" | Select-Object -Last 10

    if ($authLogs) {
        Write-Host "  Recent authentication attempts:" -ForegroundColor Cyan
        $authLogs | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    } else {
        Write-Host "  No recent authentication attempts found" -ForegroundColor Gray
    }
} else {
    Write-Host "  ADB not found, cannot check logs" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1: Create Account (Email/Password)" -ForegroundColor Cyan
Write-Host "  1. Open app on your phone" -ForegroundColor White
Write-Host "  2. Tap 'Sign Up' (not Login!)" -ForegroundColor White
Write-Host "  3. Enter email: kylehaggarty@gmail.com" -ForegroundColor White
Write-Host "  4. Enter password (min 6 chars)" -ForegroundColor White
Write-Host "  5. Confirm password" -ForegroundColor White
Write-Host "  6. Tap 'Sign Up'" -ForegroundColor White
Write-Host "  7. Wait for success message" -ForegroundColor White
Write-Host ""

Write-Host "Option 2: Google Sign-In (Recommended!)" -ForegroundColor Cyan
Write-Host "  1. Open app on your phone" -ForegroundColor White
Write-Host "  2. Tap 'Sign in with Google' button" -ForegroundColor White
Write-Host "  3. Select your Google account" -ForegroundColor White
Write-Host "  4. Done! Auto-creates account" -ForegroundColor White
Write-Host ""

Write-Host "Common Mistakes:" -ForegroundColor Yellow
Write-Host "  X Trying to 'Login' without creating account first" -ForegroundColor Red
Write-Host "  X Using wrong password" -ForegroundColor Red
Write-Host "  X Network timeout during sign up" -ForegroundColor Red
Write-Host ""

Write-Host "Check Firebase Console:" -ForegroundColor Yellow
Write-Host "  URL: https://console.firebase.google.com/project/image-gallery-481812/authentication/users" -ForegroundColor White
Write-Host "  Should see your user listed after successful sign up" -ForegroundColor Gray
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

