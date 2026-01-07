# 🎨 Digital Paint-by-Numbers Coloring App

A Zen Color-style app where users transform personal photos into interactive coloring experiences:
- **Upload your photos** → AI converts to numbered coloring templates
- **Color in-app** with tap-to-fill interaction (tap color, tap region)
- **Save & share** completed artwork to your gallery
- **Built with GCP** - Cloud Run, Cloud Storage, Firebase Auth
- **Cost-optimized** development setup (~$0.04/month)

> **Note:** This project demonstrates GCP best practices while building a fun, interactive coloring app!

## Architecture Overview

### Digital Coloring Workflow

```
1. Upload Photo          2. AI Processing         3. Interactive Canvas
   [User's Photo]    →   [Canvas Generator]    →    [Tap-to-Fill UI]
                         - Edge detection             - Color picker bar
                         - Region extraction          - Click detection
                         - Color palette              - Progress tracking
                                ↓
                         [JSON Output]
                         {regions, colors,
                          boundaries}
                                ↓
4. Save & Share
   [Completed Artwork] → Gallery → Export/Share
```

### Current Architecture (Development - Cost Optimized)

```
┌─────────────────┐
│  Web App        │──────┐
│  (React/Vite)   │      │
└─────────────────┘      │
                         │ Firebase Auth
┌─────────────────┐      │
│  Android App    │──────┤
│  (Kotlin)       │      │
└─────────────────┘      ▼
                  ┌──────────────┐
                  │  Backend API │
                  │  (Flask)     │──── Canvas Processor
                  │  Cloud Run   │     (OpenCV + K-Means)
                  └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Cloud Storage │ │ PostgreSQL   │ │   Firebase   │
│  (Images)    │ │   (Local)    │ │Identity Plat.│
│ us-central1  │ │  localhost   │ │    (Auth)    │
└──────────────┘ └──────────────┘ └──────────────┘
```

**Key Design Decisions:**
- ✅ **OpenCV + Scikit-Learn** for intelligent region detection
- ✅ **Local PostgreSQL** instead of Cloud SQL (saves $7-10/month)
- ✅ **Cloud Run** with auto-scaling to zero (free when idle)
- ✅ **Cloud Storage** with lifecycle policies (pennies per month)
- ✅ **Firebase Authentication** (free tier)

### Production Architecture (Optional - Add Cloud SQL Later)

When ready to deploy to production, you can migrate to Cloud SQL:

```
Backend API → Cloud SQL (PostgreSQL) instead of localhost
             └─ Connected via Cloud SQL Proxy
             └─ Private IP for security
             └─ Cost: ~$7-10/month for db-f1-micro
```

## Use Cases

### 🎨 Primary Use Case: Digital Coloring App

A relaxing, creative app where users:

1. **Upload Personal Photos**
   - Family photos, pet pictures, vacation snapshots
   - Selfies, landscapes, or any meaningful image

2. **AI Generates Coloring Template**
   - Automatic edge detection and region segmentation
   - Smart color palette generation (10-50 colors)
   - Choose difficulty: Easy, Medium, or Hard

3. **Color In-App** (Like Zen Color)
   - Tap a color from the bottom bar
   - Tap regions to fill with that color
   - See progress: "45% Complete"
   - Auto-save as you go

4. **Save & Share Artwork**
   - Gallery of completed colorings
   - Before/After comparison
   - Export and share on social media

**Perfect for:**
- 🧘 Mindful relaxation and stress relief
- 🎁 Creating personalized gifts
- 👨‍👩‍👧 Family activity (kids love coloring their own photos!)
- 🎨 Artistic expression without drawing skills

### 📚 Secondary Use Case: Learning GCP Concepts

This project also demonstrates:

1. **GCP Project Structure & IAM**
   - Understanding projects as billing boundaries
   - Service accounts and role-based access control
   - Principle of least privilege

2. **Cloud Storage Management**
   - Bucket creation and configuration
   - CORS policies for web uploads
   - Lifecycle policies for cost optimization
   - IAM policies at bucket and project level

3. **Serverless Deployment (Cloud Run)**
   - Container-based serverless architecture
   - Auto-scaling including scale-to-zero
   - Environment variable and secret management
   - Service account assignment for runtime identity

4. **Firebase Integration**
   - Authentication across multiple platforms (Web, Android)
   - Firebase Admin SDK for backend token verification
   - Custom claims for role-based authorization

5. **Cost Optimization**
   - Choosing appropriate services for development vs production
   - Using free tiers effectively
   - Lifecycle policies and auto-cleanup
   - Monitoring costs and setting budget alerts

### 🎯 Portfolio Project

