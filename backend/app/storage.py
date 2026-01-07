"""
Google Cloud Storage operations
"""
import os
from google.cloud import storage
from google.oauth2 import service_account
from datetime import timedelta
from PIL import Image
import io

# Storage client and bucket will be initialized lazily
_storage_client = None
_bucket = None

def get_storage_client():
    """Get or create storage client with service account credentials"""
    global _storage_client
    
    if _storage_client is None:
        credentials_path = os.getenv('FIREBASE_CREDENTIALS')
        
        # Convert relative path to absolute if needed
        if credentials_path and not os.path.isabs(credentials_path):
            # Assume path is relative to backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            credentials_path = os.path.join(backend_dir, credentials_path)
        
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            _storage_client = storage.Client(
                project=os.getenv('PROJECT_ID'),
                credentials=credentials
            )
        else:
            raise ValueError(
                f"Firebase credentials not found. "
                f"FIREBASE_CREDENTIALS={os.getenv('FIREBASE_CREDENTIALS')}, "
                f"Resolved path={credentials_path}, "
                f"Exists={os.path.exists(credentials_path) if credentials_path else False}"
            )
    
    return _storage_client

def get_bucket():
    """Get storage bucket"""
    global _bucket
    
    if _bucket is None:
        bucket_name = os.getenv('BUCKET_NAME')
        if not bucket_name:
            raise ValueError("BUCKET_NAME environment variable not set")
        
        client = get_storage_client()
        _bucket = client.bucket(bucket_name)
    
    return _bucket

def upload_image(file, destination_path):
    """
    Upload image to Cloud Storage
    
    Args:
        file: File object to upload (FileStorage or file-like object)
        destination_path: Destination path in bucket
        
    Returns:
        str: Path to uploaded file
    """
    try:
        bucket = get_bucket()
        blob = bucket.blob(destination_path)
        
        # Upload file
        file.seek(0)
        
        # Check if it's a FileStorage object (has content_type)
        content_type = getattr(file, 'content_type', 'image/jpeg')
        
        blob.upload_from_file(file, content_type=content_type)
        
        return destination_path
    except Exception as e:
        raise Exception(f"Failed to upload image: {str(e)}")

def create_thumbnail(image_file, max_size=(300, 300)):
    """
    Create thumbnail from image
    
    Args:
        image_file: Image file object
        max_size: Maximum dimensions for thumbnail
        
    Returns:
        BytesIO: Thumbnail image data
    """
    try:
        image_file.seek(0)
        img = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Create thumbnail
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise Exception(f"Failed to create thumbnail: {str(e)}")

def upload_thumbnail(image_file, destination_path):
    """
    Create and upload thumbnail
    
    Args:
        image_file: Original image file
        destination_path: Destination path for thumbnail
        
    Returns:
        str: Path to uploaded thumbnail
    """
    try:
        thumbnail = create_thumbnail(image_file)
        
        bucket = get_bucket()
        blob = bucket.blob(destination_path)
        blob.upload_from_file(thumbnail, content_type='image/jpeg')
        
        return destination_path
    except Exception as e:
        raise Exception(f"Failed to upload thumbnail: {str(e)}")

def generate_signed_url(blob_path, expiration=3600):
    """
    Generate signed URL for blob access
    
    Args:
        blob_path: Path to blob in bucket
        expiration: URL expiration time in seconds (default 1 hour)
        
    Returns:
        str: Signed URL
    """
    try:
        if not blob_path:
            return None
        
        bucket = get_bucket()
        blob = bucket.blob(blob_path)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=expiration),
            method="GET"
        )
        
        return url
    except Exception as e:
        print(f"Failed to generate signed URL: {str(e)}")
        return None

def delete_image(blob_path):
    """
    Delete image from Cloud Storage
    
    Args:
        blob_path: Path to blob in bucket
    """
    try:
        bucket = get_bucket()
        blob = bucket.blob(blob_path)
        blob.delete()
    except Exception as e:
        print(f"Failed to delete image: {str(e)}")

def get_image_metadata(image_file):
    """
    Get image metadata (dimensions, format, size)
    
    Args:
        image_file: Image file object
        
    Returns:
        dict: Image metadata
    """
    try:
        image_file.seek(0)
        img = Image.open(image_file)
        
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode
        }
    except Exception as e:
        raise Exception(f"Failed to get image metadata: {str(e)}")
