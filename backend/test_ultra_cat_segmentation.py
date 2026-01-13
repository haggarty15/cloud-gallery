"""
Cat-specific segmentation test v2
Ultra-optimized for simple cartoon-style regions like the reference cat image
"""
import sys
from pathlib import Path
from app.pet_cartoon_filter import PetCartoonFilter
from app.canvas_processor import InteractiveCanvasGenerator
import json

def test_cat_segmentation_v2(image_path, output_dir="output"):
    """
    Test segmentation ultra-optimized for cat photos

    Based on cartoon cat reference - creates very simple, blocky regions
    """
    print("=" * 70)
    print("CAT PHOTO SEGMENTATION TEST V2 (Ultra-Optimized)")
    print("=" * 70)
    print(f"Input: {image_path}")
    print("Goal: Match cartoon cat reference style")
    print("  - Very simple blocky shapes")
    print("  - Clear, large regions")
    print("  - 8-10 colors only")
    print("=" * 70)
    print()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Step 1: Apply ULTRA-AGGRESSIVE cartoon preprocessing
    print("STEP 1: Ultra-Aggressive Cartoon Preprocessing")
    print("-" * 70)
    filter = PetCartoonFilter(image_path)
    filter.apply_pet_cartoon()

    base_name = Path(image_path).stem
    preprocessed_path = output_path / f"{base_name}_ultra_cartoon.png"
    filter.save(preprocessed_path)
    print()

    # Step 2: Generate canvas with MINIMAL colors and LARGE regions
    print("STEP 2: Canvas Generation (Minimal Colors + Large Regions)")
    print("-" * 70)
    print("Settings:")
    print("  - Colors: 8 (ultra-simple like cartoon)")
    print("  - Min Region: 300px (very large, no tiny segments)")
    print()

    generator = InteractiveCanvasGenerator(
        str(preprocessed_path),
        num_colors=8,            # Very few colors = very simple
        max_size=800,
        min_region_size=300      # Very large minimum
    )

    # Process
    generator.resize_image()
    generator.quantize_colors()
    generator.create_regions()
    canvas_data = generator.generate_canvas_data()

    # Save outputs
    generator.save_json(output_path / f"{base_name}_ultra_canvas.json")
    generator.save_template_preview(output_path / f"{base_name}_ultra_template.png")
    generator.save_colored_preview(output_path / f"{base_name}_ultra_colored.png")
    generator.save_comparison(output_path / f"{base_name}_ultra_comparison.png")

    print()
    print("=" * 70)
    print("✅ ULTRA-OPTIMIZED CAT SEGMENTATION COMPLETE")
    print("=" * 70)
    print(f"\nOutputs:")
    print(f"  📸 Ultra-cartoon: {base_name}_ultra_cartoon.png")
    print(f"  🎨 Template: {base_name}_ultra_template.png")
    print(f"  🖍️  Colored: {base_name}_ultra_colored.png")
    print(f"  📊 Comparison: {base_name}_ultra_comparison.png")
    print()
    print(f"📊 Statistics:")
    print(f"  Total regions: {len(canvas_data['regions'])}")
    print(f"  Colors used: 8")
    print(f"  Min region threshold: 300 pixels")

    # Region statistics
    region_sizes = [r['pixel_count'] for r in canvas_data['regions']]
    if region_sizes:
        print(f"\n  Region sizes:")
        print(f"    - Smallest: {min(region_sizes)} pixels")
        print(f"    - Largest: {max(region_sizes)} pixels")
        print(f"    - Average: {sum(region_sizes) // len(region_sizes)} pixels")

        # Count by size categories
        tiny = sum(1 for s in region_sizes if s < 300)
        small = sum(1 for s in region_sizes if 300 <= s < 1000)
        medium = sum(1 for s in region_sizes if 1000 <= s < 5000)
        large = sum(1 for s in region_sizes if s >= 5000)

        print(f"\n  Size distribution:")
        print(f"    - Tiny (<300px): {tiny} regions")
        print(f"    - Small (300-1000px): {small} regions")
        print(f"    - Medium (1000-5000px): {medium} regions")
        print(f"    - Large (5000px+): {large} regions")

    print()
    print("🎯 Target: Match cartoon cat reference")
    print("  ✓ Blocky, simple shapes")
    print("  ✓ 8-15 main regions total")
    print("  ✓ Each region large and clear")
    print("  ✓ Easy to tap on mobile")

    return canvas_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_ultra_cat_segmentation.py <cat_image_path>")
        print("\nExample:")
        print("  python test_ultra_cat_segmentation.py ../test-photos/boba.jpg")
        print("\nOptimized for:")
        print("  - Simple cartoon-style regions")
        print("  - Pet photos (cats, dogs)")
        print("  - Matching cartoon reference style")
        sys.exit(1)

    image_path = sys.argv[1]

    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    test_cat_segmentation_v2(image_path)

