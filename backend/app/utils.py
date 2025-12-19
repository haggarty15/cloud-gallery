"""
Utility functions
"""
import re
from datetime import datetime

def sanitize_input(text, max_length=255):
    """
    Sanitize user input by removing HTML tags and limiting length
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return None
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length
    return text[:max_length].strip()

def validate_pagination(page, limit, max_limit=100):
    """
    Validate and normalize pagination parameters
    
    Args:
        page: Page number
        limit: Items per page
        max_limit: Maximum allowed limit
        
    Returns:
        tuple: (page, limit)
    """
    try:
        page = max(1, int(page))
        limit = min(max(1, int(limit)), max_limit)
        return page, limit
    except (ValueError, TypeError):
        return 1, 20

def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename: Filename string
        
    Returns:
        str: File extension in lowercase
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''