Perfect for demonstrating to potential employers:
- Full-stack development skills (Python, React, Kotlin)
- Cloud architecture knowledge (GCP services)
- Computer vision & image processing (OpenCV)
- Security best practices (IAM, authentication, authorization)
- Product thinking (pivoting from gallery to coloring app)
## 🚀 Quick Start

### For Users
1. Visit the web app (once deployed)
2. Sign in with Google or email
3. Upload a photo
4. Wait for AI processing (~30 seconds)
5. Start coloring! Tap colors, tap regions
6. Save your completed artwork

### For Developers
See **[SETUP.md](SETUP.md)** for complete setup instructions.

**Quick test of canvas generator:**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install opencv-python scikit-learn scipy numpy pillow
python app/canvas_processor.py test-photos/sample.jpg 20
```

Check `output/` folder for generated coloring template!

## Project Structure

```
cloud-gallery/
├── backend/                    # Flask API + Image Processing
│   ├── app/
│   │   ├── canvas_processor.py    # 🎨 Core: Photo → Coloring regions
│   │   ├── routes.py              # API endpoints
│   │   ├── models.py              # Database models
│   │   └── storage.py             # Cloud Storage integration
│   ├── requirements.txt
│   └── README.md
├── web/                        # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ColoringCanvas.jsx  # TODO: Interactive canvas
│   │   │   ├── Gallery.jsx
│   │   │   └── Login.jsx
│   │   └── services/
│   │       ├── api.js
│   │       └── firebase.js
│   ├── package.json
│   └── README.md
├── android/                    # Android App (Kotlin)
│   ├── app/
│   └── README.md
├── infrastructure/             # GCP Terraform configs
│   └── terraform/
├── docs/                       # API docs, deployment guides
├── DIGITAL_COLORING_VISION.md  # 📖 Product vision
├── PAINT_BY_NUMBERS_PLAN.md    # Architecture plan
├── SETUP.md                    # 🚀 Setup guide
└── README.md                   # This file
```

## Features

### ✅ Already Built

**Canvas Processing Engine:**
- ✅ Photo → Numbered regions (OpenCV edge detection)
- ✅ Smart color palette generation (K-means clustering)
- ✅ Region boundary extraction for tap detection
- ✅ JSON output format for web/mobile rendering
- ✅ Adjustable difficulty (10-50 colors)

**Infrastructure:**
- ✅ GCP project setup
- ✅ Cloud Storage bucket configured
- ✅ Firebase Authentication enabled
- ✅ Service accounts & IAM roles
- ✅ Local PostgreSQL for development

### 🚧 In Progress

**Backend API:**
- ⏳ `/api/projects/create` - Upload & process image
- ⏳ `/api/projects/:id` - Get coloring canvas data
- ⏳ `/api/coloring/fill` - Save user's filled regions
- ⏳ `/api/coloring/complete` - Export finished artwork

**Frontend:**
- ⏳ ColoringCanvas.jsx - Interactive tap-to-fill component
- ⏳ Color picker bar UI (bottom of screen)
- ⏳ Progress tracking ("45% complete")
- ⏳ Gallery of completed works

### 🎯 Roadmap

**Phase 2: Backend API (Current)**
- Build RESTful endpoints for coloring workflow
- Database schema for projects & sessions
- Image processing queue with Cloud Tasks

**Phase 3: Frontend Canvas (Next)**
- SVG-based interactive canvas
- Click detection on regions
- Real-time coloring feedback
- Auto-save functionality

**Phase 4: Polish & Deploy**
- Mobile responsive design
- Share functionality
- Cloud Run deployment
- Performance optimization

## GCP Services Used

### Currently Active (Cost-Optimized Setup)

1. **Cloud Storage** 💰 ~$0.04/month
   - Image blob storage in `us-central1`
   - CORS configuration for web uploads
   - Lifecycle policies (auto-delete old pending images)
   - IAM policies for service account access

2. **Identity Platform (Firebase)** 💰 FREE
   - Firebase Authentication for web and mobile
   - Email/Password and Google Sign-In providers
   - Custom claims for admin role management
   - Firebase Admin SDK for backend token verification

3. **IAM & Service Accounts** 💰 FREE
   - Service account: `gallery-backend`
   - Role-based access control (RBAC)
   - Least privilege principle
   - Project-level and resource-level permissions

4. **Cloud Run** 💰 FREE (free tier + scale-to-zero)
   - Serverless container platform for backend API
   - Serverless container platform for web frontend
   - Auto-scaling from 0 to N instances
   - Pay only for actual usage (requests)

5. **Cloud Build** 💰 FREE (120 build-minutes/day)
   - Container image builds
   - Push to Google Container Registry
   - CI/CD pipeline support

### Development Environment

6. **PostgreSQL (Local)** 💰 FREE
   - Running locally instead of Cloud SQL
   - Saves $7-10/month while learning
   - Can migrate to Cloud SQL later for production

### Optional (Can Add Later)

- **Cloud SQL**: Managed PostgreSQL (~$7-10/month for db-f1-micro)
- **Secret Manager**: Secure credential storage (~$0.06/month)
- **Cloud Monitoring**: Metrics and logging (free tier available)
- **Cloud CDN**: Content delivery network for images
- **VPC**: Private networking for enhanced security

**Total Current Monthly Cost: ~$0-2** 🎉

## Getting Started

### Prerequisites
- Google Cloud Platform account with billing enabled
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

### Current Workflow (When Fully Deployed)

1. **User Authentication**
   - User opens Android app
   - Authenticates via Firebase (Email/Password or Google Sign-In)
   - Firebase returns JWT token

2. **Image Upload**
   - User selects/captures image
   - App sends image + metadata to backend API
   - Backend verifies Firebase token
   - Backend validates image (format, size, dimensions)

3. **Storage & Processing**
   - Backend uploads image to Cloud Storage (`pending/` folder)
   - Backend creates thumbnail
   - Backend stores metadata in PostgreSQL (status: pending)

4. **Admin Review**
   - Admin logs into web dashboard
   - Reviews pending images
   - Approves or rejects

5. **Public Display**
   - Approved images moved to `approved/` folder
   - Status updated in database
   - Public gallery fetches only approved images
   - No authentication required to view

### Development Status

**✅ Completed (Ready to Use):**
- GCP project setup and billing
- Cloud Storage bucket with policies
- IAM service accounts and roles
- Local PostgreSQL database
- Backend configuration

**🔄 In Progress (Next Steps):**
- Firebase Authentication setup
- Backend development and testing
- Cloud Run deployment
- Web frontend deployment
- Android app configuration

**📍 You Are Here:** Ready to set up Firebase Authentication

## Security & IAM

**Current Implementation:**

- **IAM & Service Accounts** ✅
  - Service account: `gallery-backend@image-gallery-481812.iam.gserviceaccount.com`
  - Roles: `firebase.admin`, `storage.objectAdmin`
  - Principle of least privilege

- **Cloud Storage Security** ✅
  - Private bucket (not publicly accessible)
  - IAM policies for service account access
  - CORS configured for authorized origins
  - Lifecycle policies for automatic cleanup

- **Authentication** (In Progress)
  - Firebase Identity Platform
  - Email/Password and Google Sign-In providers
  - JWT token validation on backend endpoints
  - Custom claims for admin role management

- **Authorization** (To Be Implemented)
  - Role-based access control (RBAC)
  - Admin-only endpoints for approval workflow
  - User-only access to own uploaded images

- **Data Security**
  - Local PostgreSQL for development (isolated)
  - Environment variables for configuration (not committed)
  - Service account keys protected in .gitignore

- **Network Security** (To Be Configured)
  - Cloud Run with IAM-based access control
  - HTTPS by default
  - Signed URLs for temporary image access

## Testing

```bash
# Backend tests (once dependencies installed)
cd backend
python -m pytest

