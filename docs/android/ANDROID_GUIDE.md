# Android App Documentation

## Overview

Cloud Gallery Android app - Paint-by-numbers coloring from photos.

**Package:** `com.cloudgallery.portfolio`  
**Min SDK:** 24 (Android 7.0)  
**Target SDK:** 34 (Android 14)

---

## Architecture

### MVVM Pattern
```
UI Layer (Activities/Fragments)
    ↓
ViewModel Layer
    ↓
Repository Layer
    ↓
Data Layer (Firebase, API)
```

### Dependency Injection
- **Framework:** Hilt (Dagger)
- **Processor:** KSP (Kotlin Symbol Processing)

---

## Key Features

### Authentication
- Firebase email/password authentication
- Session management
- Auto-login on app start
- Secure logout

### Screens
1. **LoginActivity** - Email/password login
2. **SignUpActivity** - New user registration
3. **MainActivity** - Home screen with navigation cards
4. **UploadActivity** - Photo upload
5. **GalleryActivity** - View coloring projects
6. **ColoringActivity** - Interactive coloring canvas

---

## Build Configuration

### Gradle Setup
```gradle
// Kotlin: 1.9.20
// KSP: 1.9.20-1.0.14
// AGP: 8.2.2
// Gradle: 8.5
```

### Key Dependencies
```gradle
// Firebase
firebase-auth-ktx
firebase-bom:32.7.0

// UI
material:1.11.0
androidx.activity:activity-ktx:1.8.2

// DI
hilt-android:2.48
ksp:hilt-compiler:2.48

// Networking
retrofit:2.9.0
okhttp:4.12.0
```

---

## Firebase Integration

### google-services.json
Located: `android/app/google-services.json`

**Important:** Contains real Firebase credentials - don't commit to public repos!

### Authentication
```kotlin
// Initialize
private val auth = FirebaseAuth.getInstance()

// Sign up
auth.createUserWithEmailAndPassword(email, password)

// Login
auth.signInWithEmailAndPassword(email, password)

// Check auth state
auth.currentUser // null if not logged in
```

---

## Building

### Debug Build
```powershell
cd android
.\gradlew.bat assembleDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`

### Release Build
```powershell
.\gradlew.bat assembleRelease
```

### Clean Build
```powershell
.\gradlew.bat clean assembleDebug
```

---

## Running

### From Scripts
```powershell
# Check prerequisites
.\check-phone.ps1

# Build and run
.\check-and-run.ps1 -Build -Run

# Just run (if already built)
.\check-and-run.ps1 -Run
```

### From Android Studio
1. Open `android` folder
2. Wait for Gradle sync
3. Click green ▶ Run button
4. Select device
5. App launches

---

## Testing

### Manual Testing
1. Sign Up with new account
2. Login with credentials
3. Navigate home screen
4. Test upload flow
5. Test gallery
6. Logout and login again

### Device Requirements
- Android 7.0+ (API 24)
- USB Debugging enabled
- Connected via USB or WiFi

---

## Code Structure

```
app/src/main/
├── java/com/cloudgallery/portfolio/
│   ├── GalleryApplication.kt      # App entry point (Hilt)
│   ├── ui/
│   │   ├── MainActivity.kt        # Home screen
│   │   ├── LoginActivity.kt       # Login
│   │   ├── SignUpActivity.kt      # Registration
│   │   ├── UploadActivity.kt      # Upload
│   │   └── coloring/
│   │       └── ColoringActivity.kt
│   ├── data/
│   │   └── models/                # Data classes
│   └── network/
│       └── ApiService.kt          # Retrofit API
└── res/
    ├── layout/                    # XML layouts
    ├── values/                    # Strings, colors, themes
    └── drawable/                  # Icons, images
```

---

## Common Issues & Solutions

### Build Errors

**KAPT issues:**
- ✅ Fixed: Migrated to KSP

**XML malformed:**
- ✅ Fixed: All layouts validated

**Missing theme:**
- ✅ Fixed: themes.xml created

### Runtime Issues

**App crashes on launch:**
- Check Firebase configuration
- Verify google-services.json is present
- Check logcat for errors

**Can't login:**
- Account must be created via Sign Up first
- Check Firebase Console for registered users

**Google Sign-In fails:**
- Add SHA-1 fingerprint to Firebase
- Enable Google Sign-In in Firebase Console

---

## Development Workflow

### 1. Make Changes
Edit Kotlin files or layouts in Android Studio

### 2. Build
```powershell
.\gradlew.bat assembleDebug
```

### 3. Install
```powershell
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

### 4. Test
Launch app on device and test changes

### 5. Debug
```powershell
adb logcat | Select-String "cloudgallery"
```

---

## Scripts Reference

### check-and-run.ps1
```powershell
# Check prerequisites only
.\check-and-run.ps1

# Build and run
.\check-and-run.ps1 -Build -Run
```

### check-phone.ps1
```powershell
# Check device connection and details
.\check-phone.ps1
```

### check-firebase-auth.ps1
```powershell
# Check Firebase auth status and logs
.\check-firebase-auth.ps1
```

---

## Migrated from KAPT to KSP

### Why?
- KAPT had JDK 17 compatibility issues
- KSP is 2x faster
- KSP is officially recommended by Google

### What Changed?
```gradle
// Before
id 'kotlin-kapt'
kapt 'com.google.dagger:hilt-compiler:2.48'

// After
id 'com.google.devtools.ksp'
ksp 'com.google.dagger:hilt-compiler:2.48'
```

---

## Performance

### Build Times
- Clean build: ~30s
- Incremental build: ~10s
- KSP processing: ~5s

### APK Size
- Debug: ~8.3 MB
- Release: TBD (with minification)

---

## Next Steps

### To Do
- [ ] Connect to backend API
- [ ] Implement image upload
- [ ] Add coloring canvas
- [ ] Save progress to Firebase
- [ ] Add user profile
- [ ] Enable Google Sign-In

### Future Enhancements
- [ ] Offline mode (Room database)
- [ ] Share colored images
- [ ] Social features
- [ ] Dark mode
- [ ] Accessibility improvements

---

Last updated: January 7, 2026

