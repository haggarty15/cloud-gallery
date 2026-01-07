"""
Test the coloring API endpoints
Requires backend server running and Firebase authentication
"""
import requests
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8080"
TEST_IMAGE = "test-photos/boba.jpg"

# You need to get this from Firebase (see API_TESTING.md)
FIREBASE_TOKEN = ""  # TODO: Add your Firebase ID token here

def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✓ Health check passed")

def test_create_project():
    """Test project creation"""
    print("\n2. Testing project creation...")
    
    if not FIREBASE_TOKEN:
        print("   ⚠️  FIREBASE_TOKEN not set. Skipping authenticated tests.")
        print("   See API_TESTING.md for how to get a token")
        return None
    
    # Check if test image exists
    if not Path(TEST_IMAGE).exists():
        print(f"   ✗ Test image not found: {TEST_IMAGE}")
        return None
    
    headers = {"Authorization": f"Bearer {FIREBASE_TOKEN}"}
    files = {"file": open(TEST_IMAGE, "rb")}
    data = {
        "title": "Test Coloring Project",
        "num_colors": 15,
        "difficulty": "easy"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/create",
        headers=headers,
        files=files,
        data=data
    )
    
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    
    if response.status_code == 201:
        print("   ✓ Project created successfully")
        return result.get("project_id")
    else:
        print(f"   ✗ Failed to create project: {result}")
        return None

def test_get_project(project_id):
    """Test getting project details"""
    print(f"\n3. Testing get project (ID: {project_id})...")
    
    if not FIREBASE_TOKEN or not project_id:
        print("   ⚠️  Skipped (no token or project_id)")
        return None
    
    headers = {"Authorization": f"Bearer {FIREBASE_TOKEN}"}
    
    # Wait for processing
    print("   Waiting for processing to complete...")
    max_attempts = 12  # 60 seconds
    
    for attempt in range(max_attempts):
        response = requests.get(
            f"{BASE_URL}/api/projects/{project_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"   ✗ Failed to get project: {response.json()}")
            return None
        
        project = response.json()
        status = project.get("status")
        
        print(f"   Attempt {attempt + 1}/{max_attempts}: Status = {status}")
        
        if status == "completed":
            print(f"   ✓ Project processed successfully")
            print(f"   Template data keys: {list(project.get('template_data', {}).keys())}")
            
            # Show stats
            template = project.get("template_data", {})
            if template:
                print(f"   Regions: {len(template.get('regions', []))}")
                print(f"   Colors: {len(template.get('colors', []))}")
                dims = template.get("dimensions", {})
                print(f"   Dimensions: {dims.get('width')}x{dims.get('height')}")
            
            return project
        elif status == "failed":
            print(f"   ✗ Processing failed: {project.get('error_message')}")
            return None
        
        time.sleep(5)
    
    print("   ⚠️  Timeout waiting for processing")
    return None

def test_create_session(project_id):
    """Test creating a coloring session"""
    print(f"\n4. Testing session creation (project: {project_id})...")
    
    if not FIREBASE_TOKEN or not project_id:
        print("   ⚠️  Skipped")
        return None
    
    headers = {"Authorization": f"Bearer {FIREBASE_TOKEN}"}
    
    response = requests.post(
        f"{BASE_URL}/api/coloring/session/{project_id}",
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        session = response.json()
        print(f"   Response: {json.dumps(session, indent=2)}")
        print("   ✓ Session created successfully")
        return session.get("id")
    else:
        print(f"   ✗ Failed: {response.json()}")
        return None

def test_save_progress(session_id):
    """Test saving coloring progress"""
    print(f"\n5. Testing save progress (session: {session_id})...")
    
    if not FIREBASE_TOKEN or not session_id:
        print("   ⚠️  Skipped")
        return
    
    headers = {
        "Authorization": f"Bearer {FIREBASE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Simulate coloring some regions
    data = {
        "filled_regions": {
            "region_1": 3,
            "region_5": 7,
            "region_12": 3
        },
        "completion_percent": 25
    }
    
    response = requests.put(
        f"{BASE_URL}/api/coloring/session/{session_id}",
        headers=headers,
        json=data
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        session = response.json()
        print(f"   Completion: {session.get('completion_percent')}%")
        print("   ✓ Progress saved successfully")
    else:
        print(f"   ✗ Failed: {response.json()}")

def test_complete_project(session_id):
    """Test completing a coloring project"""
    print(f"\n6. Testing complete project (session: {session_id})...")
    
    if not FIREBASE_TOKEN or not session_id:
        print("   ⚠️  Skipped")
        return
    
    headers = {
        "Authorization": f"Bearer {FIREBASE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {"session_id": session_id}
    
    response = requests.post(
        f"{BASE_URL}/api/coloring/complete",
        headers=headers,
        json=data
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        session = response.json()
        print(f"   Completed: {session.get('is_completed')}")
        print("   ✓ Project marked as completed")
    else:
        print(f"   ✗ Failed: {response.json()}")

def test_list_projects():
    """Test listing user's projects"""
    print("\n7. Testing list projects...")
    
    if not FIREBASE_TOKEN:
        print("   ⚠️  Skipped")
        return
    
    headers = {"Authorization": f"Bearer {FIREBASE_TOKEN}"}
    
    response = requests.get(
        f"{BASE_URL}/api/projects?page=1&limit=10",
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Total projects: {result.get('pagination', {}).get('total')}")
        print(f"   Projects on this page: {len(result.get('projects', []))}")
        print("   ✓ List retrieved successfully")
    else:
        print(f"   ✗ Failed: {response.json()}")

def test_list_completed():
    """Test listing completed colorings"""
    print("\n8. Testing list completed colorings...")
    
    if not FIREBASE_TOKEN:
        print("   ⚠️  Skipped")
        return
    
    headers = {"Authorization": f"Bearer {FIREBASE_TOKEN}"}
    
    response = requests.get(
        f"{BASE_URL}/api/coloring/completed?page=1&limit=10",
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Total completed: {result.get('pagination', {}).get('total')}")
        print(f"   Sessions on this page: {len(result.get('sessions', []))}")
        print("   ✓ List retrieved successfully")
    else:
        print(f"   ✗ Failed: {response.json()}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("COLORING API TEST SUITE")
    print("=" * 60)
    
    if not FIREBASE_TOKEN:
        print("\n⚠️  WARNING: FIREBASE_TOKEN not set!")
        print("Edit this file and add your Firebase ID token to run full tests.")
        print("See API_TESTING.md for instructions.\n")
    
    try:
        # Test 1: Health check (no auth required)
        test_health()
        
        # Tests 2-8: Authenticated endpoints
        project_id = test_create_project()
        
        if project_id:
            project = test_get_project(project_id)
            
            if project:
                session_id = test_create_session(project_id)
                
                if session_id:
                    test_save_progress(session_id)
                    test_complete_project(session_id)
        
        test_list_projects()
        test_list_completed()
        
        print("\n" + "=" * 60)
        print("TEST SUITE COMPLETE")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to backend server")
        print("Make sure the server is running on http://localhost:8080")
        print("Run: python -m flask run --host=0.0.0.0 --port=8080")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