# Web tests (once dependencies installed)
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

### ✅ Phase 4: Firebase Configuration (COMPLETED)

**🎉 Phase completed on December 21-22, 2025**

- [x] **Setup Firebase Project** ✅
  - Firebase linked to existing GCP project: `image-gallery-481812`
  - Google Analytics: Enabled

- [x] **Enable Authentication** ✅
  - ✅ Email/Password provider enabled
  - ✅ Google Sign-In provider enabled

- [x] **Add Web App** ✅
  - App nickname: `Cloud Gallery Web`
  - Firebase Hosting: Enabled
  - Configuration saved to: `web/.env`

- [x] **Add Android App** ✅
  - Package name: `com.cloudgallery.portfolio`
  - App nickname: `Cloud Gallery Android`
  - File downloaded: `android/app/google-services.json` ✅

- [x] **Firebase Admin SDK Key** ✅
  - Downloaded and saved to: `backend/firebase-admin-key.json` ✅
  - Protected in `.gitignore`

**📝 Note:** SHA-1 certificate generation skipped (requires JDK). Can add later for Google Sign-In on Android. Email/Password auth works without it.

**📁 Files created:**
- `android/app/google-services.json` (1.0 KB)
- `backend/firebase-admin-key.json` (2.3 KB)
- `web/.env` (Firebase config populated)

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
