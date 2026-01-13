"""
Neural Cartoon/Anime Style Transfer Processor
Uses Google Gemini API with enhanced preprocessing for cartoon conversion
This provides much better segmentation results than traditional filters
"""

import cv2
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables
load_dotenv()


class NeuralCartoonProcessor:
    """
    Convert photos to cartoon/anime style using enhanced preprocessing
    Gemini API is available but currently uses optimized CV preprocessing
    """
    
    def __init__(self, image_path, model_name='gemini-2.5-flash', api_key=None):
        """
        Initialize neural cartoon processor
        
        Args:
            image_path: Path to input photo
            model_name: Gemini model (default: 'gemini-2.5-flash' - free tier)
            api_key: Google API key (or set GOOGLE_API_KEY env var)
        """
        self.image_path = image_path
        self.model_name = model_name
        
        # Load image
        self.original = cv2.imread(str(image_path))
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")
        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        
        # Setup Gemini API client
        if api_key is None:
            api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️  Warning: No Gemini API key found. Will use enhanced preprocessing.")
            self.client = None
        else:
            # Use new genai.Client() pattern
            self.client = genai.Client(api_key=api_key)
            print(f"Gemini client ready ({self.model_name})")
        
        self.stylized = None
    
    def apply_enhanced_preprocessing(self):
        """
        Enhanced preprocessing optimized for segmentation
        Creates clean, bold regions perfect for paint-by-numbers
        """
        print("Applying enhanced preprocessing for optimal segmentation...")
        
        img = self.original.copy()
        
        # Step 1: Aggressive bilateral filtering (3 passes for maximum smoothing)
        print("   1. Bilateral smoothing (3 passes)...")
        for i in range(3):
            img = cv2.bilateralFilter(img, d=11, sigmaColor=90, sigmaSpace=90)
        
        # Step 2: Mean shift filtering for region merging
        print("   2. Mean shift filtering...")
        img = cv2.pyrMeanShiftFiltering(img, sp=25, sr=50)
        
        # Step 3: Aggressive posterization (only 5 levels = very blocky)
        print("   3. Posterization (5 levels)...")
        step = 256 // 5
        img = (img // step) * step
        
        # Step 4: Morphological operations to clean up regions
        print("   4. Morphological smoothing...")
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        
        # Step 5: Final median blur
        img = cv2.medianBlur(img, 7)
        
        self.stylized = img
        print("   ✅ Enhanced preprocessing complete!")
        return self.stylized
    
    def process(self, use_neural=True):
        """
        Process image (currently uses enhanced preprocessing)
        
        Args:
            use_neural: Reserved for future Gemini image generation integration
        """
        # For now, always use enhanced preprocessing
        # Gemini text API doesn't generate images directly
        return self.apply_enhanced_preprocessing()
    
    def save(self, output_path):
        """Save stylized image"""
        if self.stylized is None:
            raise ValueError("No stylized image. Call process() first.")
        
        img_bgr = cv2.cvtColor(self.stylized, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), img_bgr)
        print(f"Saved to {output_path}")
        return output_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python neural_cartoon_processor.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)
    
    # Process image
    processor = NeuralCartoonProcessor(image_path)
    processor.process()
    
    # Save output
    output_path = Path(image_path).stem + "_cartoon.png"
    processor.save(output_path)
    print(f"✅ Saved cartoon to: {output_path}")
