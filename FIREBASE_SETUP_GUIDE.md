# Firebase Setup Guide - Phase 4

**Date:** December 20, 2025  
**Project:** image-gallery-481812  
**Duration:** 15-20 minutes

---

## 📋 Prerequisites

✅ GCP project created: `image-gallery-481812`  
✅ Billing enabled  
✅ Identity Platform API enabled

---

## 🎯 What We're Setting Up

Firebase will provide:
- 🔐 **Authentication** - Email/password and Google Sign-In
- 📱 **Android SDK** - Mobile app authentication
- 🌐 **Web SDK** - Web app authentication
- 🔑 **Admin SDK** - Backend authentication verification

---

## 🚀 Step-by-Step Instructions

### Step 1: Create Firebase Project (5 minutes)

1. **Open Firebase Console**
   - Go to: https://console.firebase.google.com/
   - Sign in with your Google account

2. **Add Project**
   - Click "Add project" or "Create a project"
   - **Important:** Select "**Enter a project name or select an existing Google Cloud project**"
   - Search for and select: `image-gallery-481812`
   - Click "Continue"

3. **Confirm Firebase billing plan**
   - Select "Continue" (uses your existing GCP billing)

4. **Google Analytics (Optional)**
   - Toggle OFF if you don't need analytics
   - Click "Add Firebase"
   - Wait 30-60 seconds for project creation

5. **Verify**
   - You should see "Your new project is ready"
   - Click "Continue" to go to project console

---

### Step 2: Enable Authentication (3 minutes)

1. **Navigate to Authentication**
   - In left sidebar: Click "Build" → "Authentication"
   - Click "Get started" button

2. **Enable Email/Password**
   - Click "Email/Password" from the list
   - Toggle "Email/Password" to **Enabled**
   - Leave "Email link" disabled
   - Click "Save"

3. **Enable Google Sign-In**
   - Click "Add new provider" button
   - Select "Google"
   - Toggle to **Enabled**
   - **Project support email:** Select your email from dropdown
   - Click "Save"

4. **Verify**
   - You should see both providers listed as "Enabled"

---

### Step 3: Add Web App (5 minutes)

1. **Register Web App**
   - Click the gear icon ⚙️ next to "Project Overview"
   - Click "Project settings"
   - Scroll down to "Your apps" section
   - Click the **Web icon** `</>`
   - App nickname: `Cloud Gallery Web`
   - ✅ Check "Also set up Firebase Hosting for this app"
   - Click "Register app"

