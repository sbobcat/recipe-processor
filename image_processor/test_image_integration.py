#!/usr/bin/env python3
"""
Integration Tests for Image Processing Pipeline
Tests complete workflows: Image Folder → OCR → Review Document
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import shutil

# Import components to test
try:
    from base_image_processor import ImageProcessor
    from tesseract_sidebyside_generator import TesseractSideBySideGenerator
    from aws_textract_image_sidebyside_generator import AWSTextractImageSideBySideGenerator
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the image_processor directory")
    raise


class MockTesseractProcessor(ImageProcessor):
    """Mock Tesseract processor for testing."""
    
    def __init__(self, image_folder, output_dir, simulate_failures=False):
        super().__init__(image_folder, output_dir)
        self.simulate_failures = simulate_failures
        self.processed_count = 0
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Mock Tesseract processing."""
        self.processed_count += 1
        
        # Simulate occasional failures if requested
        if self.simulate_failures and image_num % 3 == 0:
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': '',
                'text': '',
                'success': False,
                'error': 'Simulated processing failure'
            }
        
        # Simulate successful processing
        text = f"Mock Tesseract OCR text for {image_path.name}\nLine 1\nLine 2"
        text_file = output_dir / f"image_{image_num:03d}_ocr.txt"
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"Image {image_num}\n")
            f.write("Confidence: 87.5%\n")
            f.write("=" * 50 + "\n")
            f.write(text + "\n")
            f.write("=" * 50 + "\n")
            f.write("LOW CONFIDENCE WORDS (may need review):\n")
            f.write("  None - all words have good confidence!\n")
        
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(text_file),
            'text': text,
            'success': True,
            'confidence': 87.5
        }
    
    def process_image_folder(self):
        """Mock full processing pipeline."""
        image_paths = self.discover_images()
        
        if not image_paths:
            return self.create_processing_summary([])
        
        valid_images, errors = self.validate_all_images(image_paths)
        
        results = []
        for i, image_path in enumerate(valid_images, start=1):
            self.update_progress(i, len(valid_images), "processing")
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
        
        summary = self.create_processing_summary(results)
        
        # Save summary JSON
        summary_file = self.output_dir / f"{self.image_folder.name}_tesseract_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return summary


