"""
Test segmentation parameters on pre-processed cartoon image
Iterate on segmentation without regenerating the cartoon
"""
import sys
from pathlib import Path
import json

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir / 'app'))

from canvas_processor import InteractiveCanvasGenerator


def test_segmentation_variant(input_image, num_colors, min_region_size, max_size, output_suffix):
    """Test a specific set of segmentation parameters"""
    
    print(f"\n{'='*60}")
    print(f"Testing: {num_colors} colors, min region {min_region_size}px")
    print(f"{'='*60}")
    
    generator = InteractiveCanvasGenerator(
        image_path=str(input_image),
        num_colors=num_colors,
        max_size=max_size,
        min_region_size=min_region_size
    )
    
    # Process image
    generator.resize_image()
    generator.quantize_colors()
    generator.create_regions()
    canvas_data = generator.generate_canvas_data()
    
    # Save outputs
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    base_name = f"boba_{output_suffix}"
    json_path = output_dir / f"{base_name}.json"
    template_path = output_dir / f"{base_name}_template.png"
    
    # Save JSON
    with open(json_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)
    
    # Save template preview
    generator.save_template_preview(str(template_path))
    
    # Print stats
    region_sizes = [r['pixel_count'] for r in canvas_data['regions']]
    
    print(f"✅ Regions: {len(canvas_data['regions'])}")
    print(f"✅ Colors: {len(canvas_data['colors'])}")
    print(f"✅ Canvas: {canvas_data['dimensions']['width']}x{canvas_data['dimensions']['height']}")
    print(f"✅ Region sizes: min={min(region_sizes)}, max={max(region_sizes)}, avg={int(sum(region_sizes)/len(region_sizes))}")
    print(f"✅ Saved: {template_path}")
    
    return {
        'name': output_suffix,
        'regions': len(canvas_data['regions']),
        'colors': len(canvas_data['colors']),
        'min_region': min(region_sizes),
        'max_region': max(region_sizes),
        'avg_region': int(sum(region_sizes)/len(region_sizes)),
        'template': str(template_path)
    }


def main():
    """Run multiple segmentation tests with different parameters"""
    
    # Use the pre-processed cartoon image
    cartoon_image = Path("output/boba_cartoon.png")
    
    if not cartoon_image.exists():
        print(f"❌ ERROR: Cartoon image not found: {cartoon_image}")
        print(f"Run: python test_full_segmentation.py ../test-photos/boba.jpg")
        sys.exit(1)
    
    print(f"\n🎨 Testing Segmentation Variations")
    print(f"Using pre-processed image: {cartoon_image}\n")
    
    # Define test variants
    variants = [
        # (num_colors, min_region_size, max_size, suffix)
        (10, 150, 800, "simple_10c_150r"),      # Very simple - fewer colors, smaller min regions
        (15, 200, 800, "medium_15c_200r"),      # Current settings
        (20, 200, 800, "detailed_20c_200r"),    # More colors, same min region
        (15, 300, 800, "chunky_15c_300r"),      # Larger chunks
        (12, 250, 800, "balanced_12c_250r"),    # Sweet spot?
        (15, 150, 800, "fine_15c_150r"),        # More detail
    ]
    
    results = []
    
    for num_colors, min_region, max_size, suffix in variants:
        result = test_segmentation_variant(
            cartoon_image,
            num_colors,
            min_region,
            max_size,
            suffix
        )
        results.append(result)
    
    # Print comparison table
    print(f"\n{'='*80}")
    print(f"COMPARISON SUMMARY")
    print(f"{'='*80}")
    print(f"{'Variant':<25} {'Regions':<10} {'Colors':<8} {'Min':<8} {'Max':<10} {'Avg':<8}")
    print(f"{'-'*80}")
    
    for r in results:
        print(f"{r['name']:<25} {r['regions']:<10} {r['colors']:<8} {r['min_region']:<8} {r['max_region']:<10} {r['avg_region']:<8}")
    
    print(f"\n{'='*80}")
    print(f"✅ All variants generated! Check output/ folder for templates")
    print(f"{'='*80}\n")
    
    print("Recommendations:")
    print("- Fewer regions = easier/faster to color")
    print("- More regions = more detail, better likeness")
    print("- Larger min_region = bigger tap targets on mobile")
    print("- Compare the _template.png files to see which looks best!")


if __name__ == "__main__":
    main()
