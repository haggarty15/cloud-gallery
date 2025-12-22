# Firebase Setup - Quick Reference

**Start Here:** https://console.firebase.google.com/

---

## 🎯 Quick Checklist

### In Firebase Console (Browser)

- [ ] **1. Link Firebase to GCP**
  - Add project → Select `image-gallery-481812`
  
- [ ] **2. Enable Authentication**
  - Build → Authentication → Get Started
  - Enable: Email/Password ✅
  - Enable: Google Sign-In ✅

- [ ] **3. Add Web App**
  - Project Settings → Your apps → Web icon
  - Nickname: `Cloud Gallery Web`
  - ✅ Enable Firebase Hosting
  - **COPY the config object!**

- [ ] **4. Add Android App**
  - Project Settings → Your apps → Android icon  
  - Package: `com.cloudgallery.portfolio`
  - **DOWNLOAD google-services.json**

- [ ] **5. Generate Admin Key**
  - Project Settings → Service Accounts
  - Generate new private key
  - **DOWNLOAD the JSON file**

### After Downloads

- [ ] **6. Run Helper Script**
  ```bash
  cd /Users/heggs/Documents/git/cloud-gallery
  ./setup-firebase-files.sh
  ```

- [ ] **7. Update web/.env**
  - Open `web/.env`
  - Paste Firebase config values from step 3

- [ ] **8. Generate SHA-1 (Android)**
  ```bash
  cd android
  ./gradlew signingReport
  ```
  - Copy SHA-1 fingerprint
  - Add to Firebase Console (Android app settings)

---

## 📋 Files You Should Have

After setup:

```
✓ android/app/google-services.json
✓ backend/firebase-admin-key.json  
✓ web/.env (with Firebase config filled in)
```

---

## 🔒 Security

These files contain secrets and are already in `.gitignore`:
- ❌ DO NOT commit `google-services.json`
- ❌ DO NOT commit `firebase-admin-key.json`
- ❌ DO NOT commit `web/.env`

---

## ⏱️ Time Estimate

- Firebase Console steps: ~12 minutes
- File setup: ~3 minutes
- SHA-1 generation: ~2 minutes
- **Total: ~17 minutes**

---

## 🆘 Need Help?

See detailed guide: `FIREBASE_SETUP_GUIDE.md`

---

## ✅ Done?

After completing all steps, tell me and I'll verify the setup!
