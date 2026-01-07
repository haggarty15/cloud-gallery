"""
Simple runner script for the Flask backend
"""
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print(f"Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

