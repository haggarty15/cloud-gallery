# Cloud Gallery 🎨

Transform photos into interactive paint-by-numbers coloring experiences.

**Status:** ✅ Working  
**Last Updated:** January 7, 2026

---

## Quick Start

### Android App
```powershell
cd android
.\check-and-run.ps1 -Build -Run
```

### Backend API
```powershell
cd backend
.\start-backend.ps1
```

---

## Features

### ✅ Implemented
- Email/password authentication (Firebase)
- Modern Material Design UI
- User sign up and login
- Home screen navigation
- Photo upload interface
- Gallery view
- Image-to-coloring template processing

### 🚧 In Progress
- Google Sign-In
- Canvas coloring functionality
- Backend API integration

---

## Project Structure

```
cloud-gallery/
├── android/              # Android app (Kotlin + Firebase)
├── backend/             # Flask API (Python + OpenCV)
├── web/                 # React frontend (future)
├── docs/                # Documentation
└── test-photos/         # Sample images
```

---

## Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Complete setup instructions
- **[Android Guide](docs/android/ANDROID_GUIDE.md)** - Android app development
- **[Firebase Auth](docs/android/FIREBASE_AUTH.md)** - Authentication setup

---

## Tech Stack

### Android
- Kotlin, Material Design 3
- Firebase Authentication
- Hilt (DI), KSP
- MVVM architecture

### Backend
- Python, Flask
- OpenCV, NumPy
- Canvas edge detection

### Future
- React + Vite (web frontend)
- PostgreSQL (database)
- Google Cloud Run (hosting)

---

## Getting Started

### Prerequisites
- Android Studio
- Python 3.x
- Firebase account

### Setup
1. Clone repository
2. Configure Firebase (see [Setup Guide](docs/SETUP_GUIDE.md))
3. Run Android app: `cd android && .\check-and-run.ps1 -Build -Run`
4. Run backend: `cd backend && .\start-backend.ps1`

---

## Commands Reference

### Android
```powershell
# Build and run
.\check-and-run.ps1 -Build -Run

# Check device
.\check-phone.ps1
```

### Backend
```powershell
# Start server
.\start-backend.ps1

# Process image
python app/canvas_processor.py image.jpg 20
```

---

## Firebase Project

**Project ID:** image-gallery-481812  
**Console:** https://console.firebase.google.com/project/image-gallery-481812

---

## License

MIT

---

## Status

**Build:** ✅ Passing  
**Android:** ✅ Runs on device  
**Backend:** ✅ Processing images  
**Tests:** Manual testing complete

