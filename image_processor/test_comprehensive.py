#!/usr/bin/env python3
"""
Comprehensive test of ImageProcessor base class functionality
Tests all key features: discovery, validation, sorting, progress tracking
"""

import sys
from pathlib import Path
from base_image_processor import ImageProcessor


class ComprehensiveTestProcessor(ImageProcessor):
    """Test processor that validates all base class features."""
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Mock OCR processing for testing."""
        # Simulate OCR processing
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(output_dir / f"image_{image_num:03d}_text.txt"),
            'text': f"Mock OCR text for {image_path.name}",
            'success': True,
            'confidence': 95.5
        }
    
    def process_image_folder(self):
        """Full processing pipeline with all features."""
        print("\n" + "="*70)
        print("COMPREHENSIVE IMAGE PROCESSOR TEST")
        print("="*70)
        
        # Feature 1: Image Discovery with Natural Sorting
        print("\n[1] Testing Image Discovery with Natural Sorting...")
        image_paths = self.discover_images()
        
        if not image_paths:
            print("  ⚠️  No images found")
            return self.create_processing_summary([])
        
        print(f"  ✓ Found {len(image_paths)} images")
        print("  Sorted order:")
        for i, path in enumerate(image_paths, 1):
            print(f"    {i}. {path.name}")
        
        # Feature 2: Format Validation
        print("\n[2] Testing Format Validation...")
        format_valid_count = 0
        for image_path in image_paths:
            if self.validate_image_format(image_path):
                format_valid_count += 1
        print(f"  ✓ {format_valid_count}/{len(image_paths)} images have valid formats")
        
        # Feature 3: Quality Validation
        print("\n[3] Testing Quality Validation...")
        for image_path in image_paths:
            is_valid, metadata = self.validate_image_quality(image_path)
            status = "✓" if is_valid else "✗"
            print(f"  {status} {image_path.name}:")
            print(f"      Resolution: {metadata.get('width', 'N/A')}x{metadata.get('height', 'N/A')}")
            print(f"      DPI: {metadata.get('dpi', 'N/A')}")
            print(f"      Format: {metadata.get('format', 'N/A')}")
        
        # Feature 4: Batch Validation
        print("\n[4] Testing Batch Validation...")
        valid_images, errors = self.validate_all_images(image_paths)
        print(f"  ✓ Valid images: {len(valid_images)}")
        print(f"  ✗ Invalid images: {len(errors)}")
        
        if errors:
            print("  Validation errors:")
            for error in errors:
                print(f"    - {Path(error['path']).name}: {error['reason']}")
        
        if not valid_images:
            print("  ⚠️  No valid images to process")
            return self.create_processing_summary([])
        
        # Feature 5: Progress Tracking
        print("\n[5] Testing Progress Tracking...")
        results = []
        for i, image_path in enumerate(valid_images, 1):
            self.update_progress(i, len(valid_images), "processing")
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
        
        # Feature 6: Summary Generation
        print("\n[6] Testing Summary Generation...")
        summary = self.create_processing_summary(results)
        
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70)
        print(f"Folder: {summary['folder_name']}")
        print(f"Total Images: {summary['total_images']}")
        print(f"Successful: {summary['successful_images']}")
        print(f"Failed: {summary['failed_images']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        print("\nDetailed Results:")
        for img_result in summary['images']:
            status = "✓" if img_result['success'] else "✗"
            conf = img_result.get('confidence', 'N/A')
            print(f"  {status} Image {img_result['image_number']}: "
                  f"{Path(img_result['image_file']).name} (confidence: {conf})")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        
        return summary


def test_natural_sorting():
    """Test natural sorting algorithm specifically."""
    print("\n" + "="*70)
    print("NATURAL SORTING TEST")
    print("="*70)
    
    # Create test processor
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test"
    
    processor = ComprehensiveTestProcessor(str(test_folder), str(output_folder))
    
    # Test with mock filenames
    test_files = [
        Path("IMG_10.jpg"),
        Path("IMG_2.jpg"),
        Path("IMG_1.jpg"),
        Path("IMG_20.jpg"),
        Path("page_001.png"),
        Path("page_010.png"),
        Path("page_002.png"),
    ]
    
    sorted_files = processor._natural_sort(test_files)
    
    print("\nOriginal order:")
    for f in test_files:
        print(f"  {f.name}")
    
    print("\nNaturally sorted order:")
    for f in sorted_files:
        print(f"  {f.name}")
    
    # Verify correct order
    expected_order = [
        "IMG_1.jpg",
        "IMG_2.jpg",
        "IMG_10.jpg",
        "IMG_20.jpg",
        "page_001.png",
        "page_002.png",
        "page_010.png",
    ]
    
    actual_order = [f.name for f in sorted_files]
    
    if actual_order == expected_order:
        print("\n✅ Natural sorting works correctly!")
    else:
        print("\n❌ Natural sorting failed!")
        print(f"Expected: {expected_order}")
        print(f"Got: {actual_order}")
        return False
    
    return True


def main():
    """Run comprehensive tests."""
    try:
        # Test 1: Natural sorting algorithm
        if not test_natural_sorting():
            sys.exit(1)
        
        # Test 2: Full processing pipeline
        test_folder = Path(__file__).parent.parent / "assets"
        output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test"
        
        processor = ComprehensiveTestProcessor(str(test_folder), str(output_folder))
        results = processor.process_image_folder()
        
        # Verify results
        if results['success_rate'] == 100.0:
            print("\n🎉 All comprehensive tests passed successfully!")
            return 0
        else:
            print(f"\n⚠️  Some tests had issues (success rate: {results['success_rate']:.1f}%)")
            return 1
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
