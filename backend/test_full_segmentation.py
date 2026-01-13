"""
Test full segmentation pipeline with Gemini-enhanced preprocessing
"""
import sys
from pathlib import Path
import os

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import without full app context
import cv2
import numpy as np
from dotenv import load_dotenv
from PIL import Image

# Load environment
load_dotenv()

# Import processors directly (avoiding app/__init__.py)
sys.path.insert(0, str(backend_dir / 'app'))
from neural_cartoon_processor import NeuralCartoonProcessor
from canvas_processor import InteractiveCanvasGenerator


def test_full_pipeline(image_path, output_dir="output"):
    """Test complete pipeline: photo → cartoon → segmentation"""
    print(f"\n{'='*60}")
    print(f"Testing Full Segmentation Pipeline")
    print(f"{'='*60}\n")
    
    input_path = Path(image_path)
    if not input_path.exists():
        print(f"❌ ERROR: Image not found: {image_path}")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Step 1: Cartoon preprocessing with Gemini-enhanced method
    print("\n--- STEP 1: Cartoon Preprocessing ---\n")
    
    processor = NeuralCartoonProcessor(
        image_path=str(input_path),
        model_name='gemini-2.5-flash'
    )
    
    # Process (will use enhanced preprocessing since Gemini doesn't return images)
    processor.process(use_neural=True)
    
    # Save cartoon version
    cartoon_path = output_path / f"{input_path.stem}_cartoon.png"
    processor.save(str(cartoon_path))
    print(f"\n✅ Saved cartoon to: {cartoon_path}")
    
    # Step 2: Generate segmented canvas
    print(f"\n--- STEP 2: Generate Segmented Canvas ---\n")
    
    generator = InteractiveCanvasGenerator(
        image_path=str(cartoon_path),  # Use the cartoon version
        num_colors=15,  # Fewer colors = simpler segments
        max_size=800,
        min_region_size=200  # Larger regions = easier to tap
    )
    
    # Process image
    generator.resize_image()
    generator.quantize_colors()
    generator.create_regions()
    canvas_data = generator.generate_canvas_data()
    
    # Save outputs
    import json
    
    json_path = output_path / f"{input_path.stem}_canvas.json"
    template_path = output_path / f"{input_path.stem}_template.png"
    
    # Save JSON
    with open(json_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)
    
    print(f"✅ Saved canvas data: {json_path}")
    
    # Save template preview
    generator.save_template_preview(str(template_path))
    print(f"✅ Saved template: {template_path}")
    
    # Print stats
    print(f"\n--- Canvas Statistics ---")
    print(f"Total regions: {len(canvas_data['regions'])}")
    print(f"Color palette: {len(canvas_data['colors'])} colors")
    print(f"Canvas size: {canvas_data['dimensions']['width']}x{canvas_data['dimensions']['height']}")
    
    # Show region sizes
    region_sizes = [r['pixel_count'] for r in canvas_data['regions']]
    print(f"Region sizes: min={min(region_sizes)}, max={max(region_sizes)}, avg={int(sum(region_sizes)/len(region_sizes))}")
    
    print(f"\n{'='*60}")
    print(f"✅ Pipeline complete! Check {output_dir}/ for results")
    print(f"{'='*60}\n")
    
    return True


if __name__ == "__main__":
    # Default test image
    test_image = "../test-photos/boba.jpg"
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    
    if not Path(test_image).exists():
        print(f"❌ Error: Image not found: {test_image}")
        print(f"\nUsage: python test_full_segmentation.py <image_path>")
        print(f"Example: python test_full_segmentation.py ../test-photos/boba.jpg")
        sys.exit(1)
    
    print(f"\nTesting with image: {test_image}")
    
    success = test_full_pipeline(test_image)
    
    if success:
        print(f"\n🎨 Full segmentation test complete!")
    else:
        print(f"\n❌ Test failed")
        sys.exit(1)
