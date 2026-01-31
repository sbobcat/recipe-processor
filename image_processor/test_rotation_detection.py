#!/usr/bin/env python3
"""
Test script for rotation detection and correction functionality
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch
from base_image_processor import ImageProcessor


class TestRotationProcessor(ImageProcessor):
    """Test processor for rotation detection."""
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Test implementation."""
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(output_dir / f"image_{image_num:03d}_text.txt"),
            'text': f"Test text for {image_path.name}",
            'success': True
        }
    
    def process_image_folder(self):
        """Not used in this test."""
        pass


def test_rotation_detection_disabled():
    """Test that rotation detection can be disabled."""
    print("Test 1: Rotation Detection Disabled")
    print("-" * 60)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "rotation_test"
    
    try:
        # Create processor with auto_rotate=False
        processor = TestRotationProcessor(
            str(test_folder),
            str(output_folder),
            auto_rotate=False
        )
        
        print(f"✓ Processor created with auto_rotate=False")
        print(f"  Auto-rotate enabled: {processor.auto_rotate}")
        print(f"  Rotated dir: {processor.rotated_dir}")
        
        if not processor.auto_rotate and processor.rotated_dir is None:
            print("✓ Rotation detection properly disabled")
            return True
        else:
            print("✗ Rotation detection not properly disabled")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rotation_detection_enabled():
    """Test that rotation detection can be enabled."""
    print("\nTest 2: Rotation Detection Enabled")
    print("-" * 60)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "rotation_test"
    
    try:
        # Create processor with auto_rotate=True (default)
        processor = TestRotationProcessor(
            str(test_folder),
            str(output_folder),
            auto_rotate=True
        )
        
        print(f"✓ Processor created with auto_rotate=True")
        print(f"  Auto-rotate enabled: {processor.auto_rotate}")
        print(f"  Rotated dir: {processor.rotated_dir}")
        
        if processor.auto_rotate and processor.rotated_dir is not None:
            print("✓ Rotation detection properly enabled")
            print(f"✓ Rotated images directory created: {processor.rotated_dir}")
            return True
        else:
            print("✗ Rotation detection not properly enabled")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rotation_angles():
    """Test rotation angle mapping."""
    print("\nTest 3: Rotation Angle Mapping")
    print("-" * 60)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "rotation_test"
    
    try:
        processor = TestRotationProcessor(
            str(test_folder),
            str(output_folder)
        )
        
        print("✓ Testing rotation angle mappings:")
        
        expected_mappings = {
            0: 0,      # Correct orientation -> no rotation
            90: 270,   # Rotated 90° CW -> rotate 270° to correct
            180: 180,  # Upside down -> rotate 180° to correct
            270: 90    # Rotated 270° CW -> rotate 90° to correct
        }
        
        all_correct = True
        for detected, expected_correction in expected_mappings.items():
            actual_correction = processor.ROTATION_ANGLES.get(detected)
            status = "✓" if actual_correction == expected_correction else "✗"
            print(f"  {status} Detected {detected}° -> Correct by {actual_correction}° (expected {expected_correction}°)")
            if actual_correction != expected_correction:
                all_correct = False
        
        if all_correct:
            print("✓ All rotation angle mappings correct")
            return True
        else:
            print("✗ Some rotation angle mappings incorrect")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detect_and_correct_with_mock():
    """Test rotation detection with mocked Tesseract."""
    print("\nTest 4: Rotation Detection with Mock")
    print("-" * 60)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "rotation_test"
    
    try:
        processor = TestRotationProcessor(
            str(test_folder),
            str(output_folder),
            auto_rotate=True
        )
        
        # Get a test image
        images = processor.discover_images()
        if not images:
            print("⚠️  No images found for testing")
            return True
        
        test_image = images[0]
        
        # Mock the detect_text_orientation method
        with patch.object(processor, 'detect_text_orientation') as mock_detect:
            # Simulate detecting 90° rotation with high confidence
            mock_detect.return_value = (90, 95.0)
            
            # Mock the rotate_image method to avoid actual rotation
            with patch.object(processor, 'rotate_image') as mock_rotate:
                mock_rotate.return_value = test_image.parent / f"rotated_{test_image.name}"
                
                # Test detection and correction
                corrected_path, metadata = processor.detect_and_correct_rotation(test_image)
                
                print(f"✓ Rotation detection called")
                print(f"  Original: {test_image.name}")
                print(f"  Detected angle: {metadata['detected_angle']}°")
                print(f"  Confidence: {metadata['confidence']:.1f}%")
                print(f"  Correction applied: {metadata['correction_applied']}")
                
                if metadata['correction_applied']:
                    print(f"  Correction angle: {metadata.get('correction_angle', 'N/A')}°")
                    print(f"  Corrected path: {Path(metadata['corrected_path']).name}")
                
                # Verify mock was called
                if mock_detect.called and metadata['detected_angle'] == 90:
                    print("✓ Rotation detection working correctly")
                    return True
                else:
                    print("✗ Rotation detection not working as expected")
                    return False
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_rotation_needed():
    """Test when no rotation is needed."""
    print("\nTest 5: No Rotation Needed")
    print("-" * 60)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "rotation_test"
    
    try:
        processor = TestRotationProcessor(
            str(test_folder),
            str(output_folder),
            auto_rotate=True
        )
        
        # Get a test image
        images = processor.discover_images()
        if not images:
            print("⚠️  No images found for testing")
            return True
        
        test_image = images[0]
        
        # Mock the detect_text_orientation method
        with patch.object(processor, 'detect_text_orientation') as mock_detect:
            # Simulate detecting 0° rotation (correct orientation)
            mock_detect.return_value = (0, 99.0)
            
            # Test detection and correction
            corrected_path, metadata = processor.detect_and_correct_rotation(test_image)
            
            print(f"✓ Rotation detection called")
            print(f"  Original: {test_image.name}")
            print(f"  Detected angle: {metadata['detected_angle']}°")
            print(f"  Confidence: {metadata['confidence']:.1f}%")
            print(f"  Correction applied: {metadata['correction_applied']}")
            
            # Verify no correction was applied
            if not metadata['correction_applied'] and corrected_path == test_image:
                print("✓ No rotation applied for correctly oriented image")
                return True
            else:
                print("✗ Unexpected rotation applied")
                return False
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all rotation detection tests."""
    print("=" * 60)
    print("Rotation Detection and Correction - Test Suite")
    print("=" * 60)
    
    tests = [
        test_rotation_detection_disabled,
        test_rotation_detection_enabled,
        test_rotation_angles,
        test_detect_and_correct_with_mock,
        test_no_rotation_needed
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✅ All rotation detection tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
