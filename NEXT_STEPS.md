# 🎯 Next Steps - GCP & Firebase Setup

## ✅ What's Done

- ✅ Project analyzed and cleaned up
- ✅ Redundant docs removed
- ✅ Python environment created and working
- ✅ Canvas processor tested successfully
- ✅ Generated sample coloring template from boba.jpg (15 colors, 32,525 regions)

## 🔧 What You Need To Do Now

### 1. Check GCloud Authentication Status

```powershell
gcloud auth list
gcloud config list project
```

Expected output should show:
- Your email (kylehaggarty@gmail.com) as active
- Project: image-gallery-481812

If not authenticated:
```powershell
gcloud auth login
gcloud config set project image-gallery-481812
```

### 2. Create Firebase Admin Service Account Key

This key allows your backend to verify user authentication tokens.

```powershell
# Create directory for credentials
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gcp"

# Generate the service account key
gcloud iam service-accounts keys create "$env:USERPROFILE\.gcp\firebase-admin-key.json" `
  --iam-account=gallery-backend@image-gallery-481812.iam.gserviceaccount.com

# Verify it was created
Test-Path "$env:USERPROFILE\.gcp\firebase-admin-key.json"
```

Should return: `True`

### 3. Setup Firebase in Browser

**Go to:** https://console.firebase.google.com/

**Steps:**

1. **Add/Select Project**
   - Click "Add Project" (or select if already exists)
   - Select existing project: `image-gallery-481812`
   - Disable Google Analytics (optional - not needed for this app)
   - Click "Continue"

2. **Enable Authentication**
   - Left sidebar: Build → Authentication
   - Click "Get Started"
   - Enable providers:
     - ✅ Email/Password
     - ✅ Google Sign-In (click, enable, save)

3. **Add Web App**
   - Go to: Project Settings (gear icon) → Your apps
   - Click the Web icon `</>`
   - App nickname: `Digital Coloring Web`
   - **DON'T** enable Firebase Hosting
   - Click "Register app"
   
4. **COPY Firebase Config** ⚠️ IMPORTANT

   You'll see something like:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "image-gallery-481812.firebaseapp.com",
     projectId: "image-gallery-481812",
     storageBucket: "image-gallery-481812.firebasestorage.app",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef123456"
   };
   ```

   **Copy these values** - you'll need them for the next step!

### 4. Update web/.env with Firebase Config

Open `web\.env` in VS Code and update these lines:

```env
VITE_FIREBASE_API_KEY=<paste apiKey here>
VITE_FIREBASE_MESSAGING_SENDER_ID=<paste messagingSenderId here>
VITE_FIREBASE_APP_ID=<paste appId here>
```

The other values should already be correct:
- `VITE_FIREBASE_AUTH_DOMAIN=image-gallery-481812.firebaseapp.com`
- `VITE_FIREBASE_PROJECT_ID=image-gallery-481812`
- `VITE_FIREBASE_STORAGE_BUCKET=image-gallery-481812.firebasestorage.app`

### 5. (Optional) Setup PostgreSQL

If you want to test the full app (not just canvas generator):

#### Option A: Use Docker (Recommended - Easier)
```powershell
docker run --name gallery-postgres -e POSTGRES_PASSWORD=dev_password_123 -e POSTGRES_USER=gallery_user -e POSTGRES_DB=gallery -p 5432:5432 -d postgres:15
```

#### Option B: Install PostgreSQL
Download from: https://www.postgresql.org/download/windows/

Then create database:
```powershell
# Using psql
psql -U postgres -c "CREATE DATABASE gallery;"
psql -U postgres -c "CREATE USER gallery_user WITH PASSWORD 'dev_password_123';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE gallery TO gallery_user;"
```

---

## 📊 Current Setup Status

| Component | Status | Notes |
|-----------|--------|-------|
| GCP Project | ✅ Exists | `image-gallery-481812` |
| Cloud Storage Bucket | ✅ Active | `gs://image-gallery-481812-gallery-images` |
| Service Account | ✅ Created | `gallery-backend@...` |
| **Service Account Key** | ⏳ **DO THIS** | Need to create firebase-admin-key.json |
| **Firebase Auth** | ⏳ **DO THIS** | Enable in console |
| **Firebase Web Config** | ⏳ **DO THIS** | Copy to web/.env |
| Python Backend | ✅ Working | Canvas processor tested! |
| Frontend (React) | ⚠️ Not tested | Need Firebase config first |
| PostgreSQL | ⏳ Optional | Only needed for full app |

---

## 🎨 What You Can Do Right Now

Even without Firebase/DB setup, you can **test the canvas generator**:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Process any image with different difficulty levels
python app/canvas_processor.py ../test-photos/boba.jpg 10   # Easy
python app/canvas_processor.py ../test-photos/boba.jpg 20   # Medium
python app/canvas_processor.py ../test-photos/boba.jpg 40   # Hard

# Process your own photos
python app/canvas_processor.py C:\path\to\your\photo.jpg 20

# Check the output folder for results
explorer output
```

You'll see:
- **canvas.json** - Data for the interactive canvas (regions, colors)
- **template.png** - Preview with numbered regions
- **colored.png** - Target result
- **comparison.png** - Before/after side-by-side

---

## 🚀 After Setup is Complete

Once you have Firebase configured and (optionally) PostgreSQL running:

1. **Test Frontend**
   ```powershell
   cd web
   npm install
   npm run dev
   ```
   Visit: http://localhost:5173

2. **Test Backend API**
   ```powershell
   cd backend
   .\.venv\Scripts\Activate.ps1
   flask run
   ```
   Visit: http://localhost:8080

3. **Build the ColoringCanvas Component**
   - This is the next major development task
   - Interactive SVG canvas for tap-to-fill coloring

---

## 💡 Quick Reference

**Key Files:**
- `backend/.env` - Backend config (already set up)
- `web/.env` - Frontend config (needs Firebase values)
- `SETUP.md` - Complete setup guide
- `DIGITAL_COLORING_VISION.md` - Product vision
- `README.md` - Updated project overview

**GCP Resources:**
- Project ID: `image-gallery-481812`
- Bucket: `image-gallery-481812-gallery-images`
- Service Account: `gallery-backend@image-gallery-481812.iam.gserviceaccount.com`

**Commands:**
- Activate venv: `.\.venv\Scripts\Activate.ps1`
- Test canvas: `python app/canvas_processor.py <image> <colors>`
- Run backend: `flask run`
- Run frontend: `npm run dev`

---

**Questions?** Check [SETUP.md](SETUP.md) or ask!
