"""
Cat-specific segmentation test
Based on cartoon cat reference with simple, blocky regions for:
- Face (distinct region)
- Eyes (separate regions)
- Ears (triangular regions)
- Body parts
- Background objects (table, chair, cushion)
"""
import sys
from pathlib import Path
from app.stylized_processor import ImageStylizer
from app.canvas_processor import InteractiveCanvasGenerator
import os

def test_cat_segmentation(image_path, output_dir="output"):
    """
    Test segmentation optimized for cat photos

    Settings based on cartoon cat reference:
    - Lower color count (10-12) for simpler, clearer regions
    - Larger min_region_size (250px) to avoid tiny whisker/fur segments
    - Cartoon filter creates blocky, easy-to-identify features
    """
    print("=" * 70)
    print("CAT PHOTO SEGMENTATION TEST")
    print("=" * 70)
    print(f"Input: {image_path}")
    print("Optimized for: Cat features (face, eyes, ears, body)")
    print("Reference: Simple cartoon cat style with clear boundaries")
    print("=" * 70)
    print()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Step 1: Apply cartoon preprocessing (extra aggressive for cat features)
    print("STEP 1: Cartoon Preprocessing (Cat-Optimized)")
    print("-" * 70)
    stylizer = ImageStylizer(image_path)

    # Use cartoon filter - creates blocky regions like reference image
    stylizer.cartoon_filter()

    base_name = Path(image_path).stem
    preprocessed_path = output_path / f"{base_name}_cat_cartoon.png"
    stylizer.save_stylized(preprocessed_path)
    print()

    # Step 2: Generate canvas with cat-optimized settings
    print("STEP 2: Canvas Generation (Cat-Optimized Settings)")
    print("-" * 70)
    print("Settings:")
    print("  - Colors: 10 (fewer = simpler cat features)")
    print("  - Min Region: 250px (avoid tiny fur/whisker segments)")
    print("  - Target: Clear face, eyes, ears, body regions")
    print()

    generator = InteractiveCanvasGenerator(
        str(preprocessed_path),
        num_colors=10,           # Lower for clearer cat features
        max_size=800,
        min_region_size=250      # Larger to avoid tiny segments
    )

    # Process
    generator.resize_image()
    generator.quantize_colors()
    generator.create_regions()
    canvas_data = generator.generate_canvas_data()

    # Save outputs
    generator.save_json(output_path / f"{base_name}_cat_canvas.json")
    generator.save_template_preview(output_path / f"{base_name}_cat_template.png")
    generator.save_colored_preview(output_path / f"{base_name}_cat_colored.png")
    generator.save_comparison(output_path / f"{base_name}_cat_comparison.png")

    print()
    print("=" * 70)
    print("✅ CAT SEGMENTATION COMPLETE")
    print("=" * 70)
    print(f"\nOutputs saved to: {output_path.absolute()}")
    print(f"  📸 Cartoon preprocessed: {base_name}_cat_cartoon.png")
    print(f"  🎨 Template: {base_name}_cat_template.png")
    print(f"  🖍️  Colored preview: {base_name}_cat_colored.png")
    print(f"  📊 Comparison: {base_name}_cat_comparison.png")
    print(f"  📄 Canvas JSON: {base_name}_cat_canvas.json")
    print()
    print(f"📊 Statistics:")
    print(f"  Total regions: {len(canvas_data['regions'])}")
    print(f"  Colors used: 10 (optimized for cat features)")
    print(f"  Min region size: 250 pixels")
    print()

    # Region size statistics
    region_sizes = [r['pixel_count'] for r in canvas_data['regions']]
    if region_sizes:
        print("  Region size breakdown:")
        print(f"    - Smallest: {min(region_sizes)} pixels")
        print(f"    - Largest: {max(region_sizes)} pixels")
        print(f"    - Average: {sum(region_sizes) // len(region_sizes)} pixels")

    print()
    print("💡 Expected regions for cat photo:")
    print("  ✓ Cat face (1-2 large regions)")
    print("  ✓ Cat eyes (2 small but clear regions)")
    print("  ✓ Cat ears (2 triangular regions)")
    print("  ✓ Cat body (1-3 regions)")
    print("  ✓ Background objects (table, chair, cushion - separate regions)")
    print()
    print("🎯 This matches the cartoon cat reference style:")
    print("  - Simple, blocky shapes")
    print("  - Clear feature boundaries")
    print("  - Easy to identify and color")
    print("  - Large enough to tap on mobile")

    return canvas_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_cat_segmentation.py <cat_image_path>")
        print("\nExample:")
        print("  python test_cat_segmentation.py ../test-photos/boba.jpg")
        print("\nOptimized for:")
        print("  - Cat photos (face, eyes, ears, body)")
        print("  - Photos with cats + background objects")
        print("  - Based on simple cartoon cat style reference")
        sys.exit(1)

    image_path = sys.argv[1]

    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    test_cat_segmentation(image_path)

