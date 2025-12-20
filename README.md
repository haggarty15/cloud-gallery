# Cloud Gallery Portfolio

A full-stack image gallery system deployed on Google Cloud Platform (GCP) featuring:
- **Android mobile app** for authenticated image uploads
- **Backend API** for image validation and approval workflow
- **Public web gallery** for displaying approved images
- **GCP Infrastructure** using Cloud Run, Cloud Storage, Cloud SQL, and Identity Platform

## Architecture Overview

```
┌─────────────────┐
│  Android App    │──────┐
│  (Kotlin)       │      │
└─────────────────┘      │
                         │ Firebase Auth
                         ▼
                  ┌──────────────┐
                  │  Backend API │
                  │  (Flask)     │
                  │  Cloud Run   │
                  └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Cloud Storage │ │  Cloud SQL   │ │   Identity   │
│  (Images)    │ │  (Metadata)  │ │   Platform   │
└──────────────┘ └──────────────┘ └──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Web Gallery │
                  │   (React)    │
                  │  Cloud Run   │
                  └──────────────┘
```

## Project Structure

```
cloud-gallery-portfolio/
├── android/                    # Android mobile app
│   ├── app/
│   ├── build.gradle
│   └── README.md
├── backend/                    # Python Flask API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── storage.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── web/                        # React web gallery
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── infrastructure/             # GCP deployment configs
│   ├── terraform/
│   └── README.md
└── docs/                       # Additional documentation
    ├── DEPLOYMENT.md
    ├── API.md
    └── SECURITY.md
```

## Features

### Android App
- Firebase Authentication (Email/Password, Google Sign-In)
- Camera and gallery image picker
- Image upload with progress tracking
- View upload history and status

### Backend API
- User authentication and authorization
- Image upload endpoint with validation (size, format)
- Automatic image storage in Cloud Storage
- Metadata storage in Cloud SQL
- Admin approval workflow
- Public API for approved images

### Web Gallery
- Public gallery view with responsive grid
- Image detail modal
- Admin dashboard for approval workflow
- Firebase Authentication for admin access

## GCP Services Used

1. **Cloud Run**: Containerized backend API and web hosting
2. **Cloud Storage**: Image blob storage with signed URLs
3. **Cloud SQL**: PostgreSQL for image metadata and approval status
4. **Identity Platform**: Firebase Authentication
5. **IAM**: Role-based access control
6. **Cloud Build**: CI/CD for container builds

## Getting Started

### Prerequisites
- Google Cloud Platform account
- Android Studio (for mobile app)
- Node.js 18+ (for web app)
- Python 3.11+ (for backend)
- Docker (for containerization)
- gcloud CLI

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/haggarty15/cloud-gallery.git
cd cloud-gallery
```

2. **Setup GCP Infrastructure**
```bash
cd infrastructure
# Follow infrastructure/README.md for setup
```

3. **Deploy Backend**
```bash
cd backend
# Follow backend/README.md for deployment
```

4. **Deploy Web Gallery**
```bash
cd web
# Follow web/README.md for deployment
```

5. **Build Android App**
```bash
cd android
# Follow android/README.md for setup
```

## Development Workflow

1. User authenticates via Android app
2. User selects/captures image
3. Image uploaded to backend API
4. Backend validates and stores image (pending approval)
5. Admin reviews images via web dashboard
6. Approved images appear in public gallery
7. Public users view gallery without authentication

## Security & IAM

- **Authentication**: Firebase Identity Platform
- **Authorization**: Custom claims and role-based access
- **Storage**: Private buckets with signed URLs
- **API**: JWT token validation on all protected endpoints
- **Network**: Cloud Run with IAM-based access control

## Testing

```bash
# Backend tests
cd backend
python -m pytest

# Web tests
cd web
npm test

# Android tests
cd android
./gradlew test
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## API Documentation

See [API.md](docs/API.md) for complete API documentation.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

This is a portfolio project for demonstrating GCP skills. Feel free to fork and adapt for your own use.

## 💰 Cost-Optimized Deployment Guide

**Target Monthly Cost: $0-2** (vs $10-15 with Cloud SQL)

