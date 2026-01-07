# Android App

Cloud Gallery Android application.

## Quick Start

```powershell
# Build and run
.\check-and-run.ps1 -Build -Run

# Check device connection
.\check-phone.ps1

# Check Firebase auth status
.\check-firebase-auth.ps1
```

## Structure

```
android/
├── app/
│   ├── src/main/
│   │   ├── java/           # Kotlin source
│   │   └── res/            # Resources
│   ├── build.gradle        # App config
│   └── google-services.json # Firebase
├── gradle/                 # Gradle wrapper
└── *.ps1                  # Helper scripts
```

## Documentation

See [docs/android/](../docs/android/) for detailed guides:
- [Android Guide](../docs/android/ANDROID_GUIDE.md)
- [Firebase Authentication](../docs/android/FIREBASE_AUTH.md)

## Build

```powershell
# Debug build
.\gradlew.bat assembleDebug

# Clean build
.\gradlew.bat clean assembleDebug
```

## Tech Stack

- Kotlin 1.9.20
- Material Design 3
- Firebase Authentication
- Hilt + KSP
- Gradle 8.5

