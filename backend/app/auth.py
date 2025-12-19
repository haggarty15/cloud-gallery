"""
Firebase Authentication module
"""
import os
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
from flask import request, jsonify

# Initialize Firebase Admin SDK
cred_path = os.getenv('FIREBASE_CREDENTIALS')
if cred_path and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    # Use default credentials in Cloud Run
    firebase_admin.initialize_app()

def verify_firebase_token(token):
    """
    Verify Firebase ID token
    
    Args:
        token: Firebase ID token string
        
    Returns:
        dict: Decoded token containing user information
        
    Raises:
        Exception: If token is invalid
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise Exception(f"Invalid authentication token: {str(e)}")

def require_auth(f):
    """
    Decorator to require authentication for endpoints
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split('Bearer ')[1]
        
        try:
            decoded_token = verify_firebase_token(token)
            # Add decoded token to request context
            request.user = decoded_token
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    
    return decorated_function

def require_admin(f):
    """
    Decorator to require admin access for endpoints
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check authentication
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split('Bearer ')[1]
        
        try:
            decoded_token = verify_firebase_token(token)
            
            # Check if user has admin claim
            if not decoded_token.get('admin', False):
                return jsonify({'error': 'Admin access required'}), 403
            
            # Add decoded token to request context
            request.user = decoded_token
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    
    return decorated_function

def get_user_from_token():
    """
    Get user information from request context
    
    Returns:
        dict: User information from decoded token
    """
    return getattr(request, 'user', None)
