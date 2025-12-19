# Deployment Guide

This guide covers the complete deployment process for the Cloud Gallery Portfolio system on Google Cloud Platform.

## Prerequisites

1. **GCP Account & Project**
   - Active GCP account
   - New project created (e.g., `cloud-gallery-project`)
   - Billing enabled

2. **Local Tools**
   - gcloud CLI installed and configured
   - Docker installed
   - Terraform installed (optional)

3. **APIs to Enable**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable sqladmin.googleapis.com
   gcloud services enable identitytoolkit.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable firebasehosting.googleapis.com
   ```

## Step 1: Firebase Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Add Firebase to your existing GCP project
   - Enable Authentication with Email/Password and Google providers

2. **Get Firebase Config**
   - In Firebase Console, go to Project Settings
   - Add a Web app to get config (for web gallery)
   - Add an Android app (package name: `com.cloudgallery.portfolio`)
   - Download `google-services.json` for Android app

3. **Generate Service Account Key**
   ```bash
   gcloud iam service-accounts create gallery-backend \
       --display-name="Gallery Backend Service Account"
   
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member="serviceAccount:gallery-backend@PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/firebase.admin"
   
   gcloud iam service-accounts keys create service-account-key.json \
       --iam-account=gallery-backend@PROJECT_ID.iam.gserviceaccount.com
   ```

## Step 2: Cloud Storage Setup

1. **Create Storage Bucket**
   ```bash
   gsutil mb -l us-central1 gs://PROJECT_ID-gallery-images
   
   # Set lifecycle policy to delete old pending images
   cat > lifecycle.json << EOF
   {
     "lifecycle": {
       "rule": [
         {
           "action": {"type": "Delete"},
           "condition": {
             "age": 90,
             "matchesPrefix": ["pending/"]
           }
         }
       ]
     }
   }
   EOF
   
   gsutil lifecycle set lifecycle.json gs://PROJECT_ID-gallery-images
   ```

2. **Configure CORS**
   ```bash
   cat > cors.json << EOF
   [
     {
       "origin": ["*"],
       "method": ["GET", "HEAD", "PUT", "POST"],
       "responseHeader": ["Content-Type"],
       "maxAgeSeconds": 3600
     }
   ]
   EOF
   
   gsutil cors set cors.json gs://PROJECT_ID-gallery-images
   ```

## Step 3: Cloud SQL Setup

1. **Create PostgreSQL Instance**
   ```bash
   gcloud sql instances create gallery-db \
       --database-version=POSTGRES_15 \
       --tier=db-f1-micro \
       --region=us-central1 \
       --root-password=SECURE_PASSWORD
   ```

2. **Create Database**
   ```bash
   gcloud sql databases create gallery --instance=gallery-db
   ```

3. **Get Connection Name**
   ```bash
   gcloud sql instances describe gallery-db --format="value(connectionName)"
   # Save this for backend configuration
   ```

## Step 4: Deploy Backend API

1. **Prepare Backend**
   ```bash
   cd backend
   
   # Create .env file
   cat > .env << EOF
   PROJECT_ID=your-project-id
   BUCKET_NAME=your-project-id-gallery-images
   DB_CONNECTION_NAME=your-connection-name
   DB_NAME=gallery
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   FIREBASE_CREDENTIALS=./service-account-key.json
   EOF
   ```

2. **Build and Deploy to Cloud Run**
   ```bash
   # Build container
   gcloud builds submit --tag gcr.io/PROJECT_ID/gallery-backend
   
   # Deploy to Cloud Run
   gcloud run deploy gallery-backend \
       --image gcr.io/PROJECT_ID/gallery-backend \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated \
       --add-cloudsql-instances PROJECT_ID:us-central1:gallery-db \
       --set-env-vars PROJECT_ID=PROJECT_ID \
       --set-env-vars BUCKET_NAME=PROJECT_ID-gallery-images \
       --set-env-vars DB_CONNECTION_NAME=PROJECT_ID:us-central1:gallery-db \
       --set-env-vars DB_NAME=gallery \
       --set-env-vars DB_USER=postgres \
       --set-secrets DB_PASSWORD=db-password:latest \
       --set-secrets FIREBASE_CREDENTIALS=firebase-key:latest
   ```

3. **Note Backend URL**
   ```bash
   gcloud run services describe gallery-backend \
       --platform managed \
       --region us-central1 \
       --format "value(status.url)"
   ```

## Step 5: Deploy Web Gallery

1. **Configure Web App**
   ```bash
   cd web
   
   # Create .env file
   cat > .env.production << EOF
   REACT_APP_API_URL=https://gallery-backend-xxx.run.app
   REACT_APP_FIREBASE_API_KEY=your-api-key
   REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   REACT_APP_FIREBASE_PROJECT_ID=your-project-id
   REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   REACT_APP_FIREBASE_APP_ID=your-app-id
   EOF
   ```

2. **Build and Deploy**
   ```bash
   # Build production bundle
   npm install
   npm run build
   
   # Deploy to Cloud Run
   gcloud run deploy gallery-web \
       --source . \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated
   ```

   Or use Firebase Hosting:
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase init hosting
   firebase deploy --only hosting
   ```

