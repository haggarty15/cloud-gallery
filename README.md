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

## Deployment Checklist

Complete this checklist to get your Cloud Gallery system fully operational.

### 🎯 Phase 1: GCP Project Setup

- [ ] **Create GCP Project**
  - Create new project in [GCP Console](https://console.cloud.google.com/)
  - Project ID: `_________________`
  - Enable billing on the project

- [ ] **Install Required Tools**
  - [ ] Install [gcloud CLI](https://cloud.google.com/sdk/docs/install)
  - [ ] Run `gcloud auth login`
  - [ ] Run `gcloud config set project YOUR_PROJECT_ID`
  - [ ] Install Docker Desktop
  - [ ] Install Terraform (optional but recommended)

- [ ] **Enable Required GCP APIs**
  ```bash
  gcloud services enable run.googleapis.com
  gcloud services enable storage.googleapis.com
  gcloud services enable sqladmin.googleapis.com
  gcloud services enable identitytoolkit.googleapis.com
  gcloud services enable cloudbuild.googleapis.com
  gcloud services enable secretmanager.googleapis.com
  ```

### 🔥 Phase 2: Firebase Configuration

- [ ] **Setup Firebase Project**
  - [ ] Go to [Firebase Console](https://console.firebase.google.com/)
  - [ ] Add Firebase to your GCP project (use existing project)
  - [ ] Enable Authentication methods:
    - [ ] Email/Password
    - [ ] Google Sign-In

- [ ] **Get Firebase Credentials for Web**
  - [ ] In Firebase Console → Project Settings → Add Web App
  - [ ] Copy the Firebase config (apiKey, authDomain, etc.)
  - [ ] Save these values for `web/.env` file

- [ ] **Get Firebase Credentials for Android**
  - [ ] In Firebase Console → Project Settings → Add Android App
  - [ ] Package name: `com.cloudgallery.portfolio`
  - [ ] Download `google-services.json`
  - [ ] Place in `android/app/` directory

- [ ] **Create Firebase Admin Service Account**
  ```bash
  gcloud iam service-accounts create gallery-backend \
      --display-name="Gallery Backend Service Account"
  
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/firebase.admin"
  
  gcloud iam service-accounts keys create service-account-key.json \
      --iam-account=gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com
  ```
  - [ ] Save `service-account-key.json` securely (DO NOT commit to git!)

### 💾 Phase 3: Cloud Storage Setup

- [ ] **Create Storage Bucket**
  ```bash
  gsutil mb -l us-central1 gs://YOUR_PROJECT_ID-gallery-images
  ```

- [ ] **Configure CORS for Bucket**
  ```bash
  echo '[{"origin": ["*"], "method": ["GET", "HEAD", "PUT", "POST"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]' > cors.json
  gsutil cors set cors.json gs://YOUR_PROJECT_ID-gallery-images
  ```

- [ ] **Set Lifecycle Policy** (auto-delete old pending images)
  ```bash
  echo '{"lifecycle": {"rule": [{"action": {"type": "Delete"}, "condition": {"age": 90, "matchesPrefix": ["pending/"]}}]}}' > lifecycle.json
  gsutil lifecycle set lifecycle.json gs://YOUR_PROJECT_ID-gallery-images
  ```

- [ ] **Grant Storage Permissions**
  ```bash
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/storage.objectAdmin"
  ```

### 🗄️ Phase 4: Cloud SQL Database Setup

- [ ] **Create PostgreSQL Instance**
  ```bash
  gcloud sql instances create gallery-db \
      --database-version=POSTGRES_15 \
      --tier=db-f1-micro \
      --region=us-central1 \
      --root-password=YOUR_SECURE_PASSWORD
  ```
  - Root password: `_________________` (save securely!)

- [ ] **Create Database**
  ```bash
  gcloud sql databases create gallery --instance=gallery-db
  ```

- [ ] **Get Connection Name** (save for later)
  ```bash
  gcloud sql instances describe gallery-db --format="value(connectionName)"
  ```
  - Connection name: `_________________`

- [ ] **Grant SQL Permissions**
  ```bash
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/cloudsql.client"
  ```

- [ ] **Store DB Password in Secret Manager**
  ```bash
  echo -n "YOUR_SECURE_PASSWORD" | gcloud secrets create db-password --data-file=-
  gcloud secrets add-iam-policy-binding db-password \
      --member="serviceAccount:gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/secretmanager.secretAccessor"
  ```

- [ ] **Store Firebase Key in Secret Manager**
  ```bash
  gcloud secrets create firebase-key --data-file=service-account-key.json
  gcloud secrets add-iam-policy-binding firebase-key \
      --member="serviceAccount:gallery-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/secretmanager.secretAccessor"
  ```

### 🚀 Phase 5: Deploy Backend API

- [ ] **Configure Backend Environment**
  ```bash
  cd backend
  cp .env.example .env
  ```
  Edit `.env` with your values:
  - `PROJECT_ID=YOUR_PROJECT_ID`
  - `BUCKET_NAME=YOUR_PROJECT_ID-gallery-images`
  - `DB_CONNECTION_NAME=YOUR_CONNECTION_NAME`
  - `DB_PASSWORD=YOUR_DB_PASSWORD`

- [ ] **Build Backend Container**
  ```bash
  gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gallery-backend
  ```

- [ ] **Deploy to Cloud Run**
  ```bash
  gcloud run deploy gallery-backend \
      --image gcr.io/YOUR_PROJECT_ID/gallery-backend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --add-cloudsql-instances YOUR_CONNECTION_NAME \
      --set-env-vars PROJECT_ID=YOUR_PROJECT_ID \
      --set-env-vars BUCKET_NAME=YOUR_PROJECT_ID-gallery-images \
      --set-env-vars DB_CONNECTION_NAME=YOUR_CONNECTION_NAME \
      --set-env-vars DB_NAME=gallery \
      --set-env-vars DB_USER=postgres \
      --set-secrets DB_PASSWORD=db-password:latest \
      --set-secrets FIREBASE_CREDENTIALS=firebase-key:latest
  ```

- [ ] **Save Backend URL**
  ```bash
  gcloud run services describe gallery-backend --platform managed --region us-central1 --format "value(status.url)"
  ```
  - Backend URL: `_________________`

- [ ] **Test Backend Health**
  ```bash
  curl YOUR_BACKEND_URL/health
  ```
  Should return: `{"status": "healthy"}`

### 🌐 Phase 6: Deploy Web Gallery

- [ ] **Configure Web Environment**
  ```bash
  cd web
  cp .env.example .env
  ```
  Edit `.env` with your Firebase config and backend URL:
  - `VITE_API_URL=YOUR_BACKEND_URL`
  - `VITE_FIREBASE_API_KEY=...`
  - `VITE_FIREBASE_AUTH_DOMAIN=...`
  - (all other Firebase values)

- [ ] **Build Web App**
  ```bash
  npm install
  npm run build
  ```

- [ ] **Deploy to Cloud Run**
  ```bash
  gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gallery-web
  gcloud run deploy gallery-web \
      --image gcr.io/YOUR_PROJECT_ID/gallery-web \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
  ```

- [ ] **Save Web URL**
  ```bash
  gcloud run services describe gallery-web --platform managed --region us-central1 --format "value(status.url)"
  ```
  - Web URL: `_________________`

- [ ] **Test Web App**
  - [ ] Open web URL in browser
  - [ ] Verify gallery page loads
  - [ ] Test login functionality

### 📱 Phase 7: Configure Android App

- [ ] **Setup Android Studio**
  - [ ] Open `android/` folder in Android Studio
  - [ ] Wait for Gradle sync

- [ ] **Add Firebase Config**
  - [ ] Verify `google-services.json` is in `android/app/`
  - [ ] Check file is not in `.gitignore`

- [ ] **Configure Backend URL**
  - [ ] Edit `android/app/src/main/res/values/strings.xml`
  - [ ] Add: `<string name="api_base_url">YOUR_BACKEND_URL</string>`

- [ ] **Build and Test**
  - [ ] Connect Android device or start emulator
  - [ ] Click Run button in Android Studio
  - [ ] Test login and image upload

### 👤 Phase 8: Create Admin User

- [ ] **Sign Up via Web Interface**
  - [ ] Go to your web URL
  - [ ] Click Login
  - [ ] Create account with email/password

- [ ] **Grant Admin Permissions**
  - [ ] Go to Firebase Console → Authentication → Users
  - [ ] Find your user
  - [ ] Click on user → Custom Claims tab
  - [ ] Add custom claim: `{"admin": true}`
  
  Or use Firebase CLI:
  ```bash
  npm install -g firebase-tools
  firebase login
  firebase functions:config:set admin.email="your-email@example.com"
  ```

- [ ] **Verify Admin Access**
  - [ ] Log out and log back in to web app
  - [ ] Navigate to `/admin` route
  - [ ] Verify admin dashboard is accessible

### 🌍 Phase 9: Custom Domain Setup (Optional)

- [ ] **Map Custom Domain to Cloud Run**
  ```bash
  gcloud run domain-mappings create --service gallery-web --domain gallery.yourdomain.com --region us-central1
  ```

- [ ] **Update DNS Records**
  - [ ] Add DNS records provided by Cloud Run to your domain registrar
  - [ ] Wait for DNS propagation (can take up to 48 hours)

- [ ] **Update Firebase Authorized Domains**
  - [ ] Firebase Console → Authentication → Settings
  - [ ] Add your custom domain to authorized domains

- [ ] **Update CORS Configuration**
  - Update your storage bucket CORS to include your custom domain

### 🔍 Phase 10: Testing & Verification

- [ ] **End-to-End Test**
  - [ ] Android: Login → Upload image with title/description
  - [ ] Web Admin: Login → See pending image → Approve it
  - [ ] Web Public: Refresh gallery → See approved image
  - [ ] Click image to view full size in modal

- [ ] **Security Checks**
  - [ ] Verify unauthenticated users can't access `/api/upload`
  - [ ] Verify non-admin users can't access `/admin` dashboard
  - [ ] Verify pending images are NOT visible in public gallery

- [ ] **Monitoring Setup**
  ```bash
  # View recent logs
  gcloud logging read "resource.type=cloud_run_revision" --limit 50
  ```

### 📊 Phase 11: Cost Optimization & Monitoring

- [ ] **Set Billing Budget Alert**
  - [ ] Go to GCP Console → Billing → Budgets & alerts
  - [ ] Create budget alert (e.g., $20/month)

- [ ] **Configure Cloud Monitoring**
  - [ ] Set up uptime checks for backend and web URLs
  - [ ] Create alert for error rates

- [ ] **Review Cloud Run Settings**
  - [ ] Set max instances to prevent runaway costs
  - [ ] Consider min instances=0 for development (scales to zero)

### 🎉 Phase 12: Go Live!

- [ ] **Share Your Gallery**
  - Web URL: `_________________`
  - Custom domain: `_________________`

- [ ] **Update README**
  - [ ] Add live demo link to README
  - [ ] Add screenshots
  - [ ] Update portfolio/resume with project link

- [ ] **Consider Next Steps**
  - [ ] Set up CI/CD with Cloud Build triggers
  - [ ] Add image categories/tags
  - [ ] Implement image search
  - [ ] Add CDN (Cloud CDN)
  - [ ] Add monitoring dashboard
  - [ ] Implement backup strategy

---

## Author

Kyle Haggarty
