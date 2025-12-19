# Security Documentation

Security practices and considerations for the Cloud Gallery Portfolio system.

## Overview

This document outlines the security architecture, best practices, and implementation details for securing the cloud gallery system.

## Authentication & Authorization

### Firebase Authentication

**Implementation:**
- Firebase Identity Platform for user authentication
- Support for Email/Password and Google Sign-In
- JWT tokens for API authentication

**Security Measures:**
- Tokens expire after 1 hour
- Refresh tokens stored securely on client
- Token validation on every API request
- Custom claims for role-based access

**Admin Access:**
```javascript
// Setting admin claim (via Firebase Admin SDK)
admin.auth().setCustomUserClaims(uid, { admin: true });
```

### API Authentication

**Token Validation:**
```python
from firebase_admin import auth

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise Unauthorized("Invalid token")
```

**Authorization Checks:**
- Regular users: Can upload and view own images
- Admin users: Can approve/reject images, view all uploads
- Public: Can view approved images only

## Data Security

### Cloud Storage

**Bucket Configuration:**
- Private bucket (no public access)
- Signed URLs for temporary access (1-hour expiration)
- CORS configured for specific origins only
- Lifecycle policies to delete old pending images

**Access Control:**
```bash
# Service account has objectAdmin role
# Users never directly access bucket
# All access through backend API with signed URLs
```

**Best Practices:**
- Never expose bucket directly to clients
- Use signed URLs with short expiration
- Separate folders for pending/approved images
- Regular audit of bucket permissions

### Cloud SQL

**Database Security:**
- Private IP configuration (no public access)
- SSL/TLS enforced for connections
- Strong passwords stored in Secret Manager
- Automated backups enabled

**Connection Security:**
```python
# Unix socket connection via Cloud SQL Proxy
connector = Connector()
conn = connector.connect(
    "project:region:instance",
    "pg8000",
    user="postgres",
    password=os.environ["DB_PASSWORD"],
    db="gallery"
)
```

**Data Protection:**
- User passwords never stored (Firebase handles auth)
- Sensitive data encrypted at rest (GCP default)
- No PII stored in logs
- Regular database backups

## Network Security

### Cloud Run Security

**Service Configuration:**
- HTTPS only (HTTP redirects to HTTPS)
- IAM-based access control
- VPC connector for private resources
- Service-to-service authentication

**Environment Variables:**
- Sensitive values in Secret Manager
- No secrets in container images
- Runtime injection of credentials
- Automatic secret rotation support

**Ingress Control:**
```bash
# Allow public access for public endpoints
gcloud run services update gallery-backend \
  --ingress=all \
  --allow-unauthenticated

# Restrict to VPC for internal services
gcloud run services update internal-service \
  --ingress=internal \
  --no-allow-unauthenticated
```

### API Security

**Rate Limiting:**
- Anonymous: 100 req/hour
- Authenticated: 1000 req/hour
- Admin: 5000 req/hour
- Per-IP rate limiting to prevent abuse

**Input Validation:**
```python
# File upload validation
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MIN_DIMENSIONS = (200, 200)

def validate_image(file):
    # Check file size
    if file.content_length > MAX_FILE_SIZE:
        raise ValidationError("File too large")
    
    # Check file type
    if not allowed_file(file.filename):
        raise ValidationError("Invalid file type")
    
    # Check image dimensions
    img = Image.open(file)
    if img.size[0] < MIN_DIMENSIONS[0] or img.size[1] < MIN_DIMENSIONS[1]:
        raise ValidationError("Image too small")
```

**CORS Configuration:**
```json
{
  "origin": ["https://gallery.example.com"],
  "method": ["GET", "POST", "PUT", "DELETE"],
  "responseHeader": ["Content-Type", "Authorization"],
  "maxAgeSeconds": 3600
}
```

## Application Security

### Input Sanitization

**Backend:**
```python
from bleach import clean

def sanitize_input(text):
    # Remove HTML tags and dangerous content
    return clean(text, tags=[], strip=True)

# Usage
title = sanitize_input(request.form.get('title', ''))
description = sanitize_input(request.form.get('description', ''))
```

**Frontend:**
```javascript
import DOMPurify from 'dompurify';

// Sanitize before rendering
const cleanDescription = DOMPurify.sanitize(description);
```

### SQL Injection Prevention

**Use Parameterized Queries:**
```python
# Good - parameterized query
cursor.execute(
    "SELECT * FROM images WHERE user_id = %s AND status = %s",
    (user_id, status)
)

# Bad - string concatenation (DON'T DO THIS)
# cursor.execute(f"SELECT * FROM images WHERE user_id = '{user_id}'")
```

**ORM Usage:**
```python
# Using SQLAlchemy ORM prevents SQL injection
images = db.session.query(Image)\
    .filter(Image.user_id == user_id)\
    .filter(Image.status == 'approved')\
    .all()
```

### XSS Prevention

**Content Security Policy:**
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://apis.google.com;
               style-src 'self' 'unsafe-inline';
               img-src 'self' https://storage.googleapis.com;
               connect-src 'self' https://*.run.app">
```

**React Built-in Protection:**
```javascript
// React automatically escapes values
<div>{userInput}</div>  // Safe

// Dangerous HTML rendering (avoid)
<div dangerouslySetInnerHTML={{__html: userInput}} />  // Unsafe
```

### Android Security

**API Key Protection:**
```kotlin
// Use BuildConfig for sensitive values
val apiKey = BuildConfig.FIREBASE_API_KEY

// Never hardcode in source
// val apiKey = "AIza..." // DON'T DO THIS
```

**Network Security Config:**
```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
    <domain-config>
        <domain includeSubdomains="true">run.app</domain>
        <pin-set>
            <pin digest="SHA-256">base64-encoded-pin</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

