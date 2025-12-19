# Android App

Android mobile application for the Cloud Gallery Portfolio system.

## Overview

Native Android app for uploading images to the cloud gallery with Firebase authentication.

## Features

- **Firebase Authentication**: Email/password and Google Sign-In
- **Camera Integration**: Capture photos directly from camera
- **Gallery Picker**: Select images from device gallery
- **Image Upload**: Upload images with title and description
- **Upload Status**: Track upload progress and approval status
- **Material Design**: Modern UI following Material Design guidelines

## Technology Stack

- **Language**: Kotlin
- **Min SDK**: API 24 (Android 7.0)
- **Target SDK**: API 34 (Android 14)
- **Architecture**: MVVM with Repository pattern
- **DI**: Hilt
- **Networking**: Retrofit + OkHttp
- **Image Loading**: Coil
- **Authentication**: Firebase SDK
- **Async**: Kotlin Coroutines + Flow

## Project Structure

```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/cloudgallery/portfolio/
│   │   │   │   ├── ui/
│   │   │   │   │   ├── MainActivity.kt
│   │   │   │   │   ├── LoginActivity.kt
│   │   │   │   │   ├── UploadActivity.kt
│   │   │   │   │   └── UploadsListActivity.kt
│   │   │   │   ├── data/
│   │   │   │   │   ├── api/
│   │   │   │   │   │   ├── ApiService.kt
│   │   │   │   │   │   └── AuthInterceptor.kt
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── Image.kt
│   │   │   │   │   │   └── UploadResponse.kt
│   │   │   │   │   └── repository/
│   │   │   │   │       └── ImageRepository.kt
│   │   │   │   ├── viewmodel/
│   │   │   │   │   ├── LoginViewModel.kt
│   │   │   │   │   └── UploadViewModel.kt
│   │   │   │   └── GalleryApplication.kt
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── values/
│   │   │   │   └── drawable/
│   │   │   ├── AndroidManifest.xml
│   │   │   └── google-services.json
│   │   └── test/
│   └── build.gradle
├── gradle/
├── build.gradle
├── settings.gradle
└── README.md
```

## Setup

### Prerequisites

- Android Studio Hedgehog or later
- JDK 17
- Android SDK with API 34
- Firebase project with Android app configured

### Installation

1. **Open in Android Studio**
   ```bash
   cd android
   # Open in Android Studio
   ```

2. **Add google-services.json**
   - Download from Firebase Console
   - Place in `app/` directory

3. **Configure API URL**
   - Edit `app/src/main/res/values/strings.xml`
   - Set `api_base_url` to your backend URL

4. **Sync Gradle**
   - Let Android Studio sync dependencies

5. **Run**
   - Connect device or start emulator
   - Click Run button or `./gradlew installDebug`

## Configuration

### Firebase Setup

1. Create Android app in Firebase Console
2. Package name: `com.cloudgallery.portfolio`
3. Download `google-services.json`
4. Enable Authentication (Email/Password, Google)
5. Add SHA-1 fingerprint for Google Sign-In

### API Configuration

Edit `res/values/strings.xml`:
```xml
<string name="api_base_url">https://gallery-backend-xxx.run.app</string>
```

## Building

### Debug Build
```bash
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```

### Release Build
```bash
./gradlew assembleRelease
# Output: app/build/outputs/apk/release/app-release.apk
```

## Testing

```bash
# Unit tests
./gradlew test

# Instrumented tests
./gradlew connectedAndroidTest

# All tests
./gradlew check
```

## Features Detail

### Authentication

- Email/password authentication
- Google Sign-In integration
- Automatic token refresh
- Secure token storage

### Image Upload

1. Select source (Camera or Gallery)
2. Add title and description (optional)
3. Upload with progress tracking
4. View upload status

### Upload Management

- List all user uploads
- Filter by status (pending/approved/rejected)
- View upload details
- Delete uploads

## Permissions

Required permissions in AndroidManifest.xml:
- `CAMERA`: For capturing photos
- `READ_MEDIA_IMAGES`: For selecting images (Android 13+)
- `READ_EXTERNAL_STORAGE`: For selecting images (Android 12 and below)
- `INTERNET`: For API communication

## Dependencies

Key dependencies in `build.gradle`:

```gradle
// Firebase
implementation 'com.google.firebase:firebase-auth-ktx:22.3.0'
implementation 'com.google.firebase:firebase-storage-ktx:20.3.0'

// Networking
implementation 'com.squareup.retrofit2:retrofit:2.9.0'
implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
implementation 'com.squareup.okhttp3:okhttp:4.12.0'

// Image Loading
implementation 'io.coil-kt:coil:2.5.0'

// Dependency Injection
implementation 'com.google.dagger:hilt-android:2.48'
kapt 'com.google.dagger:hilt-compiler:2.48'

// Coroutines
implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'

// Lifecycle
implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.6.2'
```

## Architecture

### MVVM Pattern

- **Model**: Data classes and repository
- **View**: Activities and fragments
- **ViewModel**: Business logic and state management

### Repository Pattern

- Abstract data layer
- Single source of truth
- Handles API calls and local storage

### Dependency Injection

- Hilt for DI
- Scoped dependencies
- Testable architecture

## Security

- JWT tokens stored in encrypted SharedPreferences
- HTTPS only communication
- Certificate pinning for API
- ProGuard/R8 code obfuscation
- No API keys in source code

## UI/UX

- Material Design 3 components
- Dark mode support
- Responsive layouts
- Loading states
- Error handling
- Empty states

## Performance

- Image compression before upload
- Lazy loading for lists
- Memory-efficient bitmap handling
- Background processing with WorkManager
- Network caching

## Troubleshooting

### Firebase Authentication Issues
- Verify google-services.json is in app/
- Check Firebase Console configuration
- Ensure SHA-1 fingerprint is added for Google Sign-In

### Upload Failures
- Check network connection
- Verify API URL is correct
- Check file permissions
- Ensure backend is running

### Build Errors
- Clean project: `./gradlew clean`
- Invalidate caches: File > Invalidate Caches
- Update Android Studio and Gradle
- Check SDK versions match

## Future Enhancements

- [ ] View approved images in app
- [ ] Push notifications for approval status
- [ ] Batch upload
- [ ] Image editing before upload
- [ ] Offline support with sync
- [ ] Upload queue
- [ ] Share functionality
- [ ] User profile
- [ ] Statistics dashboard

## Contributing

This is a portfolio project. Feel free to fork and adapt for your own use.

## License

MIT License - see LICENSE file for details.
