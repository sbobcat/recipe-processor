#!/usr/bin/env python3
"""
Basic tests for image review generators
Tests document creation and structure validation
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

try:
    from tesseract_sidebyside_generator import TesseractSideBySideGenerator
    from aws_textract_image_sidebyside_generator import AWSTextractImageSideBySideGenerator
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the image_processor directory")
    raise


class TestTesseractReviewGenerator(unittest.TestCase):
    """Test Tesseract side-by-side review generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "tesseract_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mock summary JSON
        self.summary_data = {
            "folder_name": "test_images",
            "total_images": 3,
            "successful_images": 2,
            "failed_images": 1,
            "success_rate": 66.7,
            "images": [
                {
                    "image_number": 1,
                    "image_file": str(self.output_dir / "image_001.jpg"),
                    "text_file": str(self.output_dir / "image_001_ocr.txt"),
                    "text": "Test text 1",
                    "success": True,
                    "confidence": 85.5
                },
                {
                    "image_number": 2,
                    "image_file": str(self.output_dir / "image_002.jpg"),
                    "text_file": str(self.output_dir / "image_002_ocr.txt"),
                    "text": "Test text 2",
                    "success": True,
                    "confidence": 92.3
                },
                {
                    "image_number": 3,
                    "image_file": str(self.output_dir / "image_003.jpg"),
                    "text_file": str(self.output_dir / "image_003_ocr.txt"),
                    "text": "",
                    "success": False,
                    "error": "Processing failed"
                }
            ]
        }
        
        # Write summary JSON
        summary_file = self.output_dir / "test_images_tesseract_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(self.summary_data, f)
        
        # Create mock text files
        for i in range(1, 3):
            text_file = self.output_dir / f"image_{i:03d}_ocr.txt"
            with open(text_file, 'w') as f:
                f.write(f"Image {i}\n")
                f.write("Confidence: 85.0%\n")
                f.write("=" * 50 + "\n")
                f.write(f"Test text {i}\n")
                f.write("=" * 50 + "\n")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test generator initialization."""
        generator = TesseractSideBySideGenerator(str(self.output_dir))
        self.assertEqual(generator.output_dir, self.output_dir)
        self.assertTrue(generator.results_file.exists())
    
    def test_load_results(self):
        """Test loading Tesseract results."""
        generator = TesseractSideBySideGenerator(str(self.output_dir))
        results = generator.load_tesseract_results()
        
        self.assertEqual(results['total_images'], 3)
        self.assertEqual(results['successful_images'], 2)
        self.assertEqual(len(results['images']), 3)
    
    @patch('tesseract_sidebyside_generator.Document')
    @patch('PIL.Image.open')
    def test_create_review_document(self, mock_image_open, mock_doc):
        """Test review document creation."""
        # Mock Document
        mock_doc_instance = MagicMock()
        mock_doc.return_value = mock_doc_instance
        
        # Mock save to create an empty file
        def mock_save(path):
            Path(path).touch()
        mock_doc_instance.save.side_effect = mock_save
        
        # Mock Image.open
        mock_img = MagicMock()
        mock_img.size = (800, 600)
        mock_image_open.return_value.__enter__.return_value = mock_img
        
        generator = TesseractSideBySideGenerator(str(self.output_dir))
        
        # Create document (will use mocked Document)
        doc_path = generator.create_review_document()
        
        # Verify document was created
        self.assertTrue(doc_path.name.endswith('.docx'))
        self.assertTrue(doc_path.exists())
        
        # Verify Document methods were called
        mock_doc_instance.add_heading.assert_called()
        mock_doc_instance.add_paragraph.assert_called()
        mock_doc_instance.save.assert_called_once()


class TestAWSTextractReviewGenerator(unittest.TestCase):
    """Test AWS Textract image side-by-side review generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "aws_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mock summary JSON
        self.summary_data = {
            "folder_name": "test_images",
            "total_images": 3,
            "successful_images": 2,
            "failed_images": 1,
            "success_rate": 66.7,
            "images": [
                {
                    "image_number": 1,
                    "image_file": str(self.output_dir / "image_001.jpg"),
                    "text_file": str(self.output_dir / "image_001_ocr.txt"),
                    "text": "Test text 1",
                    "success": True,
                    "confidence": 85.5,
                    "word_count": 10
                },
                {
                    "image_number": 2,
                    "image_file": str(self.output_dir / "image_002.jpg"),
                    "text_file": str(self.output_dir / "image_002_ocr.txt"),
                    "text": "Test text 2",
                    "success": True,
                    "confidence": 92.3,
                    "word_count": 15
                },
                {
                    "image_number": 3,
                    "image_file": str(self.output_dir / "image_003.jpg"),
                    "text_file": str(self.output_dir / "image_003_ocr.txt"),
                    "text": "",
                    "success": False,
                    "error": "AWS API error"
                }
            ]
        }
        
        # Write summary JSON
        summary_file = self.output_dir / "test_images_aws_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(self.summary_data, f)
        
        # Create mock text files
        for i in range(1, 3):
            text_file = self.output_dir / f"image_{i:03d}_ocr.txt"
            with open(text_file, 'w') as f:
                f.write(f"Image {i}\n")
                f.write("Confidence: 85.0%\n")
                f.write("=" * 50 + "\n")
                f.write(f"Test text {i}\n")
                f.write("=" * 50 + "\n")
                f.write("LOW CONFIDENCE WORDS (may need review):\n")
                f.write("  None - all words have good confidence!\n")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test generator initialization."""
        generator = AWSTextractImageSideBySideGenerator(str(self.output_dir))
        self.assertEqual(generator.output_dir, self.output_dir)
        self.assertTrue(generator.results_file.exists())
    
    def test_load_results(self):
        """Test loading AWS Textract results."""
        generator = AWSTextractImageSideBySideGenerator(str(self.output_dir))
        results = generator.load_aws_results()
        
        self.assertEqual(results['total_images'], 3)
        self.assertEqual(results['successful_images'], 2)
        self.assertEqual(len(results['images']), 3)
    
    @patch('aws_textract_image_sidebyside_generator.Document')
    @patch('PIL.Image.open')
    def test_create_review_document(self, mock_image_open, mock_doc):
        """Test review document creation."""
        # Mock Document
        mock_doc_instance = MagicMock()
        mock_doc.return_value = mock_doc_instance
        
        # Mock save to create an empty file
        def mock_save(path):
            Path(path).touch()
        mock_doc_instance.save.side_effect = mock_save
        
        # Mock Image.open
        mock_img = MagicMock()
        mock_img.size = (800, 600)
        mock_image_open.return_value.__enter__.return_value = mock_img
        
        generator = AWSTextractImageSideBySideGenerator(str(self.output_dir))
        
        # Create document (will use mocked Document)
        doc_path = generator.create_review_document()
        
        # Verify document was created
        self.assertTrue(doc_path.name.endswith('.docx'))
        self.assertTrue(doc_path.exists())
        
        # Verify Document methods were called
        mock_doc_instance.add_heading.assert_called()
        mock_doc_instance.add_paragraph.assert_called()
        mock_doc_instance.save.assert_called_once()
    
    def test_confidence_score_analysis(self):
        """Test confidence score analysis."""
        generator = AWSTextractImageSideBySideGenerator(str(self.output_dir))
        results = generator.load_aws_results()
        
        successful_images = [img for img in results['images'] if img.get('success', False)]
        confidences = [img.get('confidence', 0) for img in successful_images]
        
        self.assertEqual(len(confidences), 2)
        self.assertGreater(min(confidences), 0)
        self.assertLessEqual(max(confidences), 100)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTesseractReviewGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestAWSTextractReviewGenerator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
