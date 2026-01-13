"""
Ultra-simplified cartoon filter for pet photos
Creates very blocky, simple regions like cartoon illustrations
"""
import cv2
import numpy as np

class PetCartoonFilter:
    """
    Specialized cartoon filter for pet photos
    Creates fewer, larger, blockier regions similar to cartoon illustrations
    """
    
    def __init__(self, image_path):
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")
        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        self.stylized = None
    
    def apply_pet_cartoon(self):
        """
        Apply ultra-aggressive cartoon filter for pet photos
        Goal: Create simple blocky regions like cartoon cat reference
        """
        print("Applying pet-optimized cartoon filter...")
        img = self.original.copy()
        
        # Step 1: Resize for processing if needed
        height, width = img.shape[:2]
        if max(height, width) > 1200:
            scale = 1200 / max(height, width)
            img = cv2.resize(img, (int(width*scale), int(height*scale)))
            print(f"   Resized: {width}x{height} -> {img.shape[1]}x{img.shape[0]}")
        
        # Step 2: AGGRESSIVE bilateral filtering (3 passes for maximum smoothing)
        print("   Bilateral filtering (3 passes)...")
        color = img.copy()
        for i in range(3):
            color = cv2.bilateralFilter(color, d=11, sigmaColor=90, sigmaSpace=90)
        
        # Step 3: Downscale and upscale to merge similar regions
        print("   Pyramid down/up for region merging...")
        h, w = color.shape[:2]
        small = cv2.pyrDown(color)
        small = cv2.pyrDown(small)  # 2 levels down
        restored = cv2.pyrUp(small)
        restored = cv2.pyrUp(restored)
        
        # Resize back to exact size
        color = cv2.resize(restored, (w, h))
        
        # Step 4: AGGRESSIVE posterization (only 4 levels = very blocky)
        print("   Aggressive posterization (4 levels)...")
        step = 256 // 4
        color = (color // step) * step
        
        # Step 5: Median blur to smooth transitions
        color = cv2.medianBlur(color, 7)
        
        # Step 6: Edge detection
        print("   Edge detection...")
        gray = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, blockSize=11, C=3)
        
        # Step 7: Combine
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        cartoon = cv2.bitwise_and(color, edges_rgb)
        
        # Resize back to original size if we scaled
        if max(height, width) > 1200:
            cartoon = cv2.resize(cartoon, (width, height))
        
        self.stylized = cartoon
        print("   ✅ Pet cartoon filter complete!")
        return self.stylized
    
    def save(self, output_path):
        """Save stylized image"""
        if self.stylized is None:
            raise ValueError("No stylized image. Call apply_pet_cartoon() first.")
        
        img_bgr = cv2.cvtColor(self.stylized, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), img_bgr)
        print(f"   Saved to {output_path}")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    if len(sys.argv) < 2:
        print("Usage: python pet_cartoon_filter.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)
    
    # Apply filter
    filter = PetCartoonFilter(image_path)
    filter.apply_pet_cartoon()
    
    # Save
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    base_name = Path(image_path).stem
    output_path = output_dir / f"{base_name}_pet_cartoon.png"
    filter.save(output_path)
    
    print(f"\n✅ Done! Saved to {output_path}")

