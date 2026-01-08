# Cloud Gallery - Main Makefile
# Usage: make <target>

.PHONY: help android backend clean

# Default target
help:
	@echo Cloud Gallery - Available Commands
	@echo ================================
	@echo.
	@echo Android:
	@echo   make android-build     - Build Android app
	@echo   make android-run       - Build and run on device
	@echo   make android-install   - Install APK on device
	@echo   make android-check     - Check device connection
	@echo   make android-clean     - Clean Android build
	@echo.
	@echo Backend:
	@echo   make backend-start     - Start Flask server
	@echo   make backend-test      - Test canvas processor
	@echo   make backend-setup     - Setup virtual environment
	@echo.
	@echo General:
	@echo   make clean            - Clean all builds
	@echo   make status           - Show project status

# Android targets
android-build:
	@echo Building Android app...
	cd android && gradlew.bat assembleDebug

android-run:
	@echo Building and running Android app...
	cd android && gradlew.bat assembleDebug
	cd android && powershell -File check-and-run.ps1 -Run

android-install:
	@echo Installing app on device...
	cd android && adb install -r app\build\outputs\apk\debug\app-debug.apk

android-check:
	@echo Checking device connection...
	cd android && powershell -File check-phone.ps1

android-clean:
	@echo Cleaning Android build...
	cd android && gradlew.bat clean

# Backend targets
backend-start:
	@echo Starting backend server...
	cd backend && powershell -File start-backend.ps1

backend-test:
	@echo Testing canvas processor...
	cd backend && .venv\Scripts\python.exe app\canvas_processor.py ..\test-photos\boba.jpg 20

backend-setup:
	@echo Setting up backend virtual environment...
	cd backend && python -m venv .venv
	cd backend && .venv\Scripts\pip.exe install -r requirements.txt

# General targets
clean:
	@echo Cleaning all builds...
	cd android && gradlew.bat clean
	@echo Clean complete!

status:
	@echo Project Status
	@echo =============
	@echo Android: Checking build...
	@if exist android\app\build\outputs\apk\debug\app-debug.apk (echo   [OK] APK exists) else (echo   [X] APK not built)
	@echo Backend: Checking venv...
	@if exist backend\.venv (echo   [OK] Virtual environment exists) else (echo   [X] Virtual environment not setup)
	@echo Device: Checking connection...
	@powershell -Command "& '$(LOCALAPPDATA)\Android\Sdk\platform-tools\adb.exe' devices | Select-String 'device$$' | Measure-Object | ForEach-Object { if ($$_.Count -gt 0) { Write-Host '  [OK] Device connected' } else { Write-Host '  [X] No device' } }"

