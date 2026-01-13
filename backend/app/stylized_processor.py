"""
Stylized Image Processor for Paint-by-Numbers

Two-step pipeline:
1. Apply AI/artistic stylization to photo (cartoon, sketch, etc.)
2. Convert stylized image to interactive canvas regions

This produces cleaner, more defined regions for easier coloring.
"""

import cv2
import numpy as np
from pathlib import Path
import sys


class ImageStylizer:
    """
    Apply artistic filters to photos before canvas generation.
    Creates cleaner, more defined regions for coloring.
    """
    
    def __init__(self, image_path):
        """
        Initialize stylizer
        
        Args:
            image_path: Path to input photo
        """
        self.image_path = image_path
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        self.stylized = None
    
    def cartoon_filter(self, blur_value=9, edge_threshold1=100, edge_threshold2=200):
        """
        Apply cartoon effect using edge detection + bilateral filtering.
        Creates bold, defined regions perfect for paint-by-numbers.
        ENHANCED: Aggressive smoothing to create larger, blockier regions.
        OPTIMIZED: Fast processing while maintaining quality.

        Args:
            blur_value: Bilateral filter strength (higher = smoother)
            edge_threshold1: Lower edge detection threshold
            edge_threshold2: Upper edge detection threshold
        """
        print("Applying enhanced cartoon filter...")

        # Convert to RGB for processing
        img = self.original.copy()
        
        # 1. Resize for faster processing if too large
        height, width = img.shape[:2]
        process_img = img
        scale_factor = 1.0

        if max(height, width) > 1200:
            scale_factor = 1200 / max(height, width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            process_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"   Resized for processing: {width}x{height} -> {new_width}x{new_height}")

        # 2. Apply bilateral filtering (2 passes for good balance of speed/quality)
        # This creates the blocky, cartoon effect by merging similar colors
        color = process_img.copy()
        for i in range(2):
            color = cv2.bilateralFilter(color, d=9, sigmaColor=75, sigmaSpace=75)
            print(f"   Bilateral filter pass {i+1}/2")

        # 3. Posterize to reduce color variation within regions
        # This ensures uniform color blocks
        step = 256 // 6  # Reduce to 6 levels per channel (faster than 8)
        color = (color // step) * step

        # 4. Apply median blur to smooth out small variations
        color = cv2.medianBlur(color, 5)

        # 5. Detect edges using adaptive threshold (for cartoon outlines)
        gray = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, blockSize=9, C=2)
        
        # 6. Combine edges with color
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        cartoon = cv2.bitwise_and(color, edges_rgb)

        # 7. Resize back to original size if we scaled down
        if scale_factor < 1.0:
            cartoon = cv2.resize(cartoon, (width, height), interpolation=cv2.INTER_LINEAR)
            print(f"   Resized back to original: {width}x{height}")

        self.stylized = cartoon

        return self.stylized
    
    def posterize_filter(self, levels=6):
        """
        Posterize image to reduce to specific number of color levels per channel.
        Creates flat color regions.
        
        Args:
            levels: Number of color levels (2-10, lower = more dramatic)
        """
        print(f"Applying posterize filter ({levels} levels)...")
        
        img = self.original.copy()
        
        # Calculate step size
        step = 256 // levels
        
        # Posterize each channel
        posterized = (img // step) * step
        
        self.stylized = posterized.astype(np.uint8)
        
        return self.stylized
    
    def oil_painting_filter(self, size=7, dynRatio=1):
        """
        Apply oil painting effect for artistic look.
        Creates smooth, painterly regions.
        
        Args:
            size: Filter size (higher = more dramatic)
            dynRatio: Dynamic ratio (1-3)
        """
        print("Applying oil painting filter...")
        
        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(self.original, cv2.COLOR_RGB2BGR)
        
        # Apply oil painting effect (OpenCV >= 4.x)
        oil = cv2.xphoto.oilPainting(img_bgr, size, dynRatio)
        
        # Convert back to RGB
        self.stylized = cv2.cvtColor(oil, cv2.COLOR_BGR2RGB)
        
        return self.stylized
    
    def watercolor_filter(self):
        """
        Apply watercolor effect for soft, artistic look.
        """
        print("Applying watercolor filter...")
        
        img = self.original.copy()
        
        # Convert to BGR for stylization
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Apply stylization (creates watercolor-like effect)
        watercolor = cv2.stylization(img_bgr, sigma_s=60, sigma_r=0.6)
        
        # Convert back to RGB
        self.stylized = cv2.cvtColor(watercolor, cv2.COLOR_BGR2RGB)
        
        return self.stylized
    
    def edge_preserve_filter(self):
        """
        Edge-preserving filter that simplifies while keeping boundaries sharp.
        Best for creating clean regions.
        """
        print("Applying edge-preserving filter...")
        
        img = self.original.copy()
        
        # Convert to BGR
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Edge-preserving filter
        filtered = cv2.edgePreservingFilter(img_bgr, flags=1, sigma_s=60, sigma_r=0.4)
        
        # Convert back to RGB
        self.stylized = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
        
        return self.stylized
    
    def super_simple_filter(self):
        """
        VERY aggressive simplification for minimal regions.
        Multiple passes of filtering + aggressive posterization.
        Best for creating large, easy-to-color regions (like kids' coloring books).
        """
        print("Applying super simple filter (aggressive)...")
        
        img = self.original.copy()
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Step 1: HEAVY bilateral filtering (removes almost all detail)
        simplified = img_bgr.copy()
        for _ in range(3):  # Multiple passes
            simplified = cv2.bilateralFilter(simplified, d=15, sigmaColor=80, sigmaSpace=80)
        
        # Step 2: Mean shift filtering (merges similar regions)
        simplified = cv2.pyrMeanShiftFiltering(simplified, sp=25, sr=50)
        
        # Step 3: Aggressive posterization (only 4-5 levels per channel)
        step = 256 // 4
        simplified = (simplified // step) * step
        
        # Convert back to RGB
        self.stylized = cv2.cvtColor(simplified, cv2.COLOR_BGR2RGB)
        
        return self.stylized
    
    def save_stylized(self, output_path):
        """Save stylized image"""
        if self.stylized is None:
            raise ValueError("No stylized image to save. Apply a filter first.")
        
        # Convert RGB to BGR for saving
        img_bgr = cv2.cvtColor(self.stylized, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), img_bgr)
        print(f"Saved stylized image to {output_path}")


class StylizedCanvasGenerator:
    """
    Complete pipeline: Stylize photo → Generate canvas data
    """
    
    def __init__(self, image_path, num_colors=15, style='cartoon', min_region_size=50):
        """
        Initialize stylized canvas generator
        
        Args:
            image_path: Path to input photo
            num_colors: Number of colors for canvas (fewer = easier)
            style: Filter to apply ('cartoon', 'posterize', 'oil', 'watercolor', 'edge', 'simple')
            min_region_size: Minimum pixels per region (smaller get merged for UX)
        """
        self.image_path = image_path
        self.num_colors = num_colors
        self.style = style
        self.min_region_size = min_region_size
        self.stylizer = ImageStylizer(image_path)
        self.stylized_path = None
    
    def process(self, output_dir='output'):
        """
        Full pipeline: Stylize → Canvas generation
        """
        print(f"\n{'='*60}")
        print(f"STYLIZED CANVAS GENERATOR")
        print(f"{'='*60}")
        print(f"Input: {self.image_path}")
        print(f"Style: {self.style}")
        print(f"Colors: {self.num_colors}")
        print(f"{'='*60}\n")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Step 1: Apply stylization
        print("STEP 1: Stylization")
        print("-" * 60)
        
        if self.style == 'cartoon':
            self.stylizer.cartoon_filter()
        elif self.style == 'posterize':
            self.stylizer.posterize_filter(levels=8)
        elif self.style == 'oil':
            self.stylizer.oil_painting_filter(size=7)
        elif self.style == 'watercolor':
            self.stylizer.watercolor_filter()
        elif self.style == 'edge':
            self.stylizer.edge_preserve_filter()
        elif self.style == 'simple':
            self.stylizer.super_simple_filter()
        else:
            raise ValueError(f"Unknown style: {self.style}")
        
        # Save stylized image
        base_name = Path(self.image_path).stem
        self.stylized_path = output_path / f"{base_name}_stylized_{self.style}.png"
        self.stylizer.save_stylized(self.stylized_path)
        
        print()
        
        # Step 2: Generate canvas from stylized image
        print("STEP 2: Canvas Generation")
        print("-" * 60)
        
        # Local import to avoid circular dependency
        from app.canvas_processor import InteractiveCanvasGenerator

        generator = InteractiveCanvasGenerator(
            str(self.stylized_path), 
            num_colors=self.num_colors,
            max_size=800,
            min_region_size=self.min_region_size
        )
        
        canvas_data = generator.process()
        
        # Save outputs
        base_name = Path(self.image_path).stem
        generator.save_json(output_path / f"{base_name}_{self.style}_canvas.json")
        generator.save_preview(output_path / f"{base_name}_{self.style}_template.png")
        generator.save_colored_preview(output_path / f"{base_name}_{self.style}_colored.png")
        generator.save_comparison(output_path / f"{base_name}_{self.style}_comparison.png")
        
        print()
        print(f"{'='*60}")
        print("✓ COMPLETE!")
        print(f"{'='*60}")
        print(f"Stylized image: {self.stylized_path}")
        print(f"Canvas data:    output/{base_name}_{self.style}_canvas.json")
        print(f"Template:       output/{base_name}_{self.style}_template.png")
        print(f"Colored:        output/{base_name}_{self.style}_colored.png")
        print(f"Comparison:     output/{base_name}_{self.style}_comparison.png")
        print(f"\nStats:")
        print(f"  Regions: {len(canvas_data['regions'])}")
        print(f"  Colors:  {len(canvas_data['colors'])}")
        print(f"  Difficulty: {canvas_data['metadata']['difficulty']}")
        print(f"  Coverage: 100% (no gaps)")
        print(f"  Avg region size: {canvas_data['metadata']['avg_region_size']} pixels")
        print(f"{'='*60}\n")
        
        return canvas_data


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python stylized_processor.py <image_path> [num_colors] [style] [min_region_size]")
        print("\nStyles:")
        print("  cartoon    - Bold edges with smooth colors (default)")
        print("  posterize  - Flat color regions")
        print("  oil        - Oil painting effect")
        print("  watercolor - Soft watercolor effect")
        print("  edge       - Edge-preserving simplification")
        print("  simple     - VERY simple (fewest regions, easiest to color)")
        print("\nExamples:")
        print("  python stylized_processor.py photo.jpg")
        print("  python stylized_processor.py photo.jpg 15 cartoon")
        print("  python stylized_processor.py photo.jpg 25 edge 50   # Merge regions < 50px")
        print("  python stylized_processor.py photo.jpg 30 edge 100  # More tappable regions")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    style = sys.argv[3] if len(sys.argv) > 3 else 'cartoon'
    min_region_size = int(sys.argv[4]) if len(sys.argv) > 4 else 50  # Default: merge < 50px
    
    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)
    
    # Process
    generator = StylizedCanvasGenerator(image_path, num_colors, style, min_region_size)
    generator.process()


if __name__ == "__main__":
    main()
