@echo off
REM Simple build script for Android project
echo.
echo ========================================
echo   BUILDING ANDROID PROJECT
echo ========================================
echo.

echo [1/3] Checking prerequisites...
if not exist "gradlew.bat" (
    echo ERROR: gradlew.bat not found!
    exit /b 1
)
echo       OK - Gradle wrapper found

echo.
echo [2/3] Syncing and downloading dependencies...
echo       This may take 5-10 minutes on first run
echo.
call gradlew.bat tasks --quiet >nul 2>&1
if errorlevel 1 (
    echo       First-time setup, downloading Gradle...
)

echo.
echo [3/3] Building debug APK...
echo.
call gradlew.bat assembleDebug --stacktrace

if errorlevel 1 (
    echo.
    echo ========================================
    echo   BUILD FAILED
    echo ========================================
    echo.
    echo Common solutions:
    echo  1. Open project in Android Studio
    echo  2. Let it configure the SDK automatically
    echo  3. Then run this script again
    echo.
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo APK created: app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo Now in Android Studio:
    echo  1. Click the green Run button
    echo  2. Select an emulator
    echo  3. App will install and launch!
    echo.
)