## Step 6: Configure Android App

1. **Add google-services.json**
   - Place downloaded `google-services.json` in `android/app/`

2. **Update Configuration**
   - Edit `android/app/src/main/res/values/strings.xml`
   - Add backend API URL:
     ```xml
     <string name="api_base_url">https://gallery-backend-xxx.run.app</string>
     ```

3. **Build APK**
   ```bash
   cd android
   ./gradlew assembleDebug
   # APK will be in app/build/outputs/apk/debug/
   ```

## Step 7: IAM Configuration

1. **Backend Service Account Roles**
   ```bash
   # Storage access
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member="serviceAccount:gallery-backend@PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/storage.objectAdmin"
   
   # Cloud SQL client
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member="serviceAccount:gallery-backend@PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/cloudsql.client"
   ```

2. **Create Admin User**
   - Sign up via web interface
   - Use Firebase Console to add custom claim:
     ```json
     {
       "admin": true
     }
     ```

## Step 8: Verify Deployment

1. **Test Backend API**
   ```bash
   curl https://gallery-backend-xxx.run.app/health
   # Should return: {"status": "healthy"}
   ```

2. **Test Web Gallery**
   - Open web URL in browser
   - Verify gallery loads
   - Test authentication

3. **Test Android App**
   - Install APK on device/emulator
   - Test login
   - Test image upload

## Monitoring & Logging

1. **View Logs**
   ```bash
   # Backend logs
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gallery-backend" --limit 50
   
   # Web logs
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gallery-web" --limit 50
   ```

2. **Set up Alerts**
   - Configure Cloud Monitoring alerts for errors
   - Set budget alerts for cost control

## Cost Optimization

1. **Cloud Run**: Pay per request, scales to zero
2. **Cloud SQL**: Use smallest tier (db-f1-micro) for development
3. **Cloud Storage**: Enable lifecycle policies to delete old files
4. **Consider**: Cloud Run always-allocated instances for production

## Troubleshooting

### Backend won't connect to database
- Verify Cloud SQL connection string
- Check IAM permissions for cloudsql.client role
- Ensure Cloud SQL Admin API is enabled

### Images not uploading
- Check bucket permissions
- Verify CORS configuration
- Check storage.objectAdmin role

### Firebase auth issues
- Verify Firebase config matches in all apps
- Check API keys are not restricted
- Ensure Identity Platform API is enabled

## Security Checklist

- [ ] Database password stored in Secret Manager
- [ ] Service account keys not committed to git
- [ ] CORS configured correctly (not "*" in production)
- [ ] Cloud Run services have proper IAM policies
- [ ] Firebase security rules configured
- [ ] Regular security audits enabled

## Next Steps

1. Set up CI/CD with Cloud Build
2. Implement automated testing pipeline
3. Add monitoring dashboards
4. Configure custom domain
5. Enable CDN for images
6. Implement backup strategy
