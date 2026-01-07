# Backend API

Flask API for image processing and coloring canvas generation.

## Quick Start

```powershell
# Start server
.\start-backend.ps1

# Server runs at: http://localhost:8080
```

## Test Canvas Processing

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Process image
python app/canvas_processor.py ../test-photos/boba.jpg 20
```

## Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── canvas_processor.py
│   └── image_processor.py
├── .venv/                   # Virtual environment
├── requirements.txt
└── start-backend.ps1       # Startup script
```

## API Endpoints

- `GET /` - Health check
- `POST /api/projects/create` - Upload & process image
- `GET /api/projects/:id` - Get canvas data

## Tech Stack

- Python 3.x
- Flask
- OpenCV
- NumPy

## Documentation

See [API.md](../docs/API.md) and [LOCAL_SETUP.md](LOCAL_SETUP.md) for details.

