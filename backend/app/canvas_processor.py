"""
Interactive Paint-by-Numbers Canvas Generator

Converts photos into interactive coloring templates with:
- Region boundaries for tap-to-fill interaction
- Color palette with numbers (like Zen Color)
- JSON/SVG output for web/mobile canvas rendering
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw
import json
import sys
from pathlib import Path
from scipy import ndimage
from typing import Dict, List, Tuple


class InteractiveCanvasGenerator:
    """
    Generate interactive paint-by-numbers templates for digital coloring.
    
    Output format for web canvas:
    {
        "regions": [
            {
                "id": "region_1",
                "color_num": 3,
                "boundary": [[x1,y1], [x2,y2], ...],
                "centroid": [cx, cy],
                "filled": false
            }
        ],
        "colors": [
            {"num": 1, "rgb": [255, 120, 80], "hex": "#FF7850"}
        ],
        "dimensions": {"width": 800, "height": 600}
    }
    """
    
    def __init__(self, image_path, num_colors=20, max_size=800, min_region_size=50):
        """
        Initialize canvas generator
        
        Args:
            image_path: Path to input image
            num_colors: Number of colors (10=easy, 25=medium, 50=hard)
            max_size: Maximum dimension for canvas (pixels)
            min_region_size: Minimum pixels per region (smaller regions get merged)
        """
        self.image_path = image_path
        self.num_colors = num_colors
        self.max_size = max_size
        self.min_region_size = min_region_size
        
        # Load image
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        
        # Processed data
        self.resized = None
        self.color_palette = None
        self.color_labels = None
        self.regions_data = []
        self.canvas_data = {}
    
    def resize_image(self):
        """Resize image to optimal canvas size"""
        height, width = self.original.shape[:2]
        
        if max(height, width) > self.max_size:
            if width > height:
                new_width = self.max_size
                new_height = int(height * (self.max_size / width))
            else:
                new_height = self.max_size
                new_width = int(width * (self.max_size / height))
            
            self.resized = cv2.resize(self.original, (new_width, new_height), 
                                     interpolation=cv2.INTER_AREA)
        else:
            self.resized = self.original.copy()
        
        return self.resized
    
    def quantize_colors(self):
        """
        Reduce image to N colors using K-means clustering
        Creates the color palette for the bottom color picker
        """
        height, width = self.resized.shape[:2]
        pixels = self.resized.reshape(-1, 3).astype(np.float32)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=self.num_colors, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        
        # Store palette and labels
        self.color_palette = kmeans.cluster_centers_.astype(int)
        self.color_labels = labels.reshape(height, width)
        
        return self.color_palette, self.color_labels
    
    def create_regions(self):
        """
        Create clickable regions from color-labeled image.
        Uses connected component analysis to group adjacent pixels of same color.
        
        CRITICAL: Ensures 100% pixel coverage - no gaps or white spaces.
        """
        # First, apply morphological operations to merge small regions
        if self.min_region_size > 0:
            self.color_labels = self._simplify_labels()
        
        regions = []
        region_id = 0
        
        # Track which pixels we've already assigned
        assigned = np.zeros_like(self.color_labels, dtype=bool)
        
        height, width = self.color_labels.shape
        
        # For each color
        for color_num in range(self.num_colors):
            # Get mask of pixels with this color
            color_mask = (self.color_labels == color_num) & ~assigned
            
            # Find connected components (separate regions of same color)
            labeled_mask, num_features = ndimage.label(color_mask)
            
            # Extract each region
            for region_label in range(1, num_features + 1):
                region_mask = labeled_mask == region_label
                
                # Get region size
                region_size = np.sum(region_mask)
                if region_size == 0:
                    continue
                
                # Extract boundary coordinates
                boundary = self._extract_boundary(region_mask)
                
                # Skip if boundary extraction failed
                if not boundary:
                    continue
                
                # Calculate centroid for number placement
                coords = np.argwhere(region_mask)
                centroid = coords.mean(axis=0).astype(int).tolist()
                
                regions.append({
                    "id": f"region_{region_id}",
                    "color_num": int(color_num + 1),  # 1-indexed for display
                    "boundary": boundary,
                    "centroid": [int(centroid[1]), int(centroid[0])],  # [x, y]
                    "pixel_count": int(region_size),  # Track region size
                    "filled": False
                })
                
                region_id += 1
                assigned |= region_mask
        
        # VERIFY: Check for any unassigned pixels
        unassigned_count = np.sum(~assigned)
        if unassigned_count > 0:
            print(f"⚠️  Warning: {unassigned_count} pixels not assigned to regions!")
        else:
            print(f"✓ Complete coverage: All {height * width} pixels assigned")
        
        self.regions_data = regions
        return self.regions_data
    
    def _simplify_labels(self):
        """
        Apply morphological operations to merge small regions.
        Uses closing (dilation + erosion) to fill small holes and gaps.
        """
        print(f"🔄 Simplifying regions (min size: {self.min_region_size} pixels)...")
        
        # Calculate kernel size based on min_region_size
        # Larger min_size = larger kernel = more aggressive merging
        kernel_size = max(3, int(np.sqrt(self.min_region_size) / 2))
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # Apply morphological closing for each color separately
        simplified_labels = self.color_labels.copy()
        
        for color_num in range(self.num_colors):
            # Create binary mask for this color
            mask = (self.color_labels == color_num).astype(np.uint8)
            
            # Morphological closing: fills small holes
            closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Morphological opening: removes small regions
            opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
            
            # Update labels where opening succeeded
            simplified_labels[opened == 1] = color_num
        
        print(f"   ✓ Applied morphological simplification (kernel: {kernel_size}x{kernel_size})")
        
        return simplified_labels
    
    def _extract_boundary(self, region_mask):
        """
        Extract boundary coordinates of a region as polygon points.
        Uses OpenCV contour detection.
        """
        # Convert boolean mask to uint8
        mask_uint8 = region_mask.astype(np.uint8) * 255
        
        # Find contours
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return []
        
        # Get largest contour (main boundary)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Simplify polygon (reduce points for performance)
        epsilon = 0.005 * cv2.arcLength(largest_contour, True)
        simplified = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        # Convert to list of [x, y] coordinates
        boundary = [[int(point[0][0]), int(point[0][1])] for point in simplified]
        
        return boundary
    
    def generate_canvas_data(self):
        """
        Generate complete JSON data for interactive canvas.
        Includes regions, color palette, and metadata.
        """
        # Create color palette array
        colors = []
        for i, rgb in enumerate(self.color_palette):
            hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            colors.append({
                "num": i + 1,  # 1-indexed
                "rgb": [int(rgb[0]), int(rgb[1]), int(rgb[2])],
                "hex": hex_color
            })
        
        # Compile canvas data
        height, width = self.resized.shape[:2]
        
        # Calculate region size statistics
        region_sizes = [r['pixel_count'] for r in self.regions_data]
        avg_region_size = np.mean(region_sizes) if region_sizes else 0
        min_size = min(region_sizes) if region_sizes else 0
        max_size = max(region_sizes) if region_sizes else 0
        
        self.canvas_data = {
            "regions": self.regions_data,
            "colors": colors,
            "dimensions": {
                "width": int(width),
                "height": int(height)
            },
            "metadata": {
                "num_colors": self.num_colors,
                "num_regions": len(self.regions_data),
                "difficulty": self._get_difficulty_label(),
                "avg_region_size": int(avg_region_size),
                "min_region_size": int(min_size),
                "max_region_size": int(max_size)
            }
        }
        
        return self.canvas_data
    
    def _get_difficulty_label(self):
        """Determine difficulty based on region count"""
        num_regions = len(self.regions_data)
        if num_regions <= 200:
            return "easy"
        elif num_regions <= 800:
            return "medium"
        elif num_regions <= 2000:
            return "hard"
        else:
            return "expert"
    
    def process(self):
        """
        Full processing pipeline:
        1. Resize image
        2. Quantize colors (K-means)
        3. Create interactive regions
        4. Generate canvas JSON data
        """
        print(f"Processing {self.image_path}...")
        print(f"Target: {self.num_colors} colors")
        
        # Step 1: Resize
        print("1. Resizing image...")
        self.resize_image()
        
        # Step 2: Color quantization
        print("2. Quantizing colors...")
        self.quantize_colors()
        
        # Step 3: Create regions
        print("3. Creating regions...")
        self.create_regions()
        
        # Step 4: Generate canvas data
        print("4. Generating canvas data...")
        self.generate_canvas_data()
        
        print(f"✓ Created {len(self.regions_data)} regions with {self.num_colors} colors")
        
        return self.canvas_data
    
    def save_json(self, output_path):
        """Save canvas data as JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.canvas_data, f, indent=2)
        print(f"Saved canvas data to {output_path}")
    
    def save_preview(self, output_path):
        """
        Save visual preview of the template (outline with numbers).
        Useful for debugging and showing users what they'll color.
        """
        height, width = self.resized.shape[:2]
        preview = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(preview)
        
        # Draw region boundaries
        for region in self.regions_data:
            boundary = region['boundary']
            if len(boundary) > 2:
                # Convert to tuple format for PIL
                polygon = [(pt[0], pt[1]) for pt in boundary]
                draw.polygon(polygon, outline='black', width=1)
                
                # Draw number at centroid
                cx, cy = region['centroid']
                num = str(region['color_num'])
                # Simple text (you'd want to load a font in production)
                draw.text((cx, cy), num, fill='black', anchor='mm')
        
        preview.save(output_path)
        print(f"Saved preview to {output_path}")
    
    def save_colored_preview(self, output_path):
        """
        Save preview with colors filled in (what final result should look like).
        Uses the EXACT quantized image to ensure perfect coverage and accuracy.
        """
        height, width = self.resized.shape[:2]
        
        # Create image directly from quantized color labels
        # This ensures 100% coverage with no gaps
        colored_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Fill each pixel with its quantized color
        for y in range(height):
            for x in range(width):
                color_idx = self.color_labels[y, x]
                colored_array[y, x] = self.color_palette[color_idx]
        
        # Convert to PIL Image
        colored = Image.fromarray(colored_array)
        
        # Optionally draw region boundaries for clarity
        draw = ImageDraw.Draw(colored)
        for region in self.regions_data:
            boundary = region['boundary']
            if len(boundary) > 2:
                polygon = [(pt[0], pt[1]) for pt in boundary]
                # Very thin black outline
                draw.polygon(polygon, outline='black', width=1)
        
        colored.save(output_path)
        print(f"Saved colored preview to {output_path}")
        
    def save_comparison(self, output_path):
        """
        Save side-by-side comparison: Original | Colored
        Shows accuracy of color quantization.
        """
        height, width = self.resized.shape[:2]
        
        # Create colored version
        colored_array = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                color_idx = self.color_labels[y, x]
                colored_array[y, x] = self.color_palette[color_idx]
        
        # Create side-by-side image
        comparison = np.zeros((height, width * 2, 3), dtype=np.uint8)
        comparison[:, :width] = self.resized  # Original (resized)
        comparison[:, width:] = colored_array  # Quantized colors
        
        # Convert to PIL and save
        comparison_img = Image.fromarray(comparison)
        comparison_img.save(output_path)
        print(f"Saved comparison to {output_path}")


