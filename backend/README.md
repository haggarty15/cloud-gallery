# Backend API

Flask-based backend API for the Cloud Gallery Portfolio system.

## Overview

RESTful API built with Flask that handles:
- User authentication via Firebase
- Image upload and storage
- Image approval workflow
- Public gallery endpoints

## Architecture

- **Framework**: Flask (Python 3.11+)
- **Database**: PostgreSQL via Cloud SQL
- **Storage**: Google Cloud Storage
- **Auth**: Firebase Admin SDK
- **Deployment**: Docker container on Cloud Run

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── auth.py              # Firebase authentication
│   ├── models.py            # Database models
│   ├── routes.py            # API endpoints
│   ├── storage.py           # Cloud Storage operations
│   └── utils.py             # Helper functions
├── tests/
│   ├── test_auth.py
│   ├── test_routes.py
│   └── test_storage.py
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (or Cloud SQL)
- Google Cloud Storage bucket
- Firebase project with Admin SDK credentials

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize database**
   ```bash
   python -c "from app import db; db.create_all()"
   ```

4. **Run development server**
   ```bash
   python -m flask run --host=0.0.0.0 --port=8080
   ```

## Environment Variables

```bash
PROJECT_ID=your-gcp-project-id
BUCKET_NAME=your-storage-bucket
DB_CONNECTION_NAME=project:region:instance  # For Cloud SQL
DB_NAME=gallery
DB_USER=postgres
DB_PASSWORD=your-db-password
FIREBASE_CREDENTIALS=./service-account-key.json
PORT=8080
```

## API Endpoints

See [API.md](../docs/API.md) for complete API documentation.

### Public Endpoints
- `GET /health` - Health check
- `GET /api/gallery` - Get approved images

### Authenticated Endpoints
- `POST /api/upload` - Upload image
- `GET /api/uploads` - Get user's uploads
- `DELETE /api/images/<id>` - Delete own image

### Admin Endpoints
- `GET /api/admin/pending` - Get pending images
- `POST /api/admin/approve/<id>` - Approve image
- `POST /api/admin/reject/<id>` - Reject image

## Database Schema

```sql
CREATE TABLE images (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    file_path VARCHAR(512) NOT NULL,
    thumbnail_path VARCHAR(512),
    mime_type VARCHAR(50),
    file_size INTEGER,
    width INTEGER,
    height INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by VARCHAR(128)
);

CREATE INDEX idx_images_status ON images(status);
CREATE INDEX idx_images_user_id ON images(user_id);
CREATE INDEX idx_images_uploaded_at ON images(uploaded_at DESC);
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_routes.py
```

## Docker Build

```bash
# Build image
docker build -t gallery-backend .

# Run container
docker run -p 8080:8080 \
  --env-file .env \
  gallery-backend
```

## Deployment to Cloud Run

```bash
# Build and push to Container Registry
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
  --set-secrets DB_PASSWORD=db-password:latest
```

## Security Considerations

- All sensitive data in Secret Manager
- JWT token validation on protected endpoints
- File upload validation (size, type, dimensions)
- Rate limiting per user
- CORS configured for specific origins
- SQL injection prevention via parameterized queries
- Input sanitization on all user input

## Performance

- Connection pooling for database
- Efficient image resizing for thumbnails
- Signed URLs for direct storage access
- Caching headers on static content
- Database indexes on frequently queried columns

## Monitoring

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gallery-backend"

# View metrics
gcloud monitoring dashboards list
```

## Troubleshooting

### Database Connection Issues
- Verify Cloud SQL instance is running
- Check Cloud SQL proxy configuration
- Verify IAM permissions for cloudsql.client

### Storage Issues
- Verify bucket exists and has correct permissions
- Check service account has storage.objectAdmin role
- Verify CORS configuration

### Authentication Issues
- Verify Firebase credentials are correct
- Check token is being sent in Authorization header
- Ensure Identity Toolkit API is enabled

## Future Enhancements

- [ ] Image compression and optimization
- [ ] Multiple image formats support (WebP, AVIF)
- [ ] Image moderation via Vision API
- [ ] Search functionality
- [ ] Tags and categories
- [ ] User profiles
- [ ] Image likes/favorites
- [ ] Comments on images
- [ ] Batch operations
- [ ] GraphQL API
