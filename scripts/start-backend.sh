#!/bin/bash
# Start Backend Server

cd "$(dirname "$0")"
cd ..

echo "🚀 Starting Flask Backend..."
source .venv/bin/activate
cd backend
python -m flask run --host=0.0.0.0 --port=8080
