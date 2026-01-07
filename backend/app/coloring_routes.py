"""
Coloring API routes for paint-by-numbers functionality
"""
from flask import request, jsonify
from app import app, db
from app.models import ColoringProject, ColoringSession
from app.auth import require_auth, get_user_from_token
from app.storage import upload_image, generate_signed_url
from app.canvas_processor import InteractiveCanvasGenerator
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
import json
import threading

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image_async(project_id, image_path, num_colors, output_dir):
    """Process image asynchronously in background"""
    try:
        # Load the project
        project = ColoringProject.query.get(project_id)
        if not project:
            return
        
        # Run canvas processor
        generator = InteractiveCanvasGenerator(
            image_path=image_path,
            num_colors=num_colors,
            max_size=int(os.getenv('MAX_CANVAS_SIZE', 800)),
            min_region_size=int(os.getenv('MIN_REGION_SIZE', 50))
        )
        
        # Process the image
        generator.resize_image()
        generator.quantize_colors()
        generator.create_regions()
        canvas_data = generator.generate_canvas_data()
        
        # Save outputs
        base_name = f"{project_id}_canvas"
        json_path = os.path.join(output_dir, f"{base_name}.json")
        template_path = os.path.join(output_dir, f"{base_name}_template.png")
        
        # Save JSON
        with open(json_path, 'w') as f:
            json.dump(canvas_data, f)
        
        # Save template preview
        generator.save_template_preview(template_path)
        
        # Upload to cloud storage
        bucket_name = os.getenv('BUCKET_NAME')
        template_cloud_path = f"coloring/{project.user_id}/{base_name}_template.png"
        
        with open(template_path, 'rb') as f:
            upload_image(f, template_cloud_path)
        
        # Update project with canvas data
        project.template_data = canvas_data
        project.template_image_url = template_cloud_path
        project.status = 'completed'
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        
    except Exception as e:
        # Update project with error
        project = ColoringProject.query.get(project_id)
        if project:
            project.status = 'failed'
            project.error_message = str(e)
            project.updated_at = datetime.utcnow()
            db.session.commit()


@app.route('/api/projects/create', methods=['POST'])
@require_auth
def create_coloring_project():
    """Create a new coloring project by uploading a photo"""
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
        
        # Get parameters
        title = request.form.get('title', 'Untitled')
        num_colors = int(request.form.get('num_colors', 20))
        difficulty = request.form.get('difficulty', 'medium')
        
        # Validate num_colors
        if num_colors < 10 or num_colors > 50:
            return jsonify({'error': 'num_colors must be between 10 and 50'}), 400
        
        # Generate unique filename
        file_ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        file_name = f"{project_id}.{file_ext}"
        
        # Upload original image to cloud storage
        file_path = f"coloring/{user_id}/originals/{file_name}"
        
        try:
            # Upload to cloud (file is still a FileStorage object here)
            upload_image(file, file_path)
            
            # Save temporarily for processing
            temp_dir = os.path.join(os.getcwd(), 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, file_name)
            
            # Reset file pointer and save
            file.seek(0)
            file.save(temp_path)
            
        except Exception as e:
            return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500
        
        # Create project record
        project = ColoringProject(
            id=project_id,
            user_id=user_id,
            title=title,
            original_image_url=file_path,
            num_colors=num_colors,
            difficulty=difficulty,
            status='processing'
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Start background processing
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        thread = threading.Thread(
            target=process_image_async,
            args=(project_id, temp_path, num_colors, output_dir)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'status': 'processing',
            'message': 'Image is being processed. Check back in ~30 seconds.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<project_id>', methods=['GET'])
@require_auth
def get_coloring_project(project_id):
    """Get project details with canvas data"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        project = ColoringProject.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify(project.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
@require_auth
def get_user_projects():
    """Get user's coloring projects"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        query = ColoringProject.query.filter_by(user_id=user_id).order_by(
            ColoringProject.created_at.desc()
        )
        
        total = query.count()
        projects = query.offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'projects': [p.to_dict() for p in projects],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/coloring/session/<project_id>', methods=['POST'])
@require_auth
def get_or_create_session(project_id):
    """Get or create a coloring session for a project"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        # Check if project exists and belongs to user
        project = ColoringProject.query.filter_by(id=project_id, user_id=user_id).first()
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        if project.status != 'completed':
            return jsonify({'error': 'Project is still processing'}), 400
        
        # Check if session already exists
        session = ColoringSession.query.filter_by(
            project_id=project_id,
            user_id=user_id,
            is_completed=False
        ).first()
        
        if not session:
            # Create new session
            session = ColoringSession(
                project_id=project_id,
                user_id=user_id,
                filled_regions={}
            )
            db.session.add(session)
            db.session.commit()
        
        return jsonify(session.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/coloring/session/<session_id>', methods=['PUT'])
@require_auth
def save_coloring_session(session_id):
    """Save coloring progress"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        session = ColoringSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        data = request.get_json()
        
        # Update filled regions and completion percent
        session.filled_regions = data.get('filled_regions', {})
        session.completion_percent = data.get('completion_percent', 0)
        session.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(session.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/coloring/complete', methods=['POST'])
@require_auth
def complete_coloring_project():
    """Mark project as completed and generate final colored image"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'session_id required'}), 400
        
        session = ColoringSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Mark as completed
        session.is_completed = True
        session.completed_at = datetime.utcnow()
        session.updated_at = datetime.utcnow()
        
        # TODO: Generate final colored image from filled_regions
        # For now, just mark as complete
        # In production, you'd render the filled canvas to an image
        
        db.session.commit()
        
        return jsonify(session.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/coloring/completed', methods=['GET'])
@require_auth
def get_completed_colorings():
    """Get user's completed colorings"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        query = ColoringSession.query.filter_by(
            user_id=user_id,
            is_completed=True
        ).order_by(ColoringSession.completed_at.desc())
        
        total = query.count()
        sessions = query.offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'sessions': [s.to_dict() for s in sessions],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<project_id>', methods=['DELETE'])
@require_auth
def delete_coloring_project(project_id):
    """Delete a coloring project"""
    try:
        user = get_user_from_token()
        user_id = user['uid']
        
        project = ColoringProject.query.filter_by(id=project_id, user_id=user_id).first()
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Delete project (sessions will cascade)
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Project deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
