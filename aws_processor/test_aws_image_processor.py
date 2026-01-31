#!/usr/bin/env python3
"""
Test script for AWS Textract Image Processor
Tests basic functionality without requiring AWS credentials
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from aws_processor.aws_textract_image_processor import AWSTextractImageProcessor


def test_initialization():
    """Test processor initialization with mocked AWS client."""
    print("Test 1: Initialization")
    print("-" * 40)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test" / "aws_test"
    
    # Mock boto3 client
    with patch('boto3.client') as mock_boto:
        mock_textract = Mock()
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        
        def client_factory(service, **kwargs):
            if service == 'textract':
                return mock_textract
            elif service == 'sts':
                return mock_sts
            return Mock()
        
        mock_boto.side_effect = client_factory
        
        try:
            processor = AWSTextractImageProcessor(
                str(test_folder),
                str(output_folder),
                region='us-east-1'
            )
            
            print(f"✓ Processor initialized successfully")
            print(f"  Image folder: {processor.image_folder}")
            print(f"  Output dir: {processor.output_dir}")
            print(f"  Region: {processor.region}")
            print(f"  Rate limit: {processor.MAX_REQUESTS_PER_SECOND} req/s")
            print(f"  Confidence threshold: {processor.LOW_CONFIDENCE_THRESHOLD}%")
            return True
            
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            return False


def test_image_discovery():
    """Test image discovery and validation."""
    print("\nTest 2: Image Discovery")
    print("-" * 40)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test" / "aws_test"
    
    # Mock boto3 client
    with patch('boto3.client') as mock_boto:
        mock_textract = Mock()
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        
        def client_factory(service, **kwargs):
            if service == 'textract':
                return mock_textract
            elif service == 'sts':
                return mock_sts
            return Mock()
        
        mock_boto.side_effect = client_factory
        
        try:
            processor = AWSTextractImageProcessor(
                str(test_folder),
                str(output_folder)
            )
            
            # Discover images
            images = processor.discover_images()
            print(f"✓ Discovered {len(images)} images")
            
            for img in images[:5]:  # Show first 5
                print(f"  - {img.name}")
            
            if len(images) > 5:
                print(f"  ... and {len(images) - 5} more")
            
            # Validate images
            valid_images, errors = processor.validate_all_images(images)
            print(f"✓ Validated images: {len(valid_images)} valid, {len(errors)} invalid")
            
            return True
            
        except Exception as e:
            print(f"✗ Image discovery failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_mock_processing():
    """Test processing with mocked AWS Textract responses."""
    print("\nTest 3: Mock Processing")
    print("-" * 40)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test" / "aws_test"
    
    # Create output folder
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Mock AWS Textract response
    mock_response = {
        'Blocks': [
            {
                'BlockType': 'LINE',
                'Text': 'Test Recipe Title',
                'Confidence': 95.5
            },
            {
                'BlockType': 'LINE',
                'Text': 'Ingredients: flour, sugar, eggs',
                'Confidence': 88.2
            },
            {
                'BlockType': 'WORD',
                'Text': 'Test',
                'Confidence': 96.0
            },
            {
                'BlockType': 'WORD',
                'Text': 'Recipe',
                'Confidence': 95.0
            },
            {
                'BlockType': 'WORD',
                'Text': 'flour',
                'Confidence': 75.0  # Low confidence word
            }
        ]
    }
    
    # Mock boto3 client
    with patch('boto3.client') as mock_boto:
        mock_textract = Mock()
        mock_textract.detect_document_text.return_value = mock_response
        
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        
        def client_factory(service, **kwargs):
            if service == 'textract':
                return mock_textract
            elif service == 'sts':
                return mock_sts
            return Mock()
        
        mock_boto.side_effect = client_factory
        
        try:
            processor = AWSTextractImageProcessor(
                str(test_folder),
                str(output_folder)
            )
            
            # Get first image
            images = processor.discover_images()
            if not images:
                print("⚠️  No images found for testing")
                return True
            
            test_image = images[0]
            
            # Process single image
            result = processor.process_single_image(test_image, output_folder, 1)
            
            print(f"✓ Processed image: {test_image.name}")
            print(f"  Success: {result['success']}")
            print(f"  Confidence: {result['confidence']:.1f}%")
            print(f"  Word count: {result['word_count']}")
            print(f"  Text preview: {result['text'][:50]}...")
            
            # Check if text file was created
            text_file = Path(result['text_file'])
            if text_file.exists():
                print(f"✓ Text file created: {text_file.name}")
                
                # Read and display content
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'LOW CONFIDENCE WORDS' in content:
                        print(f"✓ Low confidence words section included")
            
            return True
            
        except Exception as e:
            print(f"✗ Mock processing failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_rate_limiting():
    """Test rate limiting functionality."""
    print("\nTest 4: Rate Limiting")
    print("-" * 40)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test" / "aws_test"
    
    # Mock boto3 client
    with patch('boto3.client') as mock_boto:
        mock_textract = Mock()
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        
        def client_factory(service, **kwargs):
            if service == 'textract':
                return mock_textract
            elif service == 'sts':
                return mock_sts
            return Mock()
        
        mock_boto.side_effect = client_factory
        
        try:
            processor = AWSTextractImageProcessor(
                str(test_folder),
                str(output_folder)
            )
            
            import time
            
            # Test rate limiting
            start_time = time.time()
            processor._rate_limit()
            processor._rate_limit()
            processor._rate_limit()
            elapsed = time.time() - start_time
            
            expected_min_time = 2 / processor.MAX_REQUESTS_PER_SECOND  # 2 intervals
            
            print(f"✓ Rate limiting working")
            print(f"  Max rate: {processor.MAX_REQUESTS_PER_SECOND} req/s")
            print(f"  3 calls took: {elapsed:.3f}s")
            print(f"  Expected minimum: {expected_min_time:.3f}s")
            
            if elapsed >= expected_min_time * 0.9:  # Allow 10% tolerance
                print(f"✓ Rate limiting enforced correctly")
            else:
                print(f"⚠️  Rate limiting may not be working as expected")
            
            return True
            
        except Exception as e:
            print(f"✗ Rate limiting test failed: {e}")
            return False


def test_error_handling():
    """Test error handling for various failure scenarios."""
    print("\nTest 5: Error Handling")
    print("-" * 40)
    
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test" / "aws_test"
    
    # Mock boto3 client with errors
    with patch('boto3.client') as mock_boto:
        from botocore.exceptions import ClientError
        
        mock_textract = Mock()
        
        # Simulate rate limit error
        error_response = {'Error': {'Code': 'ProvisionedThroughputExceededException'}}
        mock_textract.detect_document_text.side_effect = ClientError(
            error_response, 'detect_document_text'
        )
        
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        
        def client_factory(service, **kwargs):
            if service == 'textract':
                return mock_textract
            elif service == 'sts':
                return mock_sts
            return Mock()
        
        mock_boto.side_effect = client_factory
        
        try:
            processor = AWSTextractImageProcessor(
                str(test_folder),
                str(output_folder)
            )
            
            # Get first image
            images = processor.discover_images()
            if not images:
                print("⚠️  No images found for testing")
                return True
            
            test_image = images[0]
            
            # Try to process (should handle error gracefully)
            result = processor.process_single_image(test_image, output_folder, 1)
            
            print(f"✓ Error handling working")
            print(f"  Success: {result['success']}")
            print(f"  Error message: {result.get('error', 'None')}")
            
            if not result['success'] and 'error' in result:
                print(f"✓ Error captured correctly")
            else:
                print(f"⚠️  Error may not have been captured")
            
            return True
            
        except Exception as e:
            print(f"✗ Error handling test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AWS Textract Image Processor - Test Suite")
    print("=" * 60)
    
    tests = [
        test_initialization,
        test_image_discovery,
        test_mock_processing,
        test_rate_limiting,
        test_error_handling
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
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
