"""
Simple test for cartoon filter
"""
from app.stylized_processor import ImageStylizer
from pathlib import Path

image_path = "../test-photos/boba.jpg"
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

print("Loading image...")
stylizer = ImageStylizer(image_path)

print("Applying cartoon filter...")
stylizer.cartoon_filter()

print("Saving output...")
output_path = output_dir / "test_cartoon_simple.png"
stylizer.save_stylized(output_path)

print(f"✅ Done! Saved to {output_path}")

