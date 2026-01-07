# 🎨 Digital Coloring App - Setup Guide

**Project:** Paint-by-Numbers Coloring App (Like Zen Color)  
**Tech Stack:** React + Flask + GCP + Firebase + PostgreSQL  
**GCP Project ID:** `image-gallery-481812`

---

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 18+** and npm
- **Git** installed
- **Google Cloud account** with billing enabled
- **PostgreSQL** (for local development)

---

## 🚀 Quick Setup (Windows)

### Step 1: Install GCP Tools

```powershell
# Install gcloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# Verify installation
gcloud --version

# Login to GCP
gcloud auth login

# Set project
gcloud config set project image-gallery-481812
```

### Step 2: Get GCP Service Account Key

```powershell
# Create directory for credentials
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gcp"

# Create service account key (for Firebase Admin SDK)
gcloud iam service-accounts keys create "$env:USERPROFILE\.gcp\firebase-admin-key.json" --iam-account=gallery-backend@image-gallery-481812.iam.gserviceaccount.com

# Verify key was created
Get-Content "$env:USERPROFILE\.gcp\firebase-admin-key.json" | Select-Object -First 5
```

### Step 3: Setup Firebase (Browser Required)

1. **Go to Firebase Console:** https://console.firebase.google.com/
2. **Add Project:**
   - Click "Add Project"
   - Select existing project: `image-gallery-481812`
   - Disable Google Analytics (optional)
   
3. **Enable Authentication:**
   - Go to: Build → Authentication → Get Started
   - Enable: Email/Password provider
   - Enable: Google Sign-In provider

4. **Add Web App:**
   - Project Settings → Your apps → Web icon `</>`
   - App nickname: `Digital Coloring Web`
   - Click "Register app"
   - **COPY the config** (you'll need this next)

5. **Add Android App (optional):**
   - Project Settings → Your apps → Android icon
   - Package name: `com.cloudgallery.portfolio`
   - Download `google-services.json` → Save to `android/app/`

### Step 4: Configure Backend

```powershell
# Navigate to backend
cd backend

# Create .env file
@"
# GCP Configuration
PROJECT_ID=image-gallery-481812
BUCKET_NAME=image-gallery-481812-gallery-images

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://gallery_user:dev_password_123@localhost/gallery

# Firebase Admin SDK
FIREBASE_CREDENTIALS=$env:USERPROFILE\.gcp\firebase-admin-key.json

# Server
PORT=8080
FLASK_ENV=development
"@ | Out-File -FilePath .env -Encoding utf8

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test canvas processor
python app/canvas_processor.py ../test-photos/sample.jpg 20
```

### Step 5: Configure Frontend

```powershell
cd ../web

# Create .env file with Firebase config from Step 3
@"
# Backend API
VITE_API_URL=http://localhost:8080

# Firebase Configuration (from Step 3 - Firebase Console)
VITE_FIREBASE_API_KEY=YOUR_API_KEY_HERE
VITE_FIREBASE_AUTH_DOMAIN=image-gallery-481812.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=image-gallery-481812
VITE_FIREBASE_STORAGE_BUCKET=image-gallery-481812.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=YOUR_SENDER_ID_HERE
VITE_FIREBASE_APP_ID=YOUR_APP_ID_HERE
"@ | Out-File -FilePath .env -Encoding utf8

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Step 6: Setup Local PostgreSQL

```powershell
# Install PostgreSQL (using Chocolatey)
choco install postgresql

# Or download from: https://www.postgresql.org/download/windows/

# Create database and user
psql -U postgres -c "CREATE DATABASE gallery;"
psql -U postgres -c "CREATE USER gallery_user WITH PASSWORD 'dev_password_123';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE gallery TO gallery_user;"

# Verify connection
psql -U gallery_user -d gallery -c "SELECT version();"
```

---

## ✅ Verification Steps

### Test Backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app/canvas_processor.py test-photos/sample.jpg 20

# Should create:
# - output/sample_canvas.json
# - output/sample_template.png
# - output/sample_colored.png
```

### Test Frontend
```powershell
cd web
npm run dev

# Open browser: http://localhost:5173
# Should see: Login page
```

---

## 🔑 GCP Credentials Summary

You'll need these credentials:

1. **Service Account Key** (`firebase-admin-key.json`)
   - Location: `%USERPROFILE%\.gcp\firebase-admin-key.json`
   - Used by: Backend (Flask) for Firebase Admin SDK
   - Permissions: firebase.admin, storage.objectAdmin

2. **Firebase Web Config** (from Firebase Console)
   - Used by: Frontend (React) for client-side auth
   - Stored in: `web/.env`

3. **GCP Project ID:** `image-gallery-481812`

4. **Cloud Storage Bucket:** `gs://image-gallery-481812-gallery-images`

---

## 📂 Project Structure

```
cloud-gallery/
├── backend/               # Flask API + Image Processing
│   ├── app/
│   │   ├── canvas_processor.py    # Core: Photo → Interactive regions
│   │   ├── routes.py              # API endpoints
│   │   └── models.py              # Database models
│   ├── .env                       # Backend config (create this)
│   └── requirements.txt
│
├── web/                   # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ColoringCanvas.jsx  # TODO: Build this!
│   │   └── services/
│   ├── .env                       # Frontend config (create this)
│   └── package.json
│
├── android/              # Android App (Kotlin)
│   └── app/
│       └── google-services.json   # Firebase config (download from console)
│
├── DIGITAL_COLORING_VISION.md    # 📖 Read this first!
├── PAINT_BY_NUMBERS_PLAN.md      # Architecture plan
└── CURRENT_STATUS.md             # What's done, what's next
```

---

## 🎯 Next Steps After Setup

1. **Test the canvas generator** with your own photos
2. **Build API endpoints** for:
   - Upload & process images
   - Save/load coloring sessions
   - Export finished artwork
3. **Create ColoringCanvas.jsx** - Interactive coloring component
4. **Deploy to Cloud Run** (when ready)

---

## 💰 Current Costs

| Service | Status | Monthly Cost |
|---------|--------|-------------|
| Cloud Storage | Active | ~$0.04 |
| Cloud Run | Not deployed yet | $0 (free tier) |
| Firebase Auth | Configured | $0 (free tier) |
| PostgreSQL | Local | $0 (free) |
| **TOTAL** | | **~$0.04/month** |

---

## 🆘 Troubleshooting

### "gcloud: command not found"
- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
- Restart terminal after installation

### "Permission denied" for service account key
```powershell
gcloud projects add-iam-policy-binding image-gallery-481812 `
  --member="serviceAccount:gallery-backend@image-gallery-481812.iam.gserviceaccount.com" `
  --role="roles/firebase.admin"
```

### PostgreSQL connection errors
- Verify PostgreSQL is running: `Get-Service postgresql*`
- Check credentials in `backend/.env`
- Test connection: `psql -U gallery_user -d gallery`

### Firebase config missing
- Complete Step 3 (Firebase Console setup)
- Copy the exact config from Firebase Console to `web/.env`

---

## 📚 Additional Resources

- **GCP Documentation:** https://cloud.google.com/docs
- **Firebase Docs:** https://firebase.google.com/docs
- **Flask Docs:** https://flask.palletsprojects.com/
- **React Docs:** https://react.dev/

---

**Ready to build?** Start with [DIGITAL_COLORING_VISION.md](DIGITAL_COLORING_VISION.md) to understand the product vision!
