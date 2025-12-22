# Android App Setup Checklist

**Project:** Cloud Gallery Portfolio - Android App  
**Date:** December 20, 2025  
**Status:** Configuration Phase

---

## Prerequisites Check

Before starting, ensure you have:

- [ ] Android Studio installed (Hedgehog or later)
- [ ] JDK 17 installed
- [ ] Android SDK with API 34
- [ ] Firebase project configured (Phase 4 from main README)
- [ ] Backend API URL (will get from Cloud Run deployment)

---

## Phase 1: Firebase Configuration (DEPENDS ON MAIN PHASE 4)

**Note:** This requires Firebase to be set up first (main README Phase 4).

- [ ] **Get google-services.json from Firebase Console**
  - Go to Firebase Console → Project Settings
  - Select your Android app (package: `com.cloudgallery.portfolio`)
  - Download `google-services.json`
  - Save location: `android/app/google-services.json`

- [ ] **Verify Firebase Authentication is enabled**
  - Email/Password provider ✅
  - Google Sign-In provider ✅

- [ ] **Get SHA-1 Fingerprint for Google Sign-In**
  ```bash
  cd android
  ./gradlew signingReport
  # Copy SHA-1 from debug variant
  # Add to Firebase Console → Project Settings → Your apps → Android app
  ```

---

## Phase 2: Project Configuration

- [ ] **Open Project in Android Studio**
  ```bash
  # Open Android Studio
  # File → Open → Select /Users/heggs/Documents/git/cloud-gallery/android
  ```

- [ ] **Wait for Gradle Sync**
  - Let Android Studio download dependencies
  - Fix any Gradle version issues if prompted

- [ ] **Verify Build Configuration**
  ```bash
  cd /Users/heggs/Documents/git/cloud-gallery/android
  ./gradlew build --dry-run
  ```

---

## Phase 3: API Configuration

- [ ] **Update strings.xml with Backend URL**
  
  File: `android/app/src/main/res/values/strings.xml`
  
  Add:
  ```xml
  <string name="api_base_url">YOUR_BACKEND_URL</string>
  ```
  
  **Note:** Backend URL will come from Cloud Run deployment (Phase 7 in main README)
  - For now, can use placeholder: `http://10.0.2.2:8080` (local testing)
  - Update later with actual Cloud Run URL

- [ ] **Verify Package Name**
  
  Check `android/app/build.gradle`:
  ```gradle
  android {
      namespace 'com.cloudgallery.portfolio'
      // or
      applicationId "com.cloudgallery.portfolio"
  }
  ```

---

## Phase 4: Dependencies Check

- [ ] **Verify all dependencies are in build.gradle**
  
  Check `android/app/build.gradle` has:
  - Firebase Authentication
  - Firebase Storage
  - Retrofit for API calls
  - Coil for image loading
  - Hilt for dependency injection
  - Kotlin Coroutines
  - Material Design components

- [ ] **Run Gradle Sync**
  ```bash
  ./gradlew build
  ```

---

## Phase 5: Code Verification

- [ ] **Check existing source files**
  ```bash
  # List all Kotlin files
  find android/app/src -name "*.kt"
  ```

- [ ] **Verify main components exist:**
  - [ ] `GalleryApplication.kt`
  - [ ] `MainActivity.kt`
  - [ ] `ApiService.kt`
  - [ ] Data models
  - [ ] Repository classes

- [ ] **Review any TODOs or placeholders in code**

---

## Phase 6: Manifest Configuration

- [ ] **Verify AndroidManifest.xml has required permissions**
  
  Check for:
  ```xml
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.CAMERA" />
  <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
  ```

- [ ] **Verify Application class is registered**
  ```xml
  <application
      android:name=".GalleryApplication"
      ...>
  ```

---

## Phase 7: Build & Test

- [ ] **Clean Build**
  ```bash
  cd /Users/heggs/Documents/git/cloud-gallery/android
  ./gradlew clean
  ./gradlew build
  ```

- [ ] **Build Debug APK**
  ```bash
  ./gradlew assembleDebug
  ```
  
  Output location: `app/build/outputs/apk/debug/app-debug.apk`

- [ ] **Fix any build errors**

---

## Phase 8: Local Testing (Optional - Emulator)

