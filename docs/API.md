# API Documentation

Backend API documentation for the Cloud Gallery Portfolio system.

## Base URL

```
Production: https://gallery-backend-xxx.run.app
Development: http://localhost:8080
```

## Authentication

Most endpoints require authentication via Firebase JWT token.

**Headers:**
```
Authorization: Bearer <firebase_id_token>
```

Get token from Firebase Auth in your client:
```javascript
const token = await firebase.auth().currentUser.getIdToken();
```

## Endpoints

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-19T18:00:00Z"
}
```

---

### Upload Image

**POST** `/api/upload`

Upload an image for approval.

**Authentication:** Required

**Headers:**
```
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Body:**
- `file`: Image file (JPEG, PNG, GIF, WebP)
- `title`: Image title (optional)
- `description`: Image description (optional)

**Request Example:**
```bash
curl -X POST https://api.example.com/api/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@image.jpg" \
  -F "title=My Photo" \
  -F "description=A beautiful sunset"
```

**Response:**
```json
{
  "success": true,
  "image_id": "img_123456",
  "status": "pending",
  "message": "Image uploaded successfully and pending approval"
}
```

**Validation:**
- Maximum file size: 10MB
- Allowed formats: JPEG, PNG, GIF, WebP
- Minimum dimensions: 200x200 pixels

**Error Responses:**
```json
// 400 - Invalid file
{
  "error": "Invalid file type. Allowed: JPEG, PNG, GIF, WebP"
}

// 400 - File too large
{
  "error": "File size exceeds 10MB limit"
}

// 401 - Unauthorized
{
  "error": "Authentication required"
}

// 413 - Payload too large
{
  "error": "File size too large"
}
```

---

### Get User Uploads

**GET** `/api/uploads`

Get list of images uploaded by the authenticated user.

**Authentication:** Required

**Query Parameters:**
- `status`: Filter by status (pending, approved, rejected) - optional
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "images": [
    {
      "id": "img_123456",
      "title": "My Photo",
      "description": "A beautiful sunset",
      "status": "pending",
      "uploaded_at": "2025-12-19T18:00:00Z",
      "thumbnail_url": "https://storage.googleapis.com/...",
      "reviewed_at": null,
      "reviewed_by": null
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "pages": 1
  }
}
```

---

### Get Public Gallery

**GET** `/api/gallery`

Get approved images for public display.

**Authentication:** Not required

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sort`: Sort order (newest, oldest, popular) - default: newest

**Response:**
```json
{
  "images": [
    {
      "id": "img_123456",
      "title": "Beautiful Sunset",
      "description": "A stunning sunset over the ocean",
      "image_url": "https://storage.googleapis.com/...",
      "thumbnail_url": "https://storage.googleapis.com/...",
      "uploaded_at": "2025-12-19T18:00:00Z",
      "uploader": {
        "name": "John Doe",
        "id": "user_789"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

### Get Image Details

**GET** `/api/images/<image_id>`

Get detailed information about a specific image.

**Authentication:** Not required for approved images, required for own pending images

**Response:**
```json
{
  "id": "img_123456",
  "title": "Beautiful Sunset",
  "description": "A stunning sunset over the ocean",
  "status": "approved",
  "image_url": "https://storage.googleapis.com/...",
  "thumbnail_url": "https://storage.googleapis.com/...",
  "uploaded_at": "2025-12-19T18:00:00Z",
  "approved_at": "2025-12-19T19:00:00Z",
  "uploader": {
    "name": "John Doe",
    "id": "user_789"
  },
  "metadata": {
    "width": 1920,
    "height": 1080,
    "format": "JPEG",
    "size_bytes": 245678
  }
}
```

---

### Admin: Get Pending Images

**GET** `/api/admin/pending`

Get list of images awaiting approval.

**Authentication:** Required (Admin only)

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "images": [
    {
      "id": "img_123456",
      "title": "Sunset Photo",
      "description": "A beautiful sunset",
      "image_url": "https://storage.googleapis.com/...",
      "thumbnail_url": "https://storage.googleapis.com/...",
      "uploaded_at": "2025-12-19T18:00:00Z",
      "uploader": {
        "name": "John Doe",
        "id": "user_789",
        "email": "john@example.com"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 15,
    "pages": 1
  }
}
```

---

### Admin: Approve Image

**POST** `/api/admin/approve/<image_id>`

Approve an image for public display.

**Authentication:** Required (Admin only)

**Response:**
```json
{
  "success": true,
  "message": "Image approved successfully",
  "image_id": "img_123456"
}
```

**Error Responses:**
```json
// 403 - Not admin
{
  "error": "Admin access required"
}

// 404 - Image not found
{
  "error": "Image not found"
}

// 400 - Already approved
{
  "error": "Image already approved"
}
```

---

### Admin: Reject Image

**POST** `/api/admin/reject/<image_id>`

Reject an image and optionally provide a reason.

**Authentication:** Required (Admin only)

**Body:**
```json
{
  "reason": "Image does not meet quality standards"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Image rejected",
  "image_id": "img_123456"
}
```

---

### Delete Image

**DELETE** `/api/images/<image_id>`

Delete an image (own images only, or admin can delete any).

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Image deleted successfully"
}
```

---

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `413` - Payload Too Large
- `500` - Internal Server Error

## Rate Limiting

- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Admin: 5000 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

## Error Format

All errors follow this format:
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional information"
  }
}
```

## Webhooks (Future)

Planned webhook support for:
- Image uploaded
- Image approved
- Image rejected

## Pagination

All paginated endpoints support:
- `page`: Page number (1-indexed)
- `limit`: Items per page (max 100)

Response includes pagination metadata:
```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

## Image URLs

Images are served via signed URLs from Cloud Storage with 1-hour expiration. Clients should refresh URLs after expiration.

## CORS

CORS is enabled for all origins in development. Production should be restricted to specific domains.

## Security

- All endpoints use HTTPS
- JWT tokens validated on each request
- Admin endpoints require custom claims
- File uploads scanned for malware (planned)
- Rate limiting prevents abuse
- Input validation on all endpoints

## SDK Examples

### JavaScript/TypeScript
```javascript
const API_BASE = 'https://api.example.com';

async function uploadImage(file, token) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/api/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return await response.json();
}
```

### Kotlin (Android)
```kotlin
val client = OkHttpClient()
val token = FirebaseAuth.getInstance().currentUser?.getIdToken(false)?.await()?.token

val requestBody = MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("file", file.name,
        RequestBody.create(MediaType.parse("image/*"), file))
    .build()

val request = Request.Builder()
    .url("$API_BASE/api/upload")
    .header("Authorization", "Bearer $token")
    .post(requestBody)
    .build()

val response = client.newCall(request).execute()
```

### Python
```python
import requests

def upload_image(file_path, token):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            'https://api.example.com/api/upload',
            files=files,
            headers=headers
        )
    return response.json()
```
