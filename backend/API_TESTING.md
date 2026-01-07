# Backend API Testing Guide

## Quick Start - Test the Coloring API

### 1. Start the Backend Server

```powershell
# Activate virtual environment
e:\git\cloud-gallery\backend\venv\Scripts\Activate.ps1

# Start Flask server
cd e:\git\cloud-gallery\backend
$env:FLASK_APP = "app"
python -m flask run --host=0.0.0.0 --port=8080
```

The server should start at `http://localhost:8080`

### 2. Get Firebase Auth Token

First, you need to authenticate via Firebase to get an ID token:

**Option A: Using the Web App (after upgrading Node.js)**
1. Start web app: `cd web; npm run dev`
2. Open browser, sign in
3. Open DevTools Console
4. Run: `firebase.auth().currentUser.getIdToken()`
5. Copy the token

**Option B: Using curl (test user)**
```powershell
# Create a test Firebase user via REST API
$FIREBASE_API_KEY = "AIzaSyBx0wXKdaX9HRUSTIS8tIQnfaR97IwrKi8"

# Sign up a test user
$signUpBody = @{
    email = "test@example.com"
    password = "testpass123"
    returnSecureToken = $true
} | ConvertTo-Json

$signUpResponse = Invoke-RestMethod -Uri "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=$FIREBASE_API_KEY" `
    -Method Post `
    -Body $signUpBody `
    -ContentType "application/json"

$idToken = $signUpResponse.idToken
Write-Output "Firebase ID Token: $idToken"
```

### 3. Test Upload and Project Creation

```powershell
# Upload a photo to create a coloring project
curl -X POST http://localhost:8080/api/projects/create `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" `
  -F "file=@test-photos/boba.jpg" `
  -F "title=My First Coloring" `
  -F "num_colors=20" `
  -F "difficulty=medium"

# Expected response:
# {
#   "success": true,
#   "project_id": "proj_abc123def456",
#   "status": "processing",
#   "message": "Image is being processed. Check back in ~30 seconds."
# }
```

### 4. Check Project Status

```powershell
# Get project details (replace PROJECT_ID)
curl http://localhost:8080/api/projects/proj_abc123def456 `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"

# When status is "completed", you'll get:
# {
#   "id": "proj_abc123def456",
#   "title": "My First Coloring",
#   "status": "completed",
#   "template_data": {
#     "regions": [...],
#     "colors": [...],
#     "dimensions": {"width": 800, "height": 600}
#   },
#   "original_image_url": "https://storage.googleapis.com/...",
#   "template_image_url": "https://storage.googleapis.com/...",
#   "num_colors": 20,
#   "difficulty": "medium"
# }
```

### 5. Start a Coloring Session

```powershell
# Create or get session for the project
curl -X POST http://localhost:8080/api/coloring/session/proj_abc123def456 `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"

# Response:
# {
#   "id": "session_xyz789",
#   "project_id": "proj_abc123def456",
#   "filled_regions": {},
#   "completion_percent": 0,
#   "is_completed": false
# }
```

### 6. Save Coloring Progress

```powershell
# Save which regions have been colored (replace SESSION_ID)
$saveBody = @{
    filled_regions = @{
        "region_1" = 3
        "region_2" = 5
        "region_3" = 3
    }
    completion_percent = 15
} | ConvertTo-Json

curl -X PUT http://localhost:8080/api/coloring/session/session_xyz789 `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" `
  -H "Content-Type: application/json" `
  -d $saveBody
```

### 7. Complete the Coloring

```powershell
# Mark as completed
$completeBody = @{
    session_id = "session_xyz789"
} | ConvertTo-Json

curl -X POST http://localhost:8080/api/coloring/complete `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" `
  -H "Content-Type: application/json" `
  -d $completeBody
```

### 8. List Your Projects and Completed Colorings

```powershell
# Get all projects
curl "http://localhost:8080/api/projects?page=1&limit=20" `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"

# Get completed colorings
curl "http://localhost:8080/api/coloring/completed?page=1&limit=20" `
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects/create` | Upload photo and create coloring project |
| GET | `/api/projects/<id>` | Get project details with template data |
| GET | `/api/projects` | List user's projects (paginated) |
| DELETE | `/api/projects/<id>` | Delete project |
| POST | `/api/coloring/session/<project_id>` | Get or create coloring session |
| PUT | `/api/coloring/session/<id>` | Save coloring progress |
| POST | `/api/coloring/complete` | Mark coloring as completed |
| GET | `/api/coloring/completed` | List completed colorings (paginated) |

## Authentication

All endpoints require Firebase authentication:
```
Authorization: Bearer <firebase_id_token>
```

## Error Codes

- `400` - Bad request (invalid file, parameters)
- `401` - Authentication required
- `404` - Resource not found
- `413` - File too large (>10MB)
- `500` - Internal server error

## Notes

- Processing takes ~10-30 seconds depending on image size and complexity
- Poll the GET `/api/projects/<id>` endpoint to check when processing completes
- The `template_data` JSON contains all region boundaries and colors for rendering
- Session progress auto-saves with filled_regions map (region_id -> color_num)