This guide uses **local PostgreSQL** instead of Cloud SQL to minimize costs while focusing on learning key GCP concepts: IAM, Cloud Storage, Cloud Run, and Firebase.

### 📋 What You'll Learn
- ✅ GCP project structure and resource hierarchy
- ✅ IAM roles, service accounts, and least privilege principles  
- ✅ Cloud Storage with bucket policies and lifecycle management
- ✅ Cloud Run serverless deployment with auto-scaling
- ✅ Firebase authentication and identity management
- ❌ **Skipping:** Cloud SQL (can add later if needed)

---

## 🏗️ GCP Structure: Understanding the Hierarchy

**GCP vs Azure comparison:**
```
Azure                           GCP
─────────────────────────────────────────────
Management Group         →      Organization (optional)
  └─ Subscription        →        └─ Folder (optional)
      └─ Resource Group  →            └─ Project ⭐
          └─ Resources   →                └─ Resources
```

**Key Concepts:**
- **Project** = Your billing boundary (like Azure Subscription + Resource Group)
- Your project: `image-gallery-481812`
- All resources (storage, Cloud Run, etc.) belong to this project
- Each project has its own IAM policies

---

## Deployment Checklist

### ✅ Phase 1: GCP Project Setup (COMPLETED)

- [x] **Create GCP Project**
  - Project ID: `image-gallery-481812`
  - Billing enabled ✅

- [x] **Install Required Tools**
  - [x] gcloud CLI (v550.0.0) ✅
  - [x] Authenticated as: kylehaggarty@gmail.com ✅
  - [x] Docker Desktop (v24.0.6) ✅
  - [x] Terraform (v1.14.3) ✅

- [x] **Enable Required GCP APIs** ✅
  ```bash
  # Already completed - all APIs enabled
  gcloud services list --enabled
  ```


### ✅ Phase 2: IAM & Service Accounts (COMPLETED)

**Understanding IAM:**
- Service accounts = identities for applications (like Azure Managed Identity)
- Roles = collections of permissions
- Principle of least privilege = grant minimum permissions needed

- [x] **Create Service Account for Backend** ✅

  Service account created: `gallery-backend@image-gallery-481812.iam.gserviceaccount.com`

- [x] **View Service Accounts** ✅

  ```bash
  gcloud iam service-accounts list
  ```

- [x] **Granted IAM Roles** ✅
  - ✅ `roles/firebase.admin` - Admin Firebase operations
  - ✅ `roles/storage.objectAdmin` - Full control of storage objects

  **Other key roles to know:**
  - `roles/run.invoker` - Invoke Cloud Run services (will use later)

- [ ] **🎓 Learning Exercise: Create Custom Role (Optional)**

  ```bash
  gcloud iam roles create galleryImageUploader \
      --project=image-gallery-481812 \
      --title="Gallery Image Uploader" \
      --description="Can only upload images to gallery bucket" \
      --permissions=storage.objects.create,storage.objects.get \
      --stage=GA
  ```

- [ ] **View Project IAM Policy**

  ```bash
  # See all IAM bindings for your project
  gcloud projects get-iam-policy image-gallery-481812 \
      --flatten="bindings[].members" \
      --format="table(bindings.role, bindings.members)"
  ```

---

### ✅ Phase 3: Cloud Storage Setup (COMPLETED)

- [x] **Create Storage Bucket** ✅

  Bucket created: `gs://image-gallery-481812-gallery-images`
  - Location: `us-central1`
  - Storage class: `STANDARD`

- [x] **Grant Storage Permissions (Project Level)** ✅

  Granted `roles/storage.objectAdmin` to service account

- [x] **Configure CORS** ✅

  CORS policy applied - allows web uploads from any origin

  ```bash
  # To verify:
  gsutil cors get gs://image-gallery-481812-gallery-images
  ```

- [x] **Set Lifecycle Policy (Auto-delete old pending images)** ✅

  Lifecycle policy applied - automatically deletes images in `pending/` folder after 90 days

  ```bash
  # To verify:
  gsutil lifecycle get gs://image-gallery-481812-gallery-images
  ```

  **What this does:** Automatically deletes images in `pending/` folder after 90 days (saves costs!)