**ProGuard Configuration:**
```
# Keep Firebase classes
-keep class com.google.firebase.** { *; }
-keep class com.google.android.gms.** { *; }

# Obfuscate application code
-repackageclasses 'o'
-allowaccessmodification
```

## IAM & Permissions

### Service Account Roles

**Backend Service Account:**
```bash
# Minimum required permissions
roles/cloudsql.client          # Database access
roles/storage.objectAdmin      # Storage access
roles/firebase.admin           # Firebase auth verification
```

**Principle of Least Privilege:**
- Grant only necessary permissions
- Use separate service accounts per service
- Regular audit of permissions
- Remove unused service accounts

### User Roles

**Role Definitions:**
1. **Anonymous**: View approved images only
2. **Authenticated User**: Upload images, view own uploads
3. **Admin**: Approve/reject images, view all uploads

**Custom Claims:**
```javascript
// Set admin role
await admin.auth().setCustomUserClaims(uid, {
  admin: true,
  role: 'admin'
});

// Verify admin in backend
def require_admin(decoded_token):
    if not decoded_token.get('admin'):
        raise Forbidden("Admin access required")
```

## Secrets Management

### Google Secret Manager

**Create Secrets:**
```bash
# Database password
echo -n "secure-password" | gcloud secrets create db-password \
    --data-file=- \
    --replication-policy="automatic"

# Firebase credentials
gcloud secrets create firebase-key \
    --data-file=service-account-key.json \
    --replication-policy="automatic"
```

**Access in Cloud Run:**
```bash
gcloud run services update gallery-backend \
    --set-secrets=DB_PASSWORD=db-password:latest \
    --set-secrets=FIREBASE_CREDENTIALS=firebase-key:latest
```

**Best Practices:**
- Never commit secrets to git
- Use Secret Manager for all sensitive values
- Rotate secrets regularly
- Audit secret access logs

## Monitoring & Logging

### Security Logging

**Log Important Events:**
```python
import logging

# Authentication events
logging.info(f"User login: {user_id}")
logging.warning(f"Failed login attempt: {ip_address}")

# Authorization events
logging.warning(f"Unauthorized access attempt: {user_id} to {resource}")

# Data access
logging.info(f"Image uploaded: {image_id} by {user_id}")
logging.info(f"Image approved: {image_id} by {admin_id}")
```

**Don't Log Sensitive Data:**
```python
# Good
logging.info(f"User {user_id} updated profile")

# Bad - contains sensitive data
# logging.info(f"User {email} password changed to {new_password}")
```

### Cloud Monitoring

**Set Up Alerts:**
```bash
# Alert on high error rate
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="High Error Rate" \
    --condition-display-name="Error rate > 5%" \
    --condition-threshold-value=0.05
```

**Monitor for:**
- Failed authentication attempts
- Unauthorized access attempts
- Unusual upload patterns
- API errors and exceptions
- Database connection failures

## Compliance & Privacy

### Data Retention

**Policies:**
- Pending images: 90 days
- Approved images: Indefinite (until user deletes)
- Rejected images: Deleted immediately
- User data: Deleted on account deletion

**Implementation:**
```bash
# Storage lifecycle policy
gsutil lifecycle set lifecycle.json gs://bucket-name
```

### GDPR Compliance

**User Rights:**
- Right to access data
- Right to delete data
- Right to data portability
- Right to be forgotten

**Implementation:**
```python
@app.route('/api/user/data', methods=['GET'])
@require_auth
def export_user_data(user_id):
    # Return all user data in JSON format
    return jsonify(get_all_user_data(user_id))

@app.route('/api/user/delete', methods=['DELETE'])
@require_auth
def delete_user_account(user_id):
    # Delete all user data
    delete_user_images(user_id)
    delete_user_metadata(user_id)
    auth.delete_user(user_id)
    return jsonify({"success": true})
```

## Security Checklist

### Development
- [ ] No secrets in source code
- [ ] Input validation on all endpoints
- [ ] Output encoding for user content
- [ ] Parameterized SQL queries
- [ ] Dependency vulnerability scanning

### Deployment
- [ ] HTTPS enforced
- [ ] Secrets in Secret Manager
- [ ] Service accounts with minimal permissions
- [ ] Private database instance
- [ ] CORS properly configured
- [ ] Rate limiting enabled

### Operations
- [ ] Logging enabled for security events
- [ ] Monitoring alerts configured
- [ ] Regular security audits
- [ ] Backup strategy implemented
- [ ] Incident response plan

### Compliance
- [ ] Data retention policies
- [ ] User data export capability
- [ ] Account deletion capability
- [ ] Privacy policy published
- [ ] Terms of service published

## Incident Response

### Security Incident Process

1. **Detection**: Monitor logs and alerts
2. **Analysis**: Investigate the incident
3. **Containment**: Limit the damage
4. **Eradication**: Remove the threat
5. **Recovery**: Restore services
6. **Post-mortem**: Document and learn

### Contact Information

- Security Team: security@example.com
- On-call: +1-XXX-XXX-XXXX
- GCP Support: GCP Console

## Regular Security Tasks

### Daily
- Monitor security alerts
- Review error logs

### Weekly
- Review authentication logs
- Check for failed login attempts
- Audit admin actions

### Monthly
- Update dependencies
- Review IAM permissions
- Test backup restoration
- Security audit

### Quarterly
- Penetration testing
- Security training
- Review and update policies
- Rotate service account keys

## Resources

- [GCP Security Best Practices](https://cloud.google.com/security/best-practices)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Cloud Run Security](https://cloud.google.com/run/docs/securing)
