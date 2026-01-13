"""
Test script for improved image segmentation with cartoon preprocessing
"""
import sys
from pathlib import Path
from app.stylized_processor import ImageStylizer
from app.canvas_processor import InteractiveCanvasGenerator
import os

def test_segmentation(image_path, num_colors=15, min_region_size=200):
    """
    Test improved segmentation with cartoon preprocessing

    Args:
        image_path: Path to test image
        num_colors: Number of colors for palette (default 15)
        min_region_size: Minimum region size in pixels (default 200)
    """
    print("=" * 70)
    print("IMPROVED SEGMENTATION TEST")
    print("=" * 70)
    print(f"Input: {image_path}")
    print(f"Colors: {num_colors}")
    print(f"Min Region Size: {min_region_size} pixels")
    print("=" * 70)
    print()

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Step 1: Apply cartoon preprocessing
    print("STEP 1: Cartoon Preprocessing")
    print("-" * 70)
    stylizer = ImageStylizer(image_path)
    stylizer.cartoon_filter()

    base_name = Path(image_path).stem
    preprocessed_path = output_dir / f"{base_name}_cartoon_preprocessed.png"
    stylizer.save_stylized(preprocessed_path)
    print()

    # Step 2: Generate canvas with improved settings
    print("STEP 2: Canvas Generation (with improved segmentation)")
    print("-" * 70)
    generator = InteractiveCanvasGenerator(
        str(preprocessed_path),
        num_colors=num_colors,
        max_size=800,
        min_region_size=min_region_size
    )

    # Process
    generator.resize_image()
    generator.quantize_colors()
    generator.create_regions()
    canvas_data = generator.generate_canvas_data()

    # Save outputs
    generator.save_json(output_dir / f"{base_name}_improved_canvas.json")
    generator.save_template_preview(output_dir / f"{base_name}_improved_template.png")
    generator.save_colored_preview(output_dir / f"{base_name}_improved_colored.png")
    generator.save_comparison(output_dir / f"{base_name}_improved_comparison.png")

    print()
    print("=" * 70)
    print("✅ SEGMENTATION TEST COMPLETE")
    print("=" * 70)
    print(f"\nOutputs saved to: {output_dir.absolute()}")
    print(f"  - Preprocessed image: {base_name}_cartoon_preprocessed.png")
    print(f"  - Canvas JSON: {base_name}_improved_canvas.json")
    print(f"  - Template: {base_name}_improved_template.png")
    print(f"  - Colored preview: {base_name}_improved_colored.png")
    print(f"  - Comparison: {base_name}_improved_comparison.png")
    print()
    print(f"Total regions: {len(canvas_data['regions'])}")
    print(f"Colors used: {num_colors}")
    print(f"Min region size: {min_region_size} pixels")
    print()

    # Region size statistics
    region_sizes = [r['pixel_count'] for r in canvas_data['regions']]
    if region_sizes:
        print("Region size statistics:")
        print(f"  - Smallest: {min(region_sizes)} pixels")
        print(f"  - Largest: {max(region_sizes)} pixels")
        print(f"  - Average: {sum(region_sizes) // len(region_sizes)} pixels")

    return canvas_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_improved_segmentation.py <image_path> [num_colors] [min_region_size]")
        print("\nExamples:")
        print("  python test_improved_segmentation.py test-photos/boba.jpg")
        print("  python test_improved_segmentation.py test-photos/boba.jpg 12 300")
        print("  python test_improved_segmentation.py test-photos/ldn.jpg 10 250")
        sys.exit(1)

    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    min_region_size = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    test_segmentation(image_path, num_colors, min_region_size)

