# Cloud Gallery Setup Progress

**Date:** December 20, 2025  
**Project:** Cloud Gallery Portfolio  
**GCP Project ID:** `image-gallery-481812`

---

## ✅ Completed Setup Tasks

### Phase 1: GCP Project Setup ✅
- [x] GCP Project created: `image-gallery-481812`
- [x] Billing enabled
- [x] gcloud CLI installed (v550.0.0)
- [x] Authenticated as: kylehaggarty@gmail.com
- [x] Docker Desktop installed (v24.0.6)
- [x] Terraform installed (v1.14.3)
- [x] Required GCP APIs enabled:
  - Cloud Run API
  - Cloud Storage API
  - Cloud SQL Admin API
  - Identity Toolkit API
  - Cloud Build API
  - Secret Manager API

### Phase 2: IAM & Service Accounts ✅
- [x] Created service account: `gallery-backend@image-gallery-481812.iam.gserviceaccount.com`
- [x] Granted `roles/firebase.admin` role
- [x] Granted `roles/storage.objectAdmin` role

### Phase 3: Cloud Storage ✅
- [x] Created bucket: `gs://image-gallery-481812-gallery-images`
- [x] Location: `us-central1`
- [x] Storage class: `STANDARD`
- [x] CORS configuration applied (allows web uploads)
- [x] Lifecycle policy applied (auto-delete pending images after 90 days)

### Phase 4: Local PostgreSQL ✅
- [x] PostgreSQL 15 installed via Homebrew
- [x] PostgreSQL service started
- [x] Database created: `gallery`
- [x] User created: `gallery_user` (password: dev_password_123)
- [x] Permissions granted

### Phase 5: Backend Configuration ✅
- [x] Created `backend/.env` with:
  - Local database URL
  - GCP project settings
  - Bucket name
  - Firebase credentials path
- [x] Updated `.gitignore` to exclude sensitive files

---

## 📋 Next Steps (Manual - Requires Browser)

### Phase 6: Firebase Setup (REQUIRED NEXT)
You need to complete this in the Firebase Console:

1. **Go to:** https://console.firebase.google.com/
2. **Click:** "Add Project"
3. **Select:** Existing project → "image-gallery-481812"
4. **Disable:** Google Analytics (not needed)
5. **Enable Authentication:**
   - Firebase Console → Build → Authentication → Get Started
   - Enable "Email/Password" provider
   - Enable "Google Sign-In" provider

6. **Add Web App:**
   - Project Settings → Your apps → Web (</> icon)
   - App nickname: "Cloud Gallery Web"
   - DON'T enable Firebase Hosting
   - Copy the Firebase config (you'll need this for `web/.env`)

7. **Add Android App:**
   - Project Settings → Your apps → Android
   - Package name: `com.cloudgallery.portfolio`
   - Download `google-services.json`
   - Place in `android/app/` directory

8. **Create Firebase Admin Service Account Key:**
   ```bash
   gcloud iam service-accounts keys create firebase-admin-key.json \
       --iam-account=gallery-backend@image-gallery-481812.iam.gserviceaccount.com
   ```
   This file will be used by the backend to verify user tokens.

---

## 💰 Current Monthly Cost Estimate

| Service | Status | Monthly Cost |
|---------|--------|-------------|
| Cloud Storage | Active | ~$0.04 |
| Cloud Run | Not deployed yet | $0 (free tier) |
| Firebase Auth | Configured | $0 (free tier) |
| PostgreSQL | Local | $0 (free) |
| **TOTAL** | | **~$0.04/month** |

---

## 🎯 What You've Learned So Far

### GCP Concepts Covered:
✅ **Project Structure** - Understanding projects as billing boundaries  
✅ **IAM** - Service accounts and role-based access control  
✅ **Cloud Storage** - Bucket creation, policies, CORS, lifecycle management  
✅ **gcloud CLI** - Managing GCP resources from command line  
✅ **Cost Optimization** - Using local resources where appropriate  

### Still To Learn:
⏳ Firebase Authentication integration  
⏳ Cloud Run serverless deployment  
⏳ Container building and deployment  
⏳ Cloud Run IAM policies  

---

## 📝 Important Information to Save

### Service Account
- **Email:** `gallery-backend@image-gallery-481812.iam.gserviceaccount.com`
- **Roles:** firebase.admin, storage.objectAdmin

### Cloud Storage
- **Bucket:** `gs://image-gallery-481812-gallery-images`
- **Region:** us-central1
- **CORS:** Enabled for web uploads
- **Lifecycle:** Auto-delete pending/* after 90 days

### PostgreSQL
- **Database:** gallery
- **User:** gallery_user
- **Password:** dev_password_123
- **Host:** localhost:5432
- **Connection String:** `postgresql://gallery_user:dev_password_123@localhost:5432/gallery`

### Files Created
- `cors.json` - CORS configuration for bucket
- `lifecycle.json` - Lifecycle policy for bucket
- `backend/.env` - Backend environment configuration
- Updated `.gitignore` - Prevents committing secrets

---

## 🚀 Ready for Development

Your local development environment is now configured! Once you complete the Firebase setup (Phase 6), you can:

1. Install backend dependencies
2. Initialize database schema
3. Test backend locally
4. Deploy to Cloud Run

---

## ⚠️ Security Reminders

- ✅ `.env` files are in `.gitignore`
- ✅ Service account keys will be in `.gitignore`
- ⚠️ **NEVER** commit `firebase-admin-key.json`
- ⚠️ **NEVER** commit `.env` files
- ⚠️ Change default passwords for production!

---

## 📚 Useful Commands Reference

```bash
# View GCP project info
gcloud config get-value project
gcloud projects describe image-gallery-481812

# View IAM policies
gcloud projects get-iam-policy image-gallery-481812

# View service accounts
gcloud iam service-accounts list

# View bucket info
gsutil ls -L gs://image-gallery-481812-gallery-images

# PostgreSQL commands
psql -U gallery_user -d gallery -h localhost
\l  # List databases
\du # List users
\q  # Quit

# Start/stop PostgreSQL
brew services start postgresql@15
brew services stop postgresql@15
```

---

**Status:** ✅ Phases 1-5 Complete | ⏳ Phase 6 (Firebase) Pending