def main():
    """Command-line interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: python canvas_processor.py <image_path> [num_colors] [min_region_size]")
        print("\nExamples:")
        print("  python canvas_processor.py photo.jpg 20")
        print("  python canvas_processor.py photo.jpg 25 50    # Merge regions < 50 pixels")
        print("  python canvas_processor.py photo.jpg 30 100   # More aggressive merging")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    min_region_size = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # 0 = no merging
    
    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate canvas data
    generator = InteractiveCanvasGenerator(image_path, num_colors, min_region_size=min_region_size)
    canvas_data = generator.process()
    
    # Save outputs
    base_name = Path(image_path).stem
    generator.save_json(output_dir / f"{base_name}_canvas.json")
    generator.save_preview(output_dir / f"{base_name}_template.png")
    generator.save_colored_preview(output_dir / f"{base_name}_colored.png")
    generator.save_comparison(output_dir / f"{base_name}_comparison.png")
    
    print("\n✓ Processing complete!")
    print(f"  - Canvas data: output/{base_name}_canvas.json")
    print(f"  - Template preview: output/{base_name}_template.png")
    print(f"  - Colored preview: output/{base_name}_colored.png")
    print(f"  - Comparison: output/{base_name}_comparison.png")
    print(f"\nStats:")
    print(f"  - Difficulty: {canvas_data['metadata']['difficulty']}")
    print(f"  - Regions: {canvas_data['metadata']['num_regions']}")
    print(f"  - Avg region size: {canvas_data['metadata']['avg_region_size']} pixels")
    print(f"  - Min region size: {canvas_data['metadata']['min_region_size']} pixels")


if __name__ == "__main__":
    main()
