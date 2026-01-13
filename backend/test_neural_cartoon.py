"""
Test neural cartoon processor on sample image
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.neural_cartoon_processor import NeuralCartoonProcessor


def test_neural_cartoon(image_path, output_dir="output"):
    """Test Gemini Nano Banana Pro cartoon conversion"""
    print(f"\n{'='*60}")
    print(f"Testing Gemini Nano Banana Pro Cartoon Processor")
    print(f"{'='*60}\n")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Test with Gemini Nano Banana Pro
    print(f"\n--- Testing gemini-3-flash-preview (Nano Banana Pro) ---\n")
    
    try:
        # Initialize processor
        processor = NeuralCartoonProcessor(
            image_path=image_path,
            model_name='gemini-3-flash-preview'
        )
        
        # Process image
        processor.process(use_neural=True)
        
        # Save result
        input_filename = Path(image_path).stem
        output_file = output_path / f"{input_filename}_gemini_nano_banana.png"
        processor.save(str(output_file))
        
        print(f"✅ SUCCESS: Saved to {output_file}\n")
        
    except Exception as e:
        print(f"❌ ERROR: {e}\n")
    
    print(f"\n{'='*60}")
    print(f"Testing complete! Check {output_dir}/ for results")
    print(f"{'='*60}\n")


def test_fallback(image_path, output_dir="output"):
    """Test fallback simple cartoon filter"""
    print(f"\n{'='*60}")
    print(f"Testing Fallback Simple Cartoon Filter")
    print(f"{'='*60}\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    try:
        processor = NeuralCartoonProcessor(image_path=image_path)
        processor.apply_simple_fallback()
        
        input_filename = Path(image_path).stem
        output_file = output_path / f"{input_filename}_fallback_cartoon.png"
        processor.save(str(output_file))
        
        print(f"✅ SUCCESS: Saved to {output_file}\n")
        
    except Exception as e:
        print(f"❌ ERROR: {e}\n")


if __name__ == "__main__":
    # Default test image
    test_image = "test-photos/boba.jpg"
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    
    if not Path(test_image).exists():
        print(f"❌ Error: Image not found: {test_image}")
        print(f"\nUsage: python test_neural_cartoon.py <image_path>")
        print(f"Example: python test_neural_cartoon.py test-photos/boba.jpg")
        sys.exit(1)
    
    print(f"\nTesting with image: {test_image}")
    
    # Test neural models
    test_neural_cartoon(test_image)
    
    # Test fallback
    test_fallback(test_image)
    
    print(f"\n🎨 All tests complete!")
