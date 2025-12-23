# Local Backend Setup Guide

## Overview
The backend runs locally with a local PostgreSQL database to avoid Cloud SQL costs.

## Prerequisites
- PostgreSQL 15 running locally on port 5432
- Database: `gallery`
- User: `gallery_user` (password: `dev_password_123`)
- Python 3.13 with virtual environment

## Environment Configuration
The `.env` file is configured with:
```
DATABASE_URL=postgresql+pg8000://gallery_user:dev_password_123@localhost:5432/gallery
PROJECT_ID=image-gallery-481812
BUCKET_NAME=image-gallery-481812-photos
FIREBASE_CREDENTIALS=firebase-admin-key.json
GOOGLE_APPLICATION_CREDENTIALS=firebase-admin-key.json
```

## Running the Backend

### 1. Activate virtual environment
```bash
# From project root
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
cd backend
```

### 2. Start the Flask server
```bash
python -m flask run --host=0.0.0.0 --port=8080
```

Or with gunicorn (production-like):
```bash
gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 app:app
```

### 3. Verify it's running
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T23:XX:XX.XXXXXXZ"
}
```

## Frontend Configuration
The web frontend is configured to use the local backend:
- `web/.env` has `VITE_API_URL=http://localhost:8080`

## Database Schema
Tables are created automatically on startup:
- `users` - User accounts
- `images` - Image metadata

## Troubleshooting

### Database connection failed
- Ensure PostgreSQL is running: `psql -U gallery_user -d gallery`
- Check DATABASE_URL in `.env` file
- Verify database exists: `createdb -U postgres gallery`

### Firebase credentials error
- Ensure `firebase-admin-key.json` exists in backend/ directory
- Check FIREBASE_CREDENTIALS path in `.env`

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.13)

## Cloud Run Deployment (Future)
The backend CAN be deployed to Cloud Run, but would need:
1. Cloud SQL instance (managed PostgreSQL)
2. DB_CONNECTION_NAME environment variable
3. VPC connector for private database access
4. Additional GCP costs (~$10-50/month)

For now, local development is the preferred approach.
