# Makefile Commands Guide

## Overview

All PowerShell scripts have been converted to Makefile commands for easier use.

**Quick Start:**
```bash
make help              # Show all commands
make android-run       # Build and run Android app
make backend-start     # Start Flask server
```

---

## Installation

Make is already installed on your system (GNU Make 4.4.1).

---

## Main Commands (Root Directory)

### Android
```bash
make android-build      # Build Android app
make android-run        # Build and run on device
make android-install    # Install APK on device
make android-check      # Check device connection
make android-clean      # Clean Android build
```

### Backend
```bash
make backend-start      # Start Flask server
make backend-test       # Test canvas processor
make backend-setup      # Setup virtual environment
```

### General
```bash
make clean             # Clean all builds
make status            # Show project status
make help              # Show all commands
```

---

## Android Commands (android/ directory)

```bash
cd android

# Building
make build             # Build debug APK
make clean             # Clean build files

# Running
make run               # Build and run on device
make install           # Install APK on device

# Testing
make check             # Check device connection
make logs              # Show app logs
make firebase          # Check Firebase auth status

# Shortcuts
make b                 # Same as 'make build'
make r                 # Same as 'make run'
make i                 # Same as 'make install'
make c                 # Same as 'make clean'
```

---

## Backend Commands (backend/ directory)

```bash
cd backend

# Server
make start             # Start Flask server (http://localhost:8080)
make dev               # Same as start (shortcut)

# Testing
make test              # Test canvas processor with boba.jpg

# Setup
make setup             # Create venv and install dependencies
make install           # Install/update dependencies

# Cleanup
make clean             # Remove temporary files

# Shortcuts
make s                 # Same as 'make start'
make t                 # Same as 'make test'
```

---

## Comparison: PowerShell vs Make

### Before (PowerShell)
```powershell
.\check-and-run.ps1 -Build -Run
.\check-phone.ps1
.\start-backend.ps1
```

### After (Make)
```bash
make android-run
make android-check
make backend-start
```

**Benefits:**
- ✅ Shorter commands
- ✅ No need to remember script names
- ✅ Consistent across projects
- ✅ Tab completion works
- ✅ Cross-platform (works on Linux/Mac too)

---

## Quick Workflows

### First Time Setup
```bash
# Setup backend
make backend-setup

# Check Android device
make android-check

# Build and run
make android-run
```

### Daily Development
```bash
# Terminal 1: Start backend
make backend-start

# Terminal 2: Run Android app
make android-run
```

### Build Only
```bash
# Build Android
make android-build

# Or from root
cd android && make build
```

### Clean Everything
```bash
# From root
make clean

# Or individually
make android-clean
cd backend && make clean
```

---

## Examples

### Build and Run Android App
```bash
# From root
make android-run

# Or from android/
cd android
make run
```

### Start Backend Server
```bash
# From root
make backend-start

# Or from backend/
cd backend
make start
```

### Check Project Status
```bash
make status
```

Output:
```
Project Status
=============
Android: Checking build...
  [OK] APK exists
Backend: Checking venv...
  [OK] Virtual environment exists
Device: Checking connection...
  [OK] Device connected
```

### Test Canvas Processor
```bash
cd backend
make test
```

---

## PowerShell Scripts Status

### ✅ Converted to Make Commands

| Old Script | New Make Command |
|-----------|------------------|
| `check-and-run.ps1 -Build -Run` | `make android-run` |
| `check-phone.ps1` | `make android-check` |
| `check-firebase-auth.ps1` | `make android-firebase` |
| `start-backend.ps1` | `make backend-start` |
| `gradlew.bat assembleDebug` | `make android-build` |

### 📁 Scripts Kept (for advanced use)
- `android-check.ps1` - Detailed prerequisites check
- `check-and-run.ps1` - Full options available
- `check-phone.ps1` - Detailed device info
- `check-firebase-auth.ps1` - Detailed auth logs
- `start-backend.ps1` - Can be called by Make

**Recommendation:** Use Make commands for daily work, keep scripts for detailed debugging.

---

## Troubleshooting

### Make Command Not Found
```bash
# Check if Make is installed
make --version

# Install (if needed)
# Windows: Install via Chocolatey or Git for Windows
choco install make
```

### Commands Don't Work
```bash
# Make sure you're in the right directory
cd E:\git\cloud-gallery

# Check Makefile exists
ls Makefile

# Run with verbose output
make android-build -n  # Shows what would be executed
```

### ADB Not Found
The Makefile uses the default Android SDK location:
```
%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe
```

If your SDK is elsewhere, edit `android/Makefile` and update the `ADB` variable.

---

## Tips

### Tab Completion
Type `make ` and press TAB to see available commands.

### See What Make Will Do
```bash
make android-build -n    # Dry run (show commands)
```

### Run Multiple Commands
```bash
make clean android-build android-install
```

### Parallel Execution
```bash
make -j4 android-build backend-setup  # Run in parallel
```

---

## Summary

**Before:** 7+ PowerShell scripts to remember  
**After:** Simple `make` commands

**Common Tasks:**
```bash
make android-run        # Run Android app
make backend-start      # Start backend
make status            # Check everything
make clean             # Clean builds
```

**Your workflow is now much cleaner!** 🎉

