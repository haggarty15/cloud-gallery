# Firebase Authentication Guide

## Overview

Cloud Gallery uses Firebase Authentication for secure user management.

**Project:** image-gallery-481812  
**Console:** https://console.firebase.google.com/project/image-gallery-481812

---

## Enabled Methods

### ✅ Email/Password
**Status:** Working  
**Users can:** Sign up, login, reset password

### ⚠️ Google Sign-In
**Status:** Requires SHA-1 setup  
**Your SHA-1:** `D2:01:02:97:A2:53:37:1F:99:F1:9A:F9:A9:F0:3E:EF:E0:91:9B:A1`

---

## Email/Password Authentication

### Sign Up
```kotlin
auth.createUserWithEmailAndPassword(email, password)
    .addOnCompleteListener { task ->
        if (task.isSuccessful) {
            // Account created, user logged in
        } else {
            // Show error
        }
    }
```

**Requirements:**
- Valid email format
- Password min 6 characters
- Unique email (not already registered)

### Login
```kotlin
auth.signInWithEmailAndPassword(email, password)
    .addOnCompleteListener { task ->
        if (task.isSuccessful) {
            // User logged in
        } else {
            // Invalid credentials
        }
    }
```

### Logout
```kotlin
auth.signOut()
// User logged out
```

---

## Google Sign-In Setup

### Step 1: Add SHA-1 to Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/project/image-gallery-481812)
2. Click ⚙️ Settings → Project settings
3. Find Android app: `com.cloudgallery.portfolio`
4. Scroll to **SHA certificate fingerprints**
5. Click **Add fingerprint**
6. Paste: `D2:01:02:97:A2:53:37:1F:99:F1:9A:F9:A9:F0:3E:EF:E0:91:9B:A1`
7. Click **Save**

### Step 2: Enable Google Sign-In

1. Firebase Console → Authentication
2. Sign-in method tab
3. Click **Google**
4. Toggle **Enable**
5. Select support email
6. Click **Save**

### Step 3: Download google-services.json

1. Project settings → Your apps
2. Click **Download google-services.json**
3. Replace `android/app/google-services.json`
4. Rebuild app

---

## Where Data is Stored

### ❌ NOT Stored Locally
- User passwords
- User accounts
- Authentication tokens (long-term)

### ✅ Stored in Firebase Cloud
- User accounts (email, UID)
- Encrypted passwords
- User metadata

### ✅ Stored Locally (Temporary)
- Session tokens (auto-expire)
- Current user state

---

## User Management

### Check Current User
```kotlin
val user = auth.currentUser
if (user != null) {
    // User is logged in
    val email = user.email
    val uid = user.uid
} else {
    // Not logged in
}
```

### Get User Info
```kotlin
val user = auth.currentUser
user?.let {
    val email = it.email
    val uid = it.uid
    val isEmailVerified = it.isEmailVerified
}
```

---

## Error Handling

### Common Errors

**ERROR_INVALID_EMAIL**
- Email format is wrong
- Solution: Validate email pattern

**ERROR_WEAK_PASSWORD**
- Password less than 6 characters
- Solution: Enforce minimum length

**ERROR_EMAIL_ALREADY_IN_USE**
- Account already exists
- Solution: Show "Login instead?" link

**ERROR_USER_NOT_FOUND**
- No account with that email
- Solution: Show "Sign up" link

**ERROR_WRONG_PASSWORD**
- Incorrect password
- Solution: Show error, offer reset

**ERROR_INVALID_CREDENTIAL (Google)**
- OAuth configuration issue
- Solution: Add SHA-1 to Firebase

---

## Security Best Practices

### ✅ Implemented
- Passwords never stored locally
- Firebase handles encryption
- Session tokens auto-expire
- HTTPS communication

### 🔒 Recommended
- [ ] Email verification
- [ ] Password reset flow
- [ ] Multi-factor authentication
- [ ] Account deletion

---

## Testing

### Create Test Account
```
1. Open app
2. Tap "Sign Up"
3. Email: test@example.com
4. Password: test123456
5. Confirm: test123456
6. Tap "Sign Up"
```

### Verify in Firebase
1. Go to Firebase Console
2. Authentication → Users tab
3. Should see `test@example.com` listed

### Test Login
```
1. Logout
2. Enter: test@example.com
3. Password: test123456
4. Tap "Login"
```

---

## Firebase Console Quick Links

- **Users:** https://console.firebase.google.com/project/image-gallery-481812/authentication/users
- **Sign-in methods:** https://console.firebase.google.com/project/image-gallery-481812/authentication/providers
- **Settings:** https://console.firebase.google.com/project/image-gallery-481812/settings/general

---

## Troubleshooting

### "Auth credential is incorrect"
**Cause:** No account exists  
**Solution:** Use Sign Up first

### "Google Sign-In failed :10"
**Cause:** SHA-1 not added to Firebase  
**Solution:** Add SHA-1 (see Google Sign-In Setup)

### "Network error"
**Cause:** No internet connection  
**Solution:** Check device connectivity

---

## Get Your SHA-1 Fingerprint

```powershell
& "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" -list -v -keystore "$env:USERPROFILE\.android\debug.keystore" -alias androiddebugkey -storepass android -keypass android | Select-String "SHA1"
```

Output:
```
SHA1: D2:01:02:97:A2:53:37:1F:99:F1:9A:F9:A9:F0:3E:EF:E0:91:9B:A1
```

---

Last updated: January 7, 2026

