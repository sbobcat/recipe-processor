#!/usr/bin/env python3
"""
Test the review generator with existing Kraken output
"""

import sys
from pathlib import Path

# Add the local_processor directory to path
sys.path.append('local_processor')

try:
    from kraken_sidebyside_generator import KrakenSideBySideGenerator
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure python-docx is installed: pip install python-docx")
    sys.exit(1)

def test_review_generator():
    """Test the review generator with existing Kraken output."""
    print("Testing Review Generator")
    print("=" * 30)
    
    # Check if Kraken output exists
    kraken_output_dir = Path("test-data/kraken_output")
    if not kraken_output_dir.exists():
        print("✗ Kraken output directory not found")
        return False
    
    print(f"✓ Found Kraken output directory: {kraken_output_dir}")
    
    # Check for results file
    results_file = kraken_output_dir / "processing_results.json"
    if not results_file.exists():
        print("✗ Kraken results file not found")
        return False
    
    print(f"✓ Found results file: {results_file}")
    
    try:
        # Initialize the generator
        generator = KrakenSideBySideGenerator(str(kraken_output_dir))
        print("✓ Review generator initialized")
        
        # Load results
        results = generator.load_kraken_results()
        print(f"✓ Loaded results: {results['successful_pages']}/{results['total_pages']} pages")
        
        # Check for images
        images_dir = kraken_output_dir / "page_images"
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            print(f"✓ Found {len(image_files)} page images")
        else:
            print("⚠ Page images directory not found")
        
        # Test document creation (create a test document)
        test_output = Path("validation_output/test_review_document.docx")
        test_output.parent.mkdir(exist_ok=True)
        
        print("Creating test review document...")
        doc_path = generator.create_review_document(str(test_output))
        
        if doc_path.exists():
            file_size_mb = doc_path.stat().st_size / (1024 * 1024)
            print(f"✓ Review document created successfully")
            print(f"  Path: {doc_path}")
            print(f"  Size: {file_size_mb:.2f} MB")
            return True
        else:
            print("✗ Review document was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error testing review generator: {e}")
        return False

def main():
    """Main test function."""
    success = test_review_generator()
    
    print("\n" + "=" * 30)
    if success:
        print("🎉 Review generator is working!")
    else:
        print("❌ Review generator test failed")

if __name__ == "__main__":
    main()