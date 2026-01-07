# Android App Build Script

Write-Host "`nDigital Coloring App - Android Build`n" -ForegroundColor Cyan

# Check Android SDK
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    $androidHome = $env:ANDROID_SDK_ROOT
}

if ($androidHome) {
    Write-Host "Android SDK: $androidHome" -ForegroundColor Green
} else {
    Write-Host "WARNING: Android SDK not found" -ForegroundColor Yellow
    Write-Host "Please install Android Studio or set ANDROID_HOME`n" -ForegroundColor Yellow
}

# Check backend
Write-Host "`nChecking backend server..." -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Backend is running on port 8080" -ForegroundColor Green
} catch {
    Write-Host "Backend not running - start it first!" -ForegroundColor Red
}

Write-Host "`nBuild options:" -ForegroundColor Cyan
Write-Host "1) Show project info"
Write-Host "2) Create Gradle wrapper"
Write-Host "3) Build debug APK"
Write-Host "4) Install on device"

$choice = Read-Host "`nChoice (1-4)"

cd e:\git\cloud-gallery\android

switch ($choice) {
    "1" {
        Write-Host "`nProject: com.cloudgallery.portfolio" -ForegroundColor White
        Write-Host "Min SDK: 24, Target SDK: 34" -ForegroundColor White
        Write-Host "`nLayouts:" -ForegroundColor Cyan
        Get-ChildItem "app\src\main\res\layout" -Name
        Write-Host "`nKotlin files:" -ForegroundColor Cyan
        Get-ChildItem "app\src\main\java\com\cloudgallery\portfolio" -Recurse -Filter "*.kt" | Select-Object -First 5 -ExpandProperty Name
    }
    "2" {
        Write-Host "`nCreating Gradle wrapper..." -ForegroundColor Yellow
        gradle wrapper --gradle-version 8.2
    }
    "3" {
        Write-Host "`nBuilding debug APK..." -ForegroundColor Yellow
        if (Test-Path ".\gradlew.bat") {
            .\gradlew.bat assembleDebug
        } else {
            Write-Host "Gradle wrapper not found. Run option 2 first" -ForegroundColor Red
        }
    }
    "4" {
        Write-Host "`nConnected devices:" -ForegroundColor Yellow
        adb devices
        Write-Host "`nInstalling..." -ForegroundColor Yellow
        if (Test-Path ".\gradlew.bat") {
            .\gradlew.bat installDebug
        } else {
            Write-Host "Gradle wrapper not found. Run option 2 first" -ForegroundColor Red
        }
    }
}

Write-Host "`n"
