"""
Flask application initialization and configuration
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Configure specific origins in production
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure database
if os.getenv('DB_CONNECTION_NAME'):
    # Cloud SQL connection
    from google.cloud.sql.connector import Connector
    import pg8000
    
    connector = Connector()
    
    def getconn():
        conn = connector.connect(
            os.getenv('DB_CONNECTION_NAME'),
            "pg8000",
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME')
        )
        return conn
    
    # Use creator function for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'creator': getconn
    }
else:
    # Local PostgreSQL connection
    db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Initialize database
db = SQLAlchemy(app)

# Import routes after app initialization to avoid circular imports
from app import routes, auth, storage, models

# Initialize database tables
with app.app_context():
    db.create_all()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': models.datetime.utcnow().isoformat() + 'Z'
    }), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Authentication required'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Access forbidden'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(413)
def payload_too_large(error):
    return jsonify({'error': 'File size exceeds 10MB limit'}), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
