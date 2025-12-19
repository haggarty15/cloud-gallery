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

## Author

Kyle Haggarty