---

### 🔥 Phase 4: Firebase Configuration (NEXT STEP - MANUAL)

**⚡ This is where you are now!** Complete this phase in your browser.

- [ ] **Setup Firebase Project**
  - Go to [Firebase Console](https://console.firebase.google.com/)
  - Click "Add Project"
  - **Select existing project:** `image-gallery-481812`
  - Disable Google Analytics (not needed for portfolio)
  - Click "Continue"

- [ ] **Enable Authentication**
  - Firebase Console → Build → Authentication
  - Click "Get Started"
  - Enable **Email/Password** provider
  - Enable **Google Sign-In** provider

- [ ] **Add Web App**
  - Firebase Console → Project Settings → Your apps
  - Click "Web" icon (</>) → "Add app"
  - App nickname: `Cloud Gallery Web`
  - **Don't** check Firebase Hosting
  - Click "Register app"
  - **Copy the Firebase config** (apiKey, authDomain, projectId, etc.)
  - Save for later (you'll put this in `web/.env`)

- [ ] **Add Android App**
  - Firebase Console → Project Settings → Your apps
  - Click "Android" icon → "Add app"
  - Package name: `com.cloudgallery.portfolio`
  - App nickname: `Cloud Gallery Android`
  - Click "Register app"
  - **Download `google-services.json`**
  - Place in `android/app/` directory

- [ ] **Grant Firebase Admin Role to Service Account**

  ```bash
  gcloud projects add-iam-policy-binding image-gallery-481812 \
      --member="serviceAccount:gallery-backend@image-gallery-481812.iam.gserviceaccount.com" \
      --role="roles/firebase.admin"
  ```

- [ ] **Create Service Account Key for Firebase Admin**

  ```bash
  gcloud iam service-accounts keys create firebase-admin-key.json \
      --iam-account=gallery-backend@image-gallery-481812.iam.gserviceaccount.com
  ```

  **⚠️ IMPORTANT:** Never commit `firebase-admin-key.json` to git!

  ```bash
  # Add to .gitignore
  echo "firebase-admin-key.json" >> .gitignore
  ```

---

### ✅ Phase 5: Local PostgreSQL Setup (COMPLETED)

**Why local database?**
- Cloud SQL costs $7-10/month
- Local PostgreSQL is free and perfect for development
- You'll learn GCP concepts without the database cost
- Can migrate to Cloud SQL later if needed

- [x] **Install PostgreSQL** ✅

  PostgreSQL 15 installed via Homebrew and service started

  ```bash
  # Verify installation
  psql --version
  # Should show: psql (PostgreSQL) 15.15
  ```

- [x] **Create Database and User** ✅

  Database created: `gallery`
  User created: `gallery_user` with password `dev_password_123`

- [x] **Test Database Connection** ✅

  ```bash
  psql -U gallery_user -d gallery -h localhost
  # Password: dev_password_123
  # Connection successful!
  ```

**💰 Cost saved:** ~$7-10/month!

---

### ✅ Phase 6: Backend Configuration (COMPLETED)

- [x] **Create Backend Environment File** ✅

  Created `backend/.env` with:
  - Local PostgreSQL connection: `postgresql://gallery_user:dev_password_123@localhost:5432/gallery`
  - GCP Project ID: `image-gallery-481812`
  - Bucket name: `image-gallery-481812-gallery-images`
  - Firebase credentials path: `../firebase-admin-key.json`

- [x] **Updated .gitignore** ✅

  Added to `.gitignore`:
  - `backend/.env`
  - `firebase-admin-key.json`
  - `cors.json`, `lifecycle.json`

---

### ⚙️ Phase 6: Backend Configuration

- [ ] **Update Backend Environment Variables**

  ```bash
  cd backend
  cp .env.example .env
  ```

  Edit `backend/.env`:

  ```env
  # Local PostgreSQL (not Cloud SQL!)
  DATABASE_URL=postgresql://gallery_user:dev_password_123@localhost:5432/gallery
  
  # GCP Project Settings
  PROJECT_ID=image-gallery-481812
  BUCKET_NAME=image-gallery-481812-gallery-images
  
  # Firebase Admin (path to service account key)
  FIREBASE_CREDENTIALS=../firebase-admin-key.json
  
  # App Settings
  PORT=8080
  FLASK_ENV=development
  ```

- [ ] **Install Python Dependencies**

  ```bash
  cd backend
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- [ ] **Initialize Database Schema**

  ```bash
  cd backend
  source venv/bin/activate
  python -c "from app import db, app; app.app_context().push(); db.create_all(); print('Database initialized!')"
  ```

- [ ] **Test Backend Locally**

  ```bash
  cd backend
  source venv/bin/activate
  python -m flask run --host=0.0.0.0 --port=8080
  
  # In another terminal, test:
  curl http://localhost:8080/health
  # Should return: {"status": "healthy"}
  ```

---

### 🚀 Phase 7: Deploy Backend to Cloud Run

**Cloud Run = Serverless containers with auto-scaling to zero (FREE when idle!)**

- [ ] **Ensure Docker Desktop is Running**

  ```bash
  docker ps
  # Should not show error - if it does, start Docker Desktop
  ```

- [ ] **Test Backend with Docker Locally (Optional)**

  ```bash
  cd backend
  docker build -t gallery-backend .
  docker run -p 8080:8080 --env-file .env gallery-backend
  
  # Test in another terminal
  curl http://localhost:8080/health
  ```

- [ ] **Build and Push to Google Container Registry**

  ```bash
  cd backend
  
  # Configure Docker authentication
  gcloud auth configure-docker
  
  # Build image
  gcloud builds submit --tag gcr.io/image-gallery-481812/gallery-backend
  ```

- [ ] **Deploy to Cloud Run**

  ```bash
  gcloud run deploy gallery-backend \
      --image gcr.io/image-gallery-481812/gallery-backend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars PROJECT_ID=image-gallery-481812 \
      --set-env-vars BUCKET_NAME=image-gallery-481812-gallery-images \
      --set-env-vars DATABASE_URL=YOUR_PRODUCTION_DB_URL \
      --service-account=gallery-backend@image-gallery-481812.iam.gserviceaccount.com \
      --max-instances=10 \
      --min-instances=0 \
      --memory=512Mi
  ```

  **⚠️ NOTE:** For production deployment with local DB, you'll need to either:
  1. Deploy Cloud SQL later and update DATABASE_URL
  2. Use a remote PostgreSQL service (like Supabase free tier)
  3. For now, test deployment with a dummy DATABASE_URL

- [ ] **Get Backend URL**

  ```bash
  gcloud run services describe gallery-backend \
      --platform managed \
      --region us-central1 \
      --format="value(status.url)"
  ```

  Backend URL: `_________________`

- [ ] **🎓 Learning Exercise: Cloud Run IAM**

  ```bash
  # View who can invoke your service
  gcloud run services get-iam-policy gallery-backend --region us-central1
  
  # Make it require authentication
  gcloud run services remove-iam-policy-binding gallery-backend \
      --region us-central1 \
      --member="allUsers" \
      --role="roles/run.invoker"
  
  # Add back public access (for API with its own auth)
  gcloud run services add-iam-policy-binding gallery-backend \
      --region us-central1 \
      --member="allUsers" \
      --role="roles/run.invoker"
  ```

---

### 🌐 Phase 8: Deploy Web Gallery

- [ ] **Configure Web Environment**

  ```bash
  cd web
  cp .env.example .env
  ```

  Edit `web/.env` with Firebase config from Phase 4:

  ```env
  VITE_API_URL=YOUR_BACKEND_URL_FROM_PHASE_7
  VITE_FIREBASE_API_KEY=your-api-key
  VITE_FIREBASE_AUTH_DOMAIN=image-gallery-481812.firebaseapp.com
  VITE_FIREBASE_PROJECT_ID=image-gallery-481812
  VITE_FIREBASE_STORAGE_BUCKET=image-gallery-481812.appspot.com
  VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
  VITE_FIREBASE_APP_ID=your-app-id
  ```

- [ ] **Install Dependencies and Build**

  ```bash
  cd web
  npm install
  npm run build
  ```

- [ ] **Deploy to Cloud Run**

  ```bash
  cd web
  
  # Build and push container
  gcloud builds submit --tag gcr.io/image-gallery-481812/gallery-web
  
  # Deploy
  gcloud run deploy gallery-web \
      --image gcr.io/image-gallery-481812/gallery-web \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --max-instances=10 \
      --min-instances=0
  ```

- [ ] **Get Web URL**

  ```bash
  gcloud run services describe gallery-web \
      --platform managed \
      --region us-central1 \
      --format="value(status.url)"
  ```

  Web URL: `_________________`

- [ ] **Test Web App**
  - Open web URL in browser
  - Verify gallery page loads
  - Test authentication flow

---

### 📱 Phase 9: Configure Android App

- [ ] **Open in Android Studio**
  - Open `android/` folder
  - Wait for Gradle sync

- [ ] **Verify Firebase Configuration**
  - Check `android/app/google-services.json` exists
  - Should have been added in Phase 4

- [ ] **Configure Backend URL**

  Edit `android/app/src/main/res/values/strings.xml`:

  ```xml
  <string name="api_base_url">YOUR_BACKEND_URL</string>
  ```

- [ ] **Build and Test**
  - Connect Android device or start emulator
  - Click Run in Android Studio
  - Test login and upload

---

### 👤 Phase 10: Create Admin User

- [ ] **Sign Up via Web**
  - Go to your web URL
  - Click Login
  - Create account with email/password

- [ ] **Grant Admin Permissions**

  Option A - Firebase Console:
  - Firebase Console → Authentication → Users
  - Find your user
  - Add custom claim: `{"admin": true}`

  Option B - Firebase CLI:

  ```bash
  npm install -g firebase-tools
  firebase login
  # Then use Firebase Admin SDK or Functions to set custom claims
  ```

- [ ] **Verify Admin Access**
  - Log out and log back in
  - Navigate to `/admin` route
  - Should see admin dashboard

---

### 🎉 Phase 11: Testing & Validation

- [ ] **End-to-End Test**
  - [ ] Android: Login → Upload image
  - [ ] Web Admin: Approve image
  - [ ] Web Public: View approved image

- [ ] **Security Validation**
  - [ ] Unauthenticated users can't upload
  - [ ] Non-admins can't access admin dashboard
  - [ ] Pending images not visible in public gallery

- [ ] **Cost Monitoring**

  ```bash
  # View current costs
  gcloud beta billing accounts list
  
  # Set budget alert
  # (Do this in GCP Console → Billing → Budgets)
  ```

---

## 📊 Expected Costs (This Setup)

| Service | Monthly Cost |
|---------|-------------|
| Cloud Storage (1,000 images) | $0.04 |
| Cloud Run Backend (low traffic) | $0.00 (free tier) |
| Cloud Run Web (low traffic) | $0.00 (free tier) |
| Firebase Auth | $0.00 (free tier) |
| Container Registry | $0.05 |
| Network Egress (minimal) | $0.10 |
| **TOTAL** | **~$0.20-2/month** 🎉 |

---

## 🎓 What You Learned

✅ **GCP Project Structure** - Projects, billing, resource hierarchy  
✅ **IAM** - Service accounts, roles, policies, least privilege  
✅ **Cloud Storage** - Buckets, IAM, lifecycle policies, CORS  
✅ **Cloud Run** - Serverless containers, auto-scaling, cost optimization  
✅ **Firebase** - Authentication, admin SDK, custom claims  

**Without paying for:**
❌ Cloud SQL ($7-10/month)  
❌ Always-on compute  
❌ Expensive managed services  

---

## 🔄 Optional: Migrate to Cloud SQL Later

If you want to learn Cloud SQL later, you can:

1. Create Cloud SQL instance ($7-10/month)
2. Update DATABASE_URL in backend
3. Redeploy to Cloud Run with `--add-cloudsql-instances`

But for portfolio/learning purposes, local DB is perfect!

---

## Author

Kyle Haggarty