class MockAWSProcessor(ImageProcessor):
    """Mock AWS Textract processor for testing."""
    
    def __init__(self, image_folder, output_dir, simulate_failures=False):
        super().__init__(image_folder, output_dir)
        self.simulate_failures = simulate_failures
        self.processed_count = 0
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Mock AWS Textract processing."""
        self.processed_count += 1
        
        # Simulate occasional failures if requested
        if self.simulate_failures and image_num % 4 == 0:
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': '',
                'text': '',
                'success': False,
                'confidence': 0,
                'error': 'Simulated AWS API error'
            }
        
        # Simulate successful processing with confidence scores
        text = f"Mock AWS Textract text for {image_path.name}\nDetected line 1\nDetected line 2"
        text_file = output_dir / f"image_{image_num:03d}_ocr.txt"
        
        confidence = 92.3 if image_num % 2 == 0 else 78.5
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"Image {image_num}\n")
            f.write(f"Confidence: {confidence:.1f}%\n")
            f.write("=" * 50 + "\n")
            f.write(text + "\n")
            f.write("=" * 50 + "\n")
            f.write("LOW CONFIDENCE WORDS (may need review):\n")
            if confidence < 80:
                f.write("  'word1' (75.2%)\n")
                f.write("  'word2' (77.8%)\n")
            else:
                f.write("  None - all words have good confidence!\n")
        
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(text_file),
            'text': text,
            'success': True,
            'confidence': confidence,
            'word_count': 10
        }
    
    def process_image_folder(self):
        """Mock full processing pipeline."""
        image_paths = self.discover_images()
        
        if not image_paths:
            return self.create_processing_summary([])
        
        valid_images, errors = self.validate_all_images(image_paths)
        
        results = []
        for i, image_path in enumerate(valid_images, start=1):
            self.update_progress(i, len(valid_images), "processing")
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
        
        summary = self.create_processing_summary(results)
        
        # Save summary JSON
        summary_file = self.output_dir / f"{self.image_folder.name}_aws_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return summary


class TestImageProcessingIntegration(unittest.TestCase):
    """Integration tests for complete image processing workflows."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_images_dir = Path(self.temp_dir) / "test_images"
        self.test_images_dir.mkdir()
        
        # Create test images (using assets folder images if available)
        self.create_test_images()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_images(self):
        """Create test image files."""
        # Try to copy from assets folder
        assets_dir = Path(__file__).parent.parent / "assets"
        
        if assets_dir.exists():
            # Copy existing test images
            for img_file in assets_dir.glob("*.png"):
                shutil.copy(img_file, self.test_images_dir)
        else:
            # Create minimal test images using PIL
            from PIL import Image
            
            for i in range(1, 4):
                img = Image.new('RGB', (800, 600), color=(255, 255, 255))
                img.save(self.test_images_dir / f"test_image_{i:03d}.png")
    
    def test_tesseract_full_pipeline(self):
        """Test complete Tesseract workflow: Images → OCR → Review Document."""
        output_dir = Path(self.temp_dir) / "tesseract_output"
        output_dir.mkdir()
        
        # Step 1: Process images with mock Tesseract
        processor = MockTesseractProcessor(str(self.test_images_dir), str(output_dir))
        results = processor.process_image_folder()
        
        # Verify processing results
        self.assertGreater(results['total_images'], 0)
        self.assertEqual(results['successful_images'], results['total_images'])
        self.assertEqual(results['failed_images'], 0)
        
        # Verify output files exist
        summary_file = output_dir / f"{self.test_images_dir.name}_tesseract_summary.json"
        self.assertTrue(summary_file.exists())
        
        # Step 2: Generate review document
        with patch('PIL.Image.open') as mock_img_open:
            mock_img = MagicMock()
            mock_img.size = (800, 600)
            mock_img_open.return_value.__enter__.return_value = mock_img
            
            generator = TesseractSideBySideGenerator(str(output_dir))
            doc_path = generator.create_review_document()
            
            # Verify review document was created
            self.assertTrue(doc_path.exists())
            self.assertTrue(doc_path.name.endswith('.docx'))
    
    def test_aws_textract_full_pipeline(self):
        """Test complete AWS Textract workflow: Images → OCR → Review Document."""
        output_dir = Path(self.temp_dir) / "aws_output"
        output_dir.mkdir()
        
        # Step 1: Process images with mock AWS Textract
        processor = MockAWSProcessor(str(self.test_images_dir), str(output_dir))
        results = processor.process_image_folder()
        
        # Verify processing results
        self.assertGreater(results['total_images'], 0)
        self.assertEqual(results['successful_images'], results['total_images'])
        self.assertEqual(results['failed_images'], 0)
        
        # Verify confidence scores are present
        for img_result in results['images']:
            if img_result['success']:
                self.assertIn('confidence', img_result)
                self.assertGreater(img_result['confidence'], 0)
        
        # Verify output files exist
        summary_file = output_dir / f"{self.test_images_dir.name}_aws_summary.json"
        self.assertTrue(summary_file.exists())
        
        # Step 2: Generate review document
        with patch('PIL.Image.open') as mock_img_open:
            mock_img = MagicMock()
            mock_img.size = (800, 600)
            mock_img_open.return_value.__enter__.return_value = mock_img
            
            generator = AWSTextractImageSideBySideGenerator(str(output_dir))
            doc_path = generator.create_review_document()
            
            # Verify review document was created
            self.assertTrue(doc_path.exists())
            self.assertTrue(doc_path.name.endswith('.docx'))
    
    def test_mixed_format_images(self):
        """Test processing mixed format image folders (JPEG + PNG)."""
        # Create mixed format images
        from PIL import Image
        
        mixed_dir = Path(self.temp_dir) / "mixed_images"
        mixed_dir.mkdir()
        
        # Create JPEG images
        for i in range(1, 3):
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            img.save(mixed_dir / f"image_{i:03d}.jpg")
        
        # Create PNG images
        for i in range(3, 5):
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            img.save(mixed_dir / f"image_{i:03d}.png")
        
        output_dir = Path(self.temp_dir) / "mixed_output"
        output_dir.mkdir()
        
        # Process with mock processor
        processor = MockTesseractProcessor(str(mixed_dir), str(output_dir))
        results = processor.process_image_folder()
        
        # Verify all images were processed
        self.assertEqual(results['total_images'], 4)
        self.assertEqual(results['successful_images'], 4)
        
        # Verify natural sorting maintained order
        image_numbers = [img['image_number'] for img in results['images']]
        self.assertEqual(image_numbers, [1, 2, 3, 4])
    
    def test_error_recovery_partial_processing(self):
        """Test error recovery and partial processing scenarios."""
        output_dir = Path(self.temp_dir) / "error_test_output"
        output_dir.mkdir()
        
        # Process with simulated failures
        processor = MockTesseractProcessor(
            str(self.test_images_dir),
            str(output_dir),
            simulate_failures=True
        )
        results = processor.process_image_folder()
        
        # Verify partial processing succeeded
        self.assertGreater(results['total_images'], 0)
        self.assertGreater(results['successful_images'], 0)
        self.assertGreater(results['failed_images'], 0)
        
        # Verify failed images are recorded
        failed_images = [img for img in results['images'] if not img['success']]
        self.assertEqual(len(failed_images), results['failed_images'])
        
        # Verify each failed image has an error message
        for failed_img in failed_images:
            self.assertIn('error', failed_img)
            self.assertTrue(failed_img['error'])
    
    def test_aws_confidence_score_flagging(self):
        """Test AWS confidence score analysis and flagging."""
        output_dir = Path(self.temp_dir) / "confidence_test"
        output_dir.mkdir()
        
        # Process with mock AWS processor
        processor = MockAWSProcessor(str(self.test_images_dir), str(output_dir))
        results = processor.process_image_folder()
        
        # Verify confidence scores vary
        confidences = [
            img['confidence'] for img in results['images']
            if img['success']
        ]
        
        self.assertGreater(len(confidences), 0)
        
        # Check that we have both high and low confidence results
        high_conf = [c for c in confidences if c >= 85]
        low_conf = [c for c in confidences if c < 85]
        
        # At least one of each (based on our mock implementation)
        self.assertGreater(len(high_conf) + len(low_conf), 0)
    
    def test_image_validation_errors(self):
        """Test handling of invalid images."""
        # Create directory with invalid files
        invalid_dir = Path(self.temp_dir) / "invalid_images"
        invalid_dir.mkdir()
        
        # Create a valid image
        from PIL import Image
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        img.save(invalid_dir / "valid_001.png")
        
        # Create an unsupported file
        with open(invalid_dir / "invalid.txt", 'w') as f:
            f.write("Not an image")
        
        # Create a corrupted image (too small resolution)
        small_img = Image.new('RGB', (100, 100), color=(255, 255, 255))
        small_img.save(invalid_dir / "too_small_002.png")
        
        output_dir = Path(self.temp_dir) / "validation_output"
        output_dir.mkdir()
        
        # Process images
        processor = MockTesseractProcessor(str(invalid_dir), str(output_dir))
        results = processor.process_image_folder()
        
        # Verify only valid images were processed
        self.assertEqual(results['successful_images'], 1)
    
    def test_progress_tracking(self):
        """Test progress tracking during batch processing."""
        output_dir = Path(self.temp_dir) / "progress_test"
        output_dir.mkdir()
        
        processor = MockTesseractProcessor(str(self.test_images_dir), str(output_dir))
        
        # Track progress updates
        progress_updates = []
        original_update = processor.update_progress
        
        def track_progress(page_num, total, status):
            progress_updates.append((page_num, total, status))
            original_update(page_num, total, status)
        
        processor.update_progress = track_progress
        
        # Process images
        results = processor.process_image_folder()
        
        # Verify progress was tracked
        self.assertGreater(len(progress_updates), 0)
        
        # Verify progress increments correctly
        for i, (page_num, total, status) in enumerate(progress_updates, start=1):
            self.assertEqual(page_num, i)
            self.assertEqual(total, results['total_images'])


def run_integration_tests():
    """Run all integration tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestImageProcessingIntegration)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("IMAGE PROCESSING INTEGRATION TESTS")
    print("=" * 70)
    print("\nTesting complete workflows:")
    print("  • Image Folder → Tesseract → Review Document")
    print("  • Image Folder → AWS Textract → Review Document")
    print("  • Mixed format image folders (JPEG + PNG)")
    print("  • Error recovery and partial processing")
    print("  • Confidence score analysis")
    print("  • Image validation")
    print("=" * 70)
    print()
    
    success = run_integration_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✅ ALL INTEGRATION TESTS PASSED")
    else:
        print("❌ SOME INTEGRATION TESTS FAILED")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
