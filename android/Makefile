# Android Makefile
# Usage: make <target>

.PHONY: help build run install clean check logs

JAVA_HOME = C:\Program Files\Android\Android Studio\jbr
ADB = $(LOCALAPPDATA)\Android\Sdk\platform-tools\adb.exe
GRADLE = gradlew.bat
APK = app\build\outputs\apk\debug\app-debug.apk

help:
	@echo Android App - Available Commands
	@echo ===============================
	@echo.
	@echo   make build          - Build debug APK
	@echo   make run            - Build and run on device
	@echo   make install        - Install APK on device
	@echo   make clean          - Clean build files
	@echo   make check          - Check device connection
	@echo   make logs           - Show app logs
	@echo   make firebase       - Check Firebase auth status
	@echo.

build:
	@echo Building Android app...
	set JAVA_HOME=$(JAVA_HOME) && $(GRADLE) assembleDebug

run: build install
	@echo Launching app...
	$(ADB) shell am start -n com.cloudgallery.portfolio/.ui.MainActivity

install:
	@echo Installing app on device...
	@if not exist "$(APK)" (echo Error: APK not found. Run 'make build' first. && exit 1)
	$(ADB) install -r $(APK)

clean:
	@echo Cleaning build files...
	$(GRADLE) clean

check:
	@echo Checking device connection...
	@$(ADB) devices
	@echo.
	@$(ADB) devices | findstr "device$$" >nul 2>&1 && (echo [OK] Device connected) || (echo [X] No device found)

logs:
	@echo Showing app logs (Ctrl+C to stop)...
	$(ADB) logcat | findstr cloudgallery

firebase:
	@echo Firebase Authentication Status
	@echo ============================
	@$(ADB) logcat -d | findstr FirebaseAuth | more

# Quick shortcuts
b: build
r: run
i: install
c: clean

