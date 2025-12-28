"""
Paint by Numbers Image Processor
Converts photos into paint-by-numbers templates
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import os


class PaintByNumbersGenerator:
    """Generate paint-by-numbers templates from photos"""
    
    def __init__(self, image_path, num_colors=20, max_size=800):
        """
        Initialize generator
        
        Args:
            image_path: Path to input image
            num_colors: Number of colors to reduce to (difficulty)
            max_size: Maximum dimension for processing (pixels)
        """
        self.image_path = image_path
        self.num_colors = num_colors
        self.max_size = max_size
        
        # Load image
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        
        # Storage for processed data
        self.resized = None
        self.color_palette = None
        self.color_labels = None
        self.regions = None
        self.template = None
    
    def resize_image(self):
        """Resize image to optimal processing size"""
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
        
        print(f"Resized to: {self.resized.shape[1]}x{self.resized.shape[0]}")
        return self.resized
    
    def quantize_colors(self):
        """
        Reduce image to N colors using K-means clustering
        This determines which colors will be in the palette
        """
        print(f"Quantizing to {self.num_colors} colors...")
        
        # Reshape image to list of pixels
        pixels = self.resized.reshape(-1, 3).astype(np.float32)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=self.num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Store color palette (cluster centers)
        self.color_palette = kmeans.cluster_centers_.astype(int)
        
        # Get label for each pixel (which color it belongs to)
        labels = kmeans.predict(pixels)
        self.color_labels = labels.reshape(self.resized.shape[:2])
        
        # Create quantized image (simplified color version)
        quantized = self.color_palette[labels].reshape(self.resized.shape)
        
        print(f"Color palette: {len(self.color_palette)} colors")
        return quantized
    
    def detect_boundaries(self):
        """
        Detect boundaries between color regions
        These will become the black lines in the template
        """
        print("Detecting boundaries...")
        
        # Find edges where color labels change
        edges = np.zeros_like(self.color_labels, dtype=np.uint8)
        
        # Check horizontal boundaries
        h_diff = np.diff(self.color_labels, axis=1)
        edges[:, 1:][h_diff != 0] = 255
        
        # Check vertical boundaries
        v_diff = np.diff(self.color_labels, axis=0)
        edges[1:, :][v_diff != 0] = 255
        
        # Dilate edges slightly to make them visible
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def create_regions(self):
        """
        Segment image into connected regions
        Each region will get a number
        """
        print("Creating regions...")
        
        # Label connected components for each color
        labeled_regions = np.zeros_like(self.color_labels, dtype=np.int32)
        region_colors = []
        current_label = 1
        
        for color_idx in range(self.num_colors):
            # Get mask for this color
            mask = (self.color_labels == color_idx).astype(np.uint8)
            
            # Find connected components
            num_labels, labels = cv2.connectedComponents(mask)
            
            # Assign unique labels to each region
            for label in range(1, num_labels):  # Skip background (0)
                labeled_regions[labels == label] = current_label
                region_colors.append(color_idx)
                current_label += 1
        
        self.regions = labeled_regions
        self.region_colors = region_colors
        
        print(f"Found {len(region_colors)} regions")
        return labeled_regions
    
    def generate_template(self, add_numbers=True):
        """
        Generate the final paint-by-numbers template
        
        Args:
            add_numbers: If True, add numbers to regions
        """
        print("Generating template...")
        
        # Start with white background
        height, width = self.resized.shape[:2]
        template = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Add boundaries in black
        boundaries = self.detect_boundaries()
        template[boundaries == 255] = [0, 0, 0]
        
        if add_numbers:
            # Convert to PIL Image for text drawing
            pil_template = Image.fromarray(template)
            draw = ImageDraw.Draw(pil_template)
            
            # Try to load a font (fallback to default if not available)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
            except:
                font = ImageFont.load_default()
            
            # Add number to each region
            for region_label in range(1, len(self.region_colors) + 1):
                # Find region center
                region_mask = (self.regions == region_label)
                
                if np.any(region_mask):
                    # Get region centroid
                    y_coords, x_coords = np.where(region_mask)
                    center_y = int(np.mean(y_coords))
                    center_x = int(np.mean(x_coords))
                    
                    # Get color number (1-indexed for user)
                    color_number = self.region_colors[region_label - 1] + 1
                    
                    # Draw number (only if region is large enough)
                    if len(y_coords) > 50:  # Minimum region size
                        draw.text((center_x, center_y), str(color_number), 
                                fill=(0, 0, 0), font=font, anchor="mm")
            
            template = np.array(pil_template)
        
        self.template = template
        return template
    
    def generate_color_palette_card(self):
        """
        Generate a color reference card showing:
        Number | Color Swatch | RGB Values
        """
        print("Generating color palette card...")
        
        # Card dimensions
        card_width = 400
        swatch_size = 40
        row_height = 50
        card_height = row_height * self.num_colors + 50
        
        # Create white background
        card = np.ones((card_height, card_width, 3), dtype=np.uint8) * 255
        pil_card = Image.fromarray(card)
        draw = ImageDraw.Draw(pil_card)
        
        # Font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            font = ImageFont.load_default()
        
        # Title
        draw.text((card_width // 2, 20), "Color Palette", 
                 fill=(0, 0, 0), font=font, anchor="mm")
        
        # Each color
        for i, color in enumerate(self.color_palette):
            y = 50 + i * row_height
            
            # Number
            draw.text((30, y + row_height // 2), f"{i + 1}", 
                     fill=(0, 0, 0), font=font, anchor="mm")
            
            # Color swatch
            rgb_tuple = tuple(color.tolist())
            draw.rectangle([70, y + 5, 70 + swatch_size, y + 5 + swatch_size], 
                          fill=rgb_tuple, outline=(0, 0, 0))
            
            # RGB values
            draw.text((130, y + row_height // 2), 
                     f"RGB({color[0]}, {color[1]}, {color[2]})",
                     fill=(0, 0, 0), font=font, anchor="lm")
        
        return np.array(pil_card)
    
    def process(self):
        """
        Main processing pipeline
        Returns dict with all outputs
        """
        print(f"\n{'='*50}")
        print(f"Processing: {os.path.basename(self.image_path)}")
        print(f"Target colors: {self.num_colors}")
        print(f"{'='*50}\n")
        
        # Step 1: Resize
        resized = self.resize_image()
        
        # Step 2: Quantize colors
        quantized = self.quantize_colors()
        
        # Step 3: Create regions
        regions = self.create_regions()
        
        # Step 4: Generate template
        template = self.generate_template(add_numbers=True)
        
        # Step 5: Generate color palette card
        palette_card = self.generate_color_palette_card()
        
        print(f"\n{'='*50}")
        print("Processing complete!")
        print(f"{'='*50}\n")
        
        return {
            'original': self.original,
            'resized': resized,
            'quantized': quantized,
            'template': template,
            'palette_card': palette_card,
            'num_regions': len(self.region_colors),
            'num_colors': self.num_colors
        }
    
    def save_outputs(self, output_dir, prefix="output"):
        """Save all outputs to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save template
        template_path = os.path.join(output_dir, f"{prefix}_template.png")
        cv2.imwrite(template_path, cv2.cvtColor(self.template, cv2.COLOR_RGB2BGR))
        
        # Save palette card
        palette_path = os.path.join(output_dir, f"{prefix}_palette.png")
        palette_card = self.generate_color_palette_card()
        cv2.imwrite(palette_path, cv2.cvtColor(palette_card, cv2.COLOR_RGB2BGR))
        
        # Save quantized preview
        quantized = self.color_palette[self.color_labels].reshape(self.resized.shape)
        quantized_path = os.path.join(output_dir, f"{prefix}_preview.png")
        cv2.imwrite(quantized_path, cv2.cvtColor(quantized.astype(np.uint8), cv2.COLOR_RGB2BGR))
        
        print(f"\nSaved outputs to: {output_dir}")
        print(f"  - Template: {template_path}")
        print(f"  - Palette: {palette_path}")
        print(f"  - Preview: {quantized_path}")
        
        return {
            'template': template_path,
            'palette': palette_path,
            'preview': quantized_path
        }


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python image_processor.py <image_path> [num_colors]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    # Generate paint by numbers
    generator = PaintByNumbersGenerator(image_path, num_colors=num_colors)
    results = generator.process()
    
    # Save outputs
    generator.save_outputs("output", prefix=os.path.splitext(os.path.basename(image_path))[0])
