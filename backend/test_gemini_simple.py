"""
Simple test of Gemini Nano Banana Pro without Flask dependencies
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Import directly without app init
import cv2
import numpy as np
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test basic Gemini API connection"""
    print("\n" + "="*60)
    print("Testing Gemini API Connection")
    print("="*60 + "\n")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: No GEMINI_API_KEY found in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Create client with new API
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client created successfully")
        
        # Test with simple text request (using a free tier model)
        print("\nTesting with simple text request...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Free tier model
            contents="Say 'hello' in one word"
        )
        
        print(f"✅ Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_with_image(image_path):
    """Test Gemini with image input"""
    print("\n" + "="*60)
    print("Testing Gemini with Image")
    print("="*60 + "\n")
    
    if not Path(image_path).exists():
        print(f"❌ ERROR: Image not found: {image_path}")
        return False
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    try:
        # Load image
        pil_image = Image.open(image_path)
        print(f"✅ Loaded image: {image_path}")
        print(f"   Size: {pil_image.size}")
        
        # Create client
        client = genai.Client(api_key=api_key)
        
        # Test with image
        print("\nSending image to Gemini...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Free tier model
            contents=["Describe this image in one sentence", pil_image]
        )
        
        print(f"✅ Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test 1: API connection
    if not test_gemini_api():
        print("\n⚠️  API connection failed. Check your GEMINI_API_KEY in .env")
        sys.exit(1)
    
    # Test 2: Image processing
    image_path = "../test-photos/boba.jpg"
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    if Path(image_path).exists():
        test_gemini_with_image(image_path)
    
    print("\n" + "="*60)
    print("✅ All tests complete!")
    print("="*60 + "\n")
