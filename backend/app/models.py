"""
Database models
"""
from app import db
from datetime import datetime
import uuid
import json

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


class ColoringProject(db.Model):
    """Coloring project - photo converted to paint-by-numbers template"""
    __tablename__ = 'coloring_projects'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: f"proj_{uuid.uuid4().hex[:12]}")
    user_id = db.Column(db.String(128), nullable=False, index=True)
    
    title = db.Column(db.String(255))
    original_image_url = db.Column(db.String(512), nullable=False)
    template_image_url = db.Column(db.String(512))  # Preview with numbers
    
    # JSON blob containing canvas data (regions, colors, etc)
    template_data = db.Column(db.JSON)
    
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    num_colors = db.Column(db.Integer, default=20)
    
    status = db.Column(db.String(20), default='processing', index=True)  # processing, completed, failed
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to sessions
    sessions = db.relationship('ColoringSession', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        from app.storage import generate_signed_url
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'original_image_url': generate_signed_url(self.original_image_url) if self.original_image_url else None,
            'template_image_url': generate_signed_url(self.template_image_url) if self.template_image_url else None,
            'template_data': self.template_data,
            'difficulty': self.difficulty,
            'num_colors': self.num_colors,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ColoringProject {self.id} - {self.status}>'


class ColoringSession(db.Model):
    """User's coloring progress on a project"""
    __tablename__ = 'coloring_sessions'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: f"sess_{uuid.uuid4().hex[:12]}")
    project_id = db.Column(db.String(50), db.ForeignKey('coloring_projects.id'), nullable=False, index=True)
    user_id = db.Column(db.String(128), nullable=False, index=True)
    
    # JSON mapping of filled regions: {"region_1": 3, "region_5": 1}
    filled_regions = db.Column(db.JSON, default=dict)
    
    completion_percent = db.Column(db.Integer, default=0)
    colored_image_url = db.Column(db.String(512))  # Final colored result
    
    is_completed = db.Column(db.Boolean, default=False, index=True)
    
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        from app.storage import generate_signed_url
        
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'filled_regions': self.filled_regions or {},
            'completion_percent': self.completion_percent,
            'colored_image_url': generate_signed_url(self.colored_image_url) if self.colored_image_url else None,
            'is_completed': self.is_completed,
            'started_at': self.started_at.isoformat() + 'Z' if self.started_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() + 'Z' if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<ColoringSession {self.id} - {self.completion_percent}%>'

