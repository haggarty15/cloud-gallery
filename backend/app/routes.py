"""
API routes and endpoints
"""
from flask import request, jsonify
from app import app, db
from app.models import Image
from app.auth import require_auth, require_admin, get_user_from_token
from app.storage import upload_image, upload_thumbnail, delete_image, get_image_metadata
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_input(text, max_length=255):
    """Sanitize user input"""
    if not text:
        return None
    # Remove any HTML tags and limit length
    import re
    text = re.sub(r'<[^>]+>', '', text)
    return text[:max_length].strip()

@app.route('/api/upload', methods=['POST'])
@require_auth
def upload():
    """Upload image endpoint"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS).upper()}'}), 400
        
        # Get user information
        user = get_user_from_token()
        user_id = user['uid']
        user_name = user.get('name', user.get('email', 'Anonymous'))
        user_email = user.get('email', '')
        
        # Get metadata from form
        title = sanitize_input(request.form.get('title', ''))
        description = sanitize_input(request.form.get('description', ''), max_length=1000)
        
        # Validate image
        try:
            metadata = get_image_metadata(file)
            
            # Check minimum dimensions
            if metadata['width'] < 200 or metadata['height'] < 200:
                return jsonify({'error': 'Image dimensions too small. Minimum 200x200 pixels'}), 400
        except Exception as e:
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400
        
        # Generate unique filename
        file_ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        image_id = f"img_{uuid.uuid4().hex[:12]}"
        file_name = f"{image_id}.{file_ext}"
        
        # Upload paths
        file_path = f"pending/{user_id}/{file_name}"
        thumbnail_path = f"pending/{user_id}/thumb_{file_name}"
        
        # Upload image and thumbnail
        try:
            upload_image(file, file_path)
            upload_thumbnail(file, thumbnail_path)
        except Exception as e:
            return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500
        
        # Create database record
        image = Image(
            id=image_id,
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            title=title,
            description=description,
            status='pending',
            file_path=file_path,
            thumbnail_path=thumbnail_path,
            mime_type=file.content_type,
            file_size=request.content_length,
            width=metadata['width'],
            height=metadata['height']
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'status': 'pending',
            'message': 'Image uploaded successfully and pending approval'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/uploads', methods=['GET'])
@require_auth
def get_user_uploads():
    """Get user's uploaded images"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        # Get query parameters
        status = request.args.get('status', None)
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Build query
        query = Image.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Get total count
        total = query.count()
        
        # Paginate
        images = query.order_by(Image.uploaded_at.desc())\
                     .offset((page - 1) * limit)\
                     .limit(limit)\
                     .all()
        
        return jsonify({
            'images': [img.to_dict(include_urls=True) for img in images],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get approved images for public gallery"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)
        sort = request.args.get('sort', 'newest')
        
        # Build query
        query = Image.query.filter_by(status='approved')
        
        # Sort
        if sort == 'oldest':
            query = query.order_by(Image.uploaded_at.asc())
        else:  # newest (default)
            query = query.order_by(Image.uploaded_at.desc())
        
        # Get total count
        total = query.count()
        
        # Paginate
        images = query.offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'images': [img.to_public_dict() for img in images],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/images/<image_id>', methods=['GET'])
def get_image(image_id):
    """Get image details"""
    try:
        image = Image.query.get(image_id)
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        # Check access permissions
        if image.status != 'approved':
            # Only owner can view pending/rejected images
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                from app.auth import verify_firebase_token
                try:
                    token = auth_header.split('Bearer ')[1]
                    user = verify_firebase_token(token)
                    if user['uid'] != image.user_id:
                        return jsonify({'error': 'Access forbidden'}), 403
                except:
                    return jsonify({'error': 'Access forbidden'}), 403
            else:
                return jsonify({'error': 'Access forbidden'}), 403
        
        return jsonify(image.to_dict(include_urls=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/images/<image_id>', methods=['DELETE'])
@require_auth
def delete_user_image(image_id):
    """Delete image"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        is_admin = user.get('admin', False)
        
        image = Image.query.get(image_id)
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        # Check permissions (owner or admin)
        if image.user_id != user_id and not is_admin:
            return jsonify({'error': 'Access forbidden'}), 403
        
        # Delete from storage
        delete_image(image.file_path)
        delete_image(image.thumbnail_path)
        
        # Delete from database
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pending', methods=['GET'])
@require_admin
def get_pending_images():
    """Get pending images for admin approval"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Query pending images
        query = Image.query.filter_by(status='pending')
        total = query.count()
        
        images = query.order_by(Image.uploaded_at.asc())\
                     .offset((page - 1) * limit)\
                     .limit(limit)\
                     .all()
        
        return jsonify({
            'images': [img.to_dict(include_urls=True) for img in images],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/approve/<image_id>', methods=['POST'])
@require_admin
def approve_image(image_id):
    """Approve an image"""
    try:
        user = get_user_from_token()
        admin_id = user['uid']
        
        image = Image.query.get(image_id)
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        if image.status == 'approved':
            return jsonify({'error': 'Image already approved'}), 400
        
        # Move files from pending to approved
        new_file_path = image.file_path.replace('pending/', 'approved/')
        new_thumbnail_path = image.thumbnail_path.replace('pending/', 'approved/')
        
        # Update in storage (copy and delete old)
        from google.cloud import storage
        bucket = storage.Client(project=os.getenv('PROJECT_ID')).bucket(os.getenv('BUCKET_NAME'))
        
        # Copy files
        bucket.copy_blob(bucket.blob(image.file_path), bucket, new_file_path)
        bucket.copy_blob(bucket.blob(image.thumbnail_path), bucket, new_thumbnail_path)
        
        # Delete old files
        delete_image(image.file_path)
        delete_image(image.thumbnail_path)
        
        # Update database
        image.status = 'approved'
        image.file_path = new_file_path
        image.thumbnail_path = new_thumbnail_path
        image.reviewed_at = datetime.utcnow()
        image.reviewed_by = admin_id
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image approved successfully',
            'image_id': image_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/reject/<image_id>', methods=['POST'])
@require_admin
def reject_image(image_id):
    """Reject an image"""
    try:
        user = get_user_from_token()
        admin_id = user['uid']
        
        image = Image.query.get(image_id)
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        # Get rejection reason
        data = request.get_json() or {}
        reason = sanitize_input(data.get('reason', ''), max_length=500)
        
        # Delete from storage
        delete_image(image.file_path)
        delete_image(image.thumbnail_path)
        
        # Update database
        image.status = 'rejected'
        image.reviewed_at = datetime.utcnow()
        image.reviewed_by = admin_id
        if reason:
            image.description = f"[REJECTED: {reason}]"
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image rejected',
            'image_id': image_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
