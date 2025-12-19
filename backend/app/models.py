"""
Database models
"""
from app import db
from datetime import datetime
import uuid

class Image(db.Model):
    """Image metadata model"""
    __tablename__ = 'images'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: f"img_{uuid.uuid4().hex[:12]}")
    user_id = db.Column(db.String(128), nullable=False, index=True)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='pending', index=True)  # pending, approved, rejected
    
    file_path = db.Column(db.String(512), nullable=False)
    thumbnail_path = db.Column(db.String(512))
    
    mime_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(128))
    
    def to_dict(self, include_urls=False):
        """Convert model to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat() + 'Z' if self.uploaded_at else None,
            'reviewed_at': self.reviewed_at.isoformat() + 'Z' if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'metadata': {
                'mime_type': self.mime_type,
                'file_size': self.file_size,
                'width': self.width,
                'height': self.height
            }
        }
        
        if include_urls:
            from app.storage import generate_signed_url
            data['image_url'] = generate_signed_url(self.file_path) if self.file_path else None
            data['thumbnail_url'] = generate_signed_url(self.thumbnail_path) if self.thumbnail_path else None
        
        return data
    
    def to_public_dict(self):
        """Convert model to public dictionary (for approved images only)"""
        if self.status != 'approved':
            return None
        
        from app.storage import generate_signed_url
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': generate_signed_url(self.file_path) if self.file_path else None,
            'thumbnail_url': generate_signed_url(self.thumbnail_path) if self.thumbnail_path else None,
            'uploaded_at': self.uploaded_at.isoformat() + 'Z' if self.uploaded_at else None,
            'uploader': {
                'name': self.user_name,
                'id': self.user_id
            }
        }
    
    def __repr__(self):
        return f'<Image {self.id} - {self.status}>'