- [ ] **Create Android Emulator (if needed)**
  - Open AVD Manager in Android Studio
  - Create device with API 34
  - Recommended: Pixel 6 with Play Store

- [ ] **Run app on emulator**
  ```bash
  ./gradlew installDebug
  # Or use Run button in Android Studio
  ```

- [ ] **Test app opens without crashing**

---

## Phase 9: Integration Testing (After Backend Deployed)

**Prerequisites:** Backend must be deployed to Cloud Run

- [ ] **Update API URL in strings.xml**
  - Replace placeholder with actual Cloud Run URL
  - Format: `https://gallery-backend-xxx.run.app`

- [ ] **Rebuild app**
  ```bash
  ./gradlew clean assembleDebug
  ```

- [ ] **Test Firebase Authentication**
  - [ ] Email/Password sign up
  - [ ] Email/Password login
  - [ ] Google Sign-In
  - [ ] Logout

- [ ] **Test Image Upload Flow**
  - [ ] Select image from gallery
  - [ ] Add title and description
  - [ ] Upload to backend
  - [ ] Verify appears in backend/database

- [ ] **Test Upload List**
  - [ ] View uploaded images
  - [ ] See approval status
  - [ ] Refresh list

---

## Phase 10: Physical Device Testing (Optional)

- [ ] **Enable Developer Mode on Android device**
  - Settings → About Phone → Tap Build Number 7 times
  - Settings → Developer Options → Enable USB Debugging

- [ ] **Connect device via USB**
  ```bash
  adb devices
  # Should show your device
  ```

- [ ] **Install on device**
  ```bash
  ./gradlew installDebug
  ```

- [ ] **Test all features on real device**

---

## Phase 11: Code Cleanup & Polish

- [ ] **Remove unused imports**
- [ ] **Fix lint warnings**
  ```bash
  ./gradlew lint
  ```
- [ ] **Format code**
  - Android Studio → Code → Reformat Code
- [ ] **Update comments and documentation**
- [ ] **Remove debug logs for production**

---

## Common Issues & Solutions

### Issue: google-services.json not found
**Solution:** Download from Firebase Console and place in `android/app/`

### Issue: SHA-1 fingerprint mismatch
**Solution:** Run `./gradlew signingReport` and add SHA-1 to Firebase

### Issue: API connection fails
**Solution:** 
- Check backend URL in strings.xml
- Verify backend is running
- Check network permissions in manifest
- For emulator, use `10.0.2.2` instead of `localhost`

### Issue: Build fails with dependency errors
**Solution:**
- Update Gradle: `./gradlew wrapper --gradle-version=8.5`
- Sync project: Android Studio → File → Sync Project
- Clean build: `./gradlew clean build`

### Issue: App crashes on launch
**Solution:**
- Check logcat in Android Studio
- Verify google-services.json is present
- Check Application class is registered in manifest

---

## Current Status Summary

**What We Need Before Starting:**
1. ✅ Android app code exists (basic structure)
2. ⏳ Firebase project setup (main README Phase 4)
3. ⏳ `google-services.json` file
4. ⏳ Backend API deployed (for API URL)

**Immediate Next Steps:**
1. Complete Firebase setup (main README Phase 4)
2. Download `google-services.json`
3. Open project in Android Studio
4. Build and verify compilation

**Can Do Now (Without Backend):**
- Review existing code
- Check dependencies
- Verify project structure
- Build debug APK
- Test app opens (auth will fail until Firebase configured)

---

## Timeline Estimate

- **Phase 1-2** (Firebase + Project Setup): 30 minutes
- **Phase 3-4** (Configuration + Dependencies): 15 minutes
- **Phase 5-6** (Code Review + Manifest): 15 minutes
- **Phase 7-8** (Build + Local Test): 30 minutes
- **Phase 9** (Integration Testing): 1 hour (after backend ready)
- **Phase 10-11** (Device Test + Polish): 1 hour

**Total: 3-4 hours** (excluding backend deployment time)

---

## Dependencies

**Blocked By:**
- Firebase project setup (main README Phase 4)
- Backend deployment (main README Phase 7)

**Blocks:**
- End-to-end testing
- Production deployment

---

**Ready to start?** Complete Firebase setup first, then come back to Phase 1!
