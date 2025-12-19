"""
Google Cloud Storage operations
"""
import os
from google.cloud import storage
from datetime import timedelta
from PIL import Image
import io

# Initialize storage client
storage_client = storage.Client(project=os.getenv('PROJECT_ID'))
bucket_name = os.getenv('BUCKET_NAME')

def get_bucket():
    """Get storage bucket"""
    return storage_client.bucket(bucket_name)

def upload_image(file, destination_path):
    """
    Upload image to Cloud Storage
    
    Args:
        file: File object to upload
        destination_path: Destination path in bucket
        
    Returns:
        str: Path to uploaded file
    """
    try:
        bucket = get_bucket()
        blob = bucket.blob(destination_path)
        
        # Upload file
        file.seek(0)
        blob.upload_from_file(file, content_type=file.content_type)
        
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
