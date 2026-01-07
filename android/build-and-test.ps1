# Android App Build & Test Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  DIGITAL COLORING APP - ANDROID BUILD" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check prerequisites
Write-Host "1. Checking prerequisites..." -ForegroundColor Yellow

# Check if Android SDK is available
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    $androidHome = $env:ANDROID_SDK_ROOT
}

if ($androidHome) {
    Write-Host "   ✓ Android SDK found: $androidHome" -ForegroundColor Green
} else {
    Write-Host "   ✗ Android SDK not found!" -ForegroundColor Red
    Write-Host "   Please install Android Studio or set ANDROID_HOME environment variable" -ForegroundColor Yellow
    Write-Host "`n   Quick fix:" -ForegroundColor Cyan
    Write-Host '   $env:ANDROID_HOME = "C:\Users\<YourUsername>\AppData\Local\Android\Sdk"' -ForegroundColor White
    exit 1
}

# Check Java
$javaVersion = java -version 2>&1 | Select-String "version"
if ($javaVersion) {
    Write-Host "   ✓ Java found: $javaVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Java not found! Please install JDK 17" -ForegroundColor Red
    exit 1
}

# Step 2: Check backend server
Write-Host "`n2. Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✓ Backend server is running on port 8080" -ForegroundColor Green
    }
} catch {
    Write-Host "   ✗ Backend server not running!" -ForegroundColor Red
    Write-Host "   Please start the Flask server first:" -ForegroundColor Yellow
    Write-Host "   cd e:\git\cloud-gallery\backend" -ForegroundColor White
    Write-Host '   $env:FLASK_APP="app"; e:\git\cloud-gallery\backend\.venv\Scripts\python.exe -m flask run --host=0.0.0.0 --port=8080' -ForegroundColor White
    
    $continue = Read-Host "`n   Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit 1
    }
}

# Step 3: Update API base URL in strings.xml
Write-Host "`n3. Configuring API endpoint..." -ForegroundColor Yellow
$stringsPath = "e:\git\cloud-gallery\android\app\src\main\res\values\strings.xml"
$content = Get-Content $stringsPath -Raw

# Get local IP for testing (use 10.0.2.2 for emulator)
Write-Host "   Select API endpoint:" -ForegroundColor Cyan
Write-Host "   1) 10.0.2.2:8080 (Android Emulator)" -ForegroundColor White
Write-Host "   2) localhost:8080 (Physical device with USB debugging)" -ForegroundColor White
Write-Host "   3) <Your local IP>:8080 (Physical device on same network)" -ForegroundColor White

$choice = Read-Host "   Choice (1-3)"
switch ($choice) {
    "1" { $apiUrl = "http://10.0.2.2:8080" }
    "2" { $apiUrl = "http://localhost:8080" }
    "3" {
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" -and $_.InterfaceAlias -notlike "*Virtual*" } | Select-Object -First 1).IPAddress
        $apiUrl = "http://${localIP}:8080"
        Write-Host "   Using local IP: $localIP" -ForegroundColor Cyan
    }
    default { $apiUrl = "http://10.0.2.2:8080" }
}

Write-Host "   API URL: $apiUrl" -ForegroundColor Green

# Step 4: List available build options
Write-Host "`n4. Build options:" -ForegroundColor Yellow
Write-Host "   1) Check for errors (dry run)" -ForegroundColor White
Write-Host "   2) Build debug APK" -ForegroundColor White
Write-Host "   3) Build and install on connected device" -ForegroundColor White
Write-Host "   4) Just show project info" -ForegroundColor White

$buildChoice = Read-Host "`n   Choice (1-4)"

cd e:\git\cloud-gallery\android

switch ($buildChoice) {
    "1" {
        Write-Host "`nRunning gradle tasks to check project..." -ForegroundColor Yellow
        if (Test-Path ".\gradlew.bat") {
            .\gradlew.bat tasks
        } else {
            Write-Host "   Creating Gradle wrapper..." -ForegroundColor Yellow
            gradle wrapper
            .\gradlew.bat tasks
        }
    }
    "2" {
        Write-Host "`nBuilding debug APK..." -ForegroundColor Yellow
        if (Test-Path ".\gradlew.bat") {
            .\gradlew.bat assembleDebug
        } else {
            Write-Host "   Creating Gradle wrapper..." -ForegroundColor Yellow
            gradle wrapper
            .\gradlew.bat assembleDebug
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✓ Build successful!" -ForegroundColor Green
            $apkPath = "app\build\outputs\apk\debug\app-debug.apk"
            if (Test-Path $apkPath) {
                Write-Host "   APK location: $apkPath" -ForegroundColor Cyan
                Write-Host "`n   To install manually:" -ForegroundColor Yellow
                Write-Host "   adb install $apkPath" -ForegroundColor White
            }
        }
    }
    "3" {
        Write-Host "`nChecking for connected devices..." -ForegroundColor Yellow
        adb devices
        
        $install = Read-Host "`nBuild and install? (y/n)"
        if ($install -eq 'y') {
            if (Test-Path ".\gradlew.bat") {
                .\gradlew.bat installDebug
            } else {
                gradle wrapper
                .\gradlew.bat installDebug
            }
        }
    }
    "4" {
        Write-Host "`nProject Information:" -ForegroundColor Cyan
        Write-Host "   Package: com.cloudgallery.portfolio" -ForegroundColor White
        Write-Host "   Min SDK: 24 (Android 7.0)" -ForegroundColor White
        Write-Host "   Target SDK: 34 (Android 14)" -ForegroundColor White
        Write-Host "   Kotlin: 1.9.20" -ForegroundColor White
        Write-Host "   Dependencies: Firebase, Retrofit, Hilt, Coil" -ForegroundColor White
        
        Write-Host "`n   Layouts created:" -ForegroundColor Cyan
        Get-ChildItem "app\src\main\res\layout" | ForEach-Object { Write-Host "     - $($_.Name)" -ForegroundColor White }
        
        Write-Host "`n   Kotlin files:" -ForegroundColor Cyan
        Get-ChildItem "app\src\main\java\com\cloudgallery\portfolio" -Recurse -Filter "*.kt" | Select-Object -First 10 | ForEach-Object { Write-Host "     - $($_.Name)" -ForegroundColor White }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "To test the app:" -ForegroundColor Yellow
Write-Host "1. Make sure backend is running (http://localhost:8080)" -ForegroundColor White
Write-Host "2. Launch Android emulator or connect physical device" -ForegroundColor White
Write-Host "3. Run: .\gradlew.bat installDebug" -ForegroundColor White
Write-Host "4. Open app and sign in with Firebase" -ForegroundColor White
Write-Host "5. Upload a photo from test-photos folder" -ForegroundColor White
Write-Host "6. Start coloring!" -ForegroundColor White

Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
Write-Host "- If build fails, try: .\gradlew.bat clean" -ForegroundColor White
Write-Host "- For sync issues: File > Sync Project with Gradle Files in Android Studio" -ForegroundColor White
Write-Host "- Check logs: .\gradlew.bat assembleDebug --stacktrace" -ForegroundColor White

Write-Host "`n"
