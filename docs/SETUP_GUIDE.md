# Cloud Gallery - Complete Setup Guide

**Last Updated:** January 7, 2026  
**Status:** ✅ Working - App runs on Android with Firebase authentication

---

## Quick Start

### Prerequisites
- Android Studio installed
- Android device or emulator
- Firebase project: `image-gallery-481812`

### Run the App (5 Minutes)

```powershell
# 1. Install and run
cd android
.\check-and-run.ps1 -Build -Run

# 2. Create account on phone
# - Tap "Sign Up"
# - Enter email and password
# - Done!
```

---

## Project Structure

```
cloud-gallery/
├── android/           # Android app (Kotlin)
│   ├── app/
│   │   ├── src/main/
│   │   └── google-services.json
│   └── *.ps1         # Helper scripts
├── backend/          # Flask API (Python)
│   ├── app/
│   └── .venv/
├── web/              # Frontend (React + Vite)
└── docs/             # Documentation
```

---

## Features Implemented

### ✅ Authentication
- Email/Password sign up and login
- Firebase Authentication
- Session management
- Logout functionality

### ✅ UI
- Modern Material Design 3
- Login screen with validation
- Sign up screen with password confirmation
- Home page with card-based navigation
- Responsive layouts

### ✅ Navigation
- Login → Sign Up flow
- Auto-login after sign up
- Protected home screen
- Navigation to Upload/Gallery

---

## Development Setup

### Android App

**Build:**
```powershell
cd android
.\gradlew.bat assembleDebug
```

**Install & Run:**
```powershell
.\check-and-run.ps1 -Build -Run
```

**Check Device:**
```powershell
.\check-phone.ps1
```

### Backend (Flask)

**Start Server:**
```powershell
cd backend
.\start-backend.ps1
```

**Test Canvas Processor:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app/canvas_processor.py ../test-photos/boba.jpg 20
```

---

## Firebase Configuration

### Project Details
- **Project ID:** `image-gallery-481812`
- **Project Number:** `564492032682`
- **Console:** https://console.firebase.google.com/project/image-gallery-481812

### Authentication Methods Enabled
- ✅ Email/Password
- ⚠️ Google Sign-In (requires SHA-1 setup)

### Your SHA-1 Fingerprint
```
D2:01:02:97:A2:53:37:1F:99:F1:9A:F9:A9:F0:3E:EF:E0:91:9B:A1
```

**To enable Google Sign-In:**
1. Go to Firebase Console → Project Settings
2. Add SHA-1 fingerprint to your Android app
3. Enable Google Sign-In in Authentication → Sign-in method
4. Rebuild app

---

## Common Commands

### Android
```powershell
# Build
cd android
.\gradlew.bat assembleDebug

# Clean build
.\gradlew.bat clean assembleDebug

# Install on device
.\check-and-run.ps1 -Run

# Check device connection
.\check-phone.ps1
```

### Backend
```powershell
# Start server
cd backend
.\start-backend.ps1

# Process image
python app/canvas_processor.py path/to/image.jpg 20
```

---

## Troubleshooting

### App Won't Install
```powershell
# Check device connection
cd android
.\check-phone.ps1

# Should show: [OK] Device(s) connected!
```

### Build Fails
```powershell
# Clean and rebuild
cd android
.\gradlew.bat clean
.\gradlew.bat assembleDebug
```

### Can't Login
- **Issue:** "Auth credential is incorrect"
- **Cause:** No account exists
- **Solution:** Use "Sign Up" first, then "Login"

### Google Sign-In Error :10
- **Issue:** OAuth not configured
- **Solution:** Add SHA-1 to Firebase Console (see Firebase Configuration above)

---

## Tech Stack

### Android App
- **Language:** Kotlin
- **UI:** Material Design 3, View Binding
- **Architecture:** MVVM
- **DI:** Hilt (with KSP)
- **Auth:** Firebase Authentication
- **Build:** Gradle 8.5, AGP 8.2.2

### Backend
- **Framework:** Flask
- **Image Processing:** OpenCV, NumPy
- **Language:** Python 3.x

---

## Next Steps

### Immediate
- [ ] Connect Upload screen to backend API
- [ ] Implement coloring canvas
- [ ] Save coloring progress

### Short Term
- [ ] Enable Google Sign-In
- [ ] Add profile screen
- [ ] Implement gallery view

### Long Term
- [ ] Deploy backend to Cloud Run
- [ ] Add social sharing
- [ ] Implement offline mode

---

## Important Files

### Configuration
- `android/app/google-services.json` - Firebase config
- `android/app/build.gradle` - App dependencies
- `backend/requirements.txt` - Python packages

### Scripts
- `android/check-and-run.ps1` - Build and run app
- `android/check-phone.ps1` - Check device connection
- `backend/start-backend.ps1` - Start Flask server

---

## Support

**Firebase Console:** https://console.firebase.google.com/project/image-gallery-481812  
**Backend:** http://localhost:8080 (when running)

---

## Quick Reference

**Create Account:**
```
1. Open app
2. Tap "Sign Up"
3. Enter email + password
4. Confirm password
5. Done!
```

**Login:**
```
1. Open app
2. Enter email + password (from sign up)
3. Tap "Login"
```

**Navigate:**
```
Home → Upload New Photo → Upload screen
Home → My Coloring Gallery → Gallery screen
Home → Logout → Back to login
```

---

Last updated: January 7, 2026