2. **Copy Configuration**
   - You'll see a code snippet like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIza...",
     authDomain: "image-gallery-481812.firebaseapp.com",
     projectId: "image-gallery-481812",
     storageBucket: "image-gallery-481812.firebasestorage.app",
     messagingSenderId: "123456789",
     appId: "1:123456789:web:abcdef123456"
   };
   ```

3. **Save This Configuration**
   - **Copy the entire config object** (we'll use it in Step 6)
   - Click "Continue to console"

---

### Step 4: Add Android App (4 minutes)

1. **Register Android App**
   - Still in "Project settings"
   - Scroll to "Your apps" section
   - Click the **Android icon** (robot)
   - **Android package name:** `com.cloudgallery.portfolio`
   - **App nickname (optional):** `Cloud Gallery Android`
   - **Debug signing certificate SHA-1:** Leave blank for now (we'll add later)
   - Click "Register app"

2. **Download google-services.json**
   - Click "Download google-services.json" button
   - **IMPORTANT:** Save it to your Downloads folder
   - Click "Next" → "Next" → "Continue to console"

3. **Move the File (DO THIS NOW)**
   - Open Terminal and run:
   ```bash
   # Replace ~/Downloads/ with your actual download location
   mv ~/Downloads/google-services.json /Users/heggs/Documents/git/cloud-gallery/android/app/
   ```
   - Or manually drag the file to: `cloud-gallery/android/app/`

4. **Verify**
   ```bash
   ls -la /Users/heggs/Documents/git/cloud-gallery/android/app/google-services.json
   ```
   - You should see the file listed

---

### Step 5: Generate Android SHA-1 Certificate (2 minutes)

1. **Generate Debug Certificate**
   - In Terminal, navigate to android directory:
   ```bash
   cd /Users/heggs/Documents/git/cloud-gallery/android
   ./gradlew signingReport
   ```

2. **Copy SHA-1 Fingerprint**
   - Look for output like:
   ```
   Variant: debug
   SHA1: AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD
   ```
   - Copy the SHA-1 value (the long hex string)

3. **Add to Firebase Console**
   - Back in Firebase Console → Project Settings
   - Scroll to "Your apps" → find "Cloud Gallery Android"
   - Click "Add fingerprint"
   - Paste the SHA-1 value
   - Click "Save"

---

### Step 6: Generate Firebase Admin SDK Key (2 minutes)

1. **Navigate to Service Accounts**
   - Firebase Console → Project Settings (gear icon)
   - Click "Service accounts" tab at top

2. **Generate Key**
   - You should see "Firebase Admin SDK" section
   - Click "Generate new private key" button
   - Confirm "Generate key" in popup
   - A JSON file will download (like `image-gallery-481812-firebase-adminsdk-xxxxx.json`)

3. **Rename and Move the File**
   ```bash
   # Replace the filename with your actual downloaded file
   mv ~/Downloads/image-gallery-481812-firebase-adminsdk-*.json /Users/heggs/Documents/git/cloud-gallery/backend/firebase-admin-key.json
   ```

4. **Verify**
   ```bash
   ls -la /Users/heggs/Documents/git/cloud-gallery/backend/firebase-admin-key.json
   ```

---

### Step 7: Configure Web Environment (1 minute)

1. **Update web/.env File**
   - Open or create: `web/.env`
   - Add the Firebase config from Step 3:
   ```bash
   # I'll help you do this automatically
   ```

---

### Step 8: Update .gitignore (1 minute)

```bash
# I'll handle this automatically
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] Firebase project linked to `image-gallery-481812`
- [ ] Email/Password authentication enabled
- [ ] Google Sign-In authentication enabled
- [ ] Web app registered with nickname "Cloud Gallery Web"
- [ ] Android app registered with package name "com.cloudgallery.portfolio"
- [ ] File exists: `android/app/google-services.json`
- [ ] File exists: `backend/firebase-admin-key.json`
- [ ] File updated: `web/.env` with Firebase config
- [ ] SHA-1 fingerprint added to Android app in Firebase Console
- [ ] Both JSON files added to .gitignore

---

## 🎬 After This Setup

Once Firebase is configured, you can:

1. ✅ Build the Android app (no more google-services.json error)
2. ✅ Deploy the backend to Cloud Run (with Firebase auth)
3. ✅ Deploy the web frontend (with Firebase auth)
4. ✅ Test authentication across all platforms

---

## 🆘 Troubleshooting

### "Can't find existing GCP project"
- Make sure you're signed in with the correct Google account
- Check project ID is exactly: `image-gallery-481812`
- Verify billing is enabled in GCP Console

### "google-services.json not found"
- Check Downloads folder
- File should be named exactly `google-services.json`
- Must be placed in `android/app/` directory

### "SHA-1 command fails"
- Need Android Studio or JDK installed
- Use: `cd android && ./gradlew signingReport`
- If no gradlew: `gradle signingReport`

### "Firebase Admin key download fails"
- Disable popup blocker
- Try different browser
- Check Downloads folder permissions

---

## 📝 Next Steps After Firebase Setup

Once you complete this phase:

1. **Phase 7: Backend Development**
   - Install Python dependencies
   - Initialize database schema
   - Test Firebase authentication
   - Deploy to Cloud Run

2. **Phase 8: Web Development**
   - Configure Firebase SDK
   - Test authentication locally
   - Deploy to Firebase Hosting

3. **Phase 9: Android App**
   - Configure backend API URL
   - Build APK
   - Test authentication and image upload

---

## 🎯 Start Now

**Ready to begin?**

Open this URL in your browser:  
**https://console.firebase.google.com/**

Follow Steps 1-6 above, then let me know when you're done!

I'll handle Step 7 (web/.env) and Step 8 (.gitignore) automatically once you've downloaded the files.
