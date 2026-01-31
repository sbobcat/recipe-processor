#!/usr/bin/env python3
"""
AWS Textract Image Processor
Processes image folders directly with AWS Textract without PDF conversion
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    print("Missing boto3. Install with: pip install boto3")
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    print("Missing Pillow. Install with: pip install Pillow")
    sys.exit(1)

# Import base image processor
try:
    from image_processor.base_image_processor import ImageProcessor
except ImportError:
    # Try relative import if running as script
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from image_processor.base_image_processor import ImageProcessor

# Import existing AWS OCR processor for reuse
try:
    from aws_processor.kraken_alternative_aws import AWSTextractOCR
except ImportError:
    # Try relative import
    from kraken_alternative_aws import AWSTextractOCR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class AWSTextractImageProcessor(ImageProcessor):
    """
    AWS Textract processor for image folders.
    Extends ImageProcessor base class and reuses AWSTextractOCR logic.
    """
    
    # AWS Textract rate limits (adjust based on your account limits)
    MAX_REQUESTS_PER_SECOND = 2
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2
    
    # Confidence threshold for flagging low-confidence words
    LOW_CONFIDENCE_THRESHOLD = 80.0
    
    def __init__(self, image_folder: str, output_dir: str, region: str = 'us-east-1', profile: str = None):
        """
        Initialize AWS Textract image processor.
        
        Args:
            image_folder: Path to folder containing images
            output_dir: Path to output directory for results
            region: AWS region for Textract service
            profile: AWS profile name (optional, uses default if not specified)
        """
        super().__init__(image_folder, output_dir)
        
        self.region = region
        self.profile = profile
        
        # Initialize AWS Textract client
        try:
            # Create session with profile if specified
            if profile:
                session = boto3.Session(profile_name=profile)
                self.textract = session.client('textract', region_name=region)
                sts = session.client('sts')
            else:
                self.textract = boto3.client('textract', region_name=region)
                sts = boto3.client('sts')
            
            # Test connection
            identity = sts.get_caller_identity()
            logger.info(f"AWS connection established: {identity['Account']}")
        except Exception as e:
            logger.error(f"AWS setup error: {e}")
            logger.error("Make sure you've logged in with: aws sso login --sso-session <session-name>")
            logger.error("Or set AWS_PROFILE environment variable to your profile name")
            raise
        
        # Rate limiting tracking
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting for AWS API calls."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        min_interval = 1.0 / self.MAX_REQUESTS_PER_SECOND
        
        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _load_image_bytes(self, image_path: Path) -> Optional[bytes]:
        """
        Load image file as bytes for AWS Textract.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image data as bytes, or None if loading fails
        """
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Validate image size (AWS Textract limit is 5MB for synchronous calls)
            size_mb = len(image_bytes) / (1024 * 1024)
            if size_mb > 5:
                logger.warning(
                    f"Image {image_path.name} is {size_mb:.2f}MB "
                    f"(AWS Textract limit: 5MB). Consider resizing."
                )
                # Try to compress the image
                image_bytes = self._compress_image(image_path)
            
            return image_bytes
            
        except Exception as e:
            logger.error(f"Failed to load image {image_path.name}: {e}")
            return None
    
    def _compress_image(self, image_path: Path) -> bytes:
        """
        Compress image to meet AWS Textract size limits.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Compressed image data as bytes
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                
                # Save with compression
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                compressed_bytes = output.getvalue()
                
                size_mb = len(compressed_bytes) / (1024 * 1024)
                logger.info(f"Compressed image to {size_mb:.2f}MB")
                
                return compressed_bytes
                
        except Exception as e:
            logger.error(f"Failed to compress image: {e}")
            raise
    
    def _extract_text_with_retry(self, image_bytes: bytes, image_name: str) -> Dict[str, Any]:
        """
        Extract text from image with retry logic for AWS service failures.
        
        Args:
            image_bytes: Image data as bytes
            image_name: Name of image file (for logging)
            
        Returns:
            Dictionary with OCR results and confidence scores
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                # Apply rate limiting
                self._rate_limit()
                
                # Call AWS Textract
                response = self.textract.detect_document_text(
                    Document={'Bytes': image_bytes}
                )
                
                # Extract text with confidence scores
                lines = []
                words = []
                
                for block in response['Blocks']:
                    if block['BlockType'] == 'LINE':
                        lines.append({
                            'text': block['Text'],
                            'confidence': block['Confidence']
                        })
                    elif block['BlockType'] == 'WORD':
                        words.append({
                            'text': block['Text'],
                            'confidence': block['Confidence']
                        })
                
                # Combine into full text
                full_text = '\n'.join([line['text'] for line in lines])
                avg_confidence = (
                    sum([line['confidence'] for line in lines]) / len(lines)
                    if lines else 0
                )
                
                return {
                    'text': full_text,
                    'confidence': avg_confidence,
                    'lines': lines,
                    'words': words,
                    'success': True
                }
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                if error_code == 'ProvisionedThroughputExceededException':
                    # Rate limit exceeded, retry with exponential backoff
                    if attempt < self.MAX_RETRIES - 1:
                        delay = self.RETRY_DELAY_SECONDS * (2 ** attempt)
                        logger.warning(
                            f"Rate limit exceeded for {image_name}. "
                            f"Retrying in {delay}s (attempt {attempt + 1}/{self.MAX_RETRIES})"
                        )
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"Max retries exceeded for {image_name}")
                        return {
                            'text': '',
                            'confidence': 0,
                            'lines': [],
                            'words': [],
                            'error': f"Rate limit exceeded after {self.MAX_RETRIES} retries",
                            'success': False
                        }
                
                elif error_code == 'InvalidParameterException':
                    logger.error(f"Invalid image format for {image_name}: {e}")
                    return {
                        'text': '',
                        'confidence': 0,
                        'lines': [],
                        'words': [],
                        'error': f"Invalid image format: {e}",
                        'success': False
                    }
                
                else:
                    logger.error(f"AWS Textract error for {image_name}: {e}")
                    if attempt < self.MAX_RETRIES - 1:
                        delay = self.RETRY_DELAY_SECONDS
                        logger.warning(f"Retrying in {delay}s...")
                        time.sleep(delay)
                        continue
                    else:
                        return {
                            'text': '',
                            'confidence': 0,
                            'lines': [],
                            'words': [],
                            'error': str(e),
                            'success': False
                        }
            
            except BotoCoreError as e:
                logger.error(f"AWS connection error for {image_name}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY_SECONDS
                    logger.warning(f"Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    return {
                        'text': '',
                        'confidence': 0,
                        'lines': [],
                        'words': [],
                        'error': f"Connection error: {e}",
                        'success': False
                    }
            
            except Exception as e:
                logger.error(f"Unexpected error for {image_name}: {e}")
                return {
                    'text': '',
                    'confidence': 0,
                    'lines': [],
                    'words': [],
                    'error': str(e),
                    'success': False
                }
        
        # Should not reach here, but just in case
        return {
            'text': '',
            'confidence': 0,
            'lines': [],
            'words': [],
            'error': 'Unknown error',
            'success': False
        }
    
    def process_single_image(
        self,
        image_path: Path,
        output_dir: Path,
        image_num: int
    ) -> Dict[str, Any]:
        """
        Process a single image with AWS Textract.
        
        Args:
            image_path: Path to image file
            output_dir: Directory for output files
            image_num: Image number in sequence
            
        Returns:
            Dictionary with processing results
        """
        logger.info(f"Processing image {image_num}: {image_path.name}")
        
        # Load image bytes
        image_bytes = self._load_image_bytes(image_path)
        if not image_bytes:
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': '',
                'text': '',
                'success': False,
                'confidence': 0,
                'error': 'Failed to load image'
            }
        
        # Extract text with AWS Textract
        ocr_result = self._extract_text_with_retry(image_bytes, image_path.name)
        
        # Save results to text file
        text_filename = f"image_{image_num:03d}_ocr.txt"
        text_file_path = output_dir / text_filename
        
        try:
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(f"Image {image_num} - {image_path.name}\n")
                f.write(f"Confidence: {ocr_result.get('confidence', 0):.1f}%\n")
                f.write("=" * 50 + "\n")
                f.write(ocr_result.get('text', ''))
                f.write("\n\n" + "=" * 50 + "\n")
                f.write("LOW CONFIDENCE WORDS (may need review):\n")
                
                # Flag low confidence words
                words = ocr_result.get('words', [])
                low_conf_words = [
                    w for w in words
                    if w['confidence'] < self.LOW_CONFIDENCE_THRESHOLD
                ]
                
                if low_conf_words:
                    for word in low_conf_words:
                        f.write(f"  '{word['text']}' ({word['confidence']:.1f}%)\n")
                else:
                    f.write("  None - all words have good confidence!\n")
                
                if 'error' in ocr_result:
                    f.write(f"\n\nERROR: {ocr_result['error']}\n")
        
        except Exception as e:
            logger.error(f"Failed to save text file for image {image_num}: {e}")
        
        # Return result
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(text_file_path),
            'text': ocr_result.get('text', ''),
            'success': ocr_result.get('success', False),
            'confidence': ocr_result.get('confidence', 0),
            'word_count': len(ocr_result.get('words', [])),
            'error': ocr_result.get('error', '') if not ocr_result.get('success', False) else None
        }
    
    def process_image_folder(self) -> Dict[str, Any]:
        """
        Process all images in the folder with AWS Textract.
        
        Returns:
            Dictionary with overall processing results
        """
        logger.info(f"Starting AWS Textract image processing")
        logger.info(f"Image folder: {self.image_folder}")
        logger.info(f"Output directory: {self.output_dir}")
        
        # Discover images
        image_paths = self.discover_images()
        
        if not image_paths:
            logger.warning("No images found in folder")
            return {
                'folder_name': str(self.image_folder),
                'total_images': 0,
                'successful_images': 0,
                'failed_images': 0,
                'images': []
            }
        
        # Validate images
        valid_images, validation_errors = self.validate_all_images(image_paths)
        
        if validation_errors:
            logger.warning(f"Skipping {len(validation_errors)} invalid images")
            for error in validation_errors:
                logger.warning(f"  {error['path']}: {error['reason']}")
        
        if not valid_images:
            logger.error("No valid images to process")
            return {
                'folder_name': str(self.image_folder),
                'total_images': len(image_paths),
                'successful_images': 0,
                'failed_images': len(validation_errors),
                'images': [],
                'validation_errors': validation_errors
            }
        
        # Process each image
        results = []
        for i, image_path in enumerate(valid_images, start=1):
            self.update_progress(i, len(valid_images), "processing")
            
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
            
            if result['success']:
                logger.info(
                    f"  ✓ Success - Confidence: {result['confidence']:.1f}%, "
                    f"Words: {result['word_count']}"
                )
            else:
                logger.error(f"  ✗ Failed - {result.get('error', 'Unknown error')}")
                self.failed_images += 1
        
        # Create summary
        summary = self.create_processing_summary(results)
        
        # Add validation errors to summary
        if validation_errors:
            summary['validation_errors'] = validation_errors
        
        # Save summary to JSON
        summary_file = self.output_dir / f"{self.image_folder.name}_aws_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n{'=' * 50}")
        logger.info("AWS Textract Processing Complete")
        logger.info(f"{'=' * 50}")
        logger.info(f"Total images: {summary['total_images']}")
        logger.info(f"Successful: {summary['successful_images']}")
        logger.info(f"Failed: {summary['failed_images']}")
        logger.info(f"Success rate: {summary['success_rate']:.1f}%")
        
        if summary['successful_images'] > 0:
            avg_confidence = sum(
                r['confidence'] for r in results if r['success']
            ) / summary['successful_images']
            logger.info(f"Average confidence: {avg_confidence:.1f}%")
        
        logger.info(f"Summary saved to: {summary_file}")
        
        return summary


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Process image folder with AWS Textract OCR'
    )
    parser.add_argument(
        'image_folder',
        help='Path to folder containing images'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output directory (default: image_folder/aws_textract_output)'
    )
    parser.add_argument(
        '-r', '--region',
        default='us-east-1',
        help='AWS region (default: us-east-1)'
    )
    parser.add_argument(
        '-p', '--profile',
        default=None,
        help='AWS profile name (uses default or AWS_PROFILE env var if not specified)'
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = str(Path(args.image_folder) / 'aws_textract_output')
    
    try:
        # Create processor
        processor = AWSTextractImageProcessor(
            args.image_folder,
            output_dir,
            region=args.region,
            profile=args.profile
        )
        
        # Process images
        results = processor.process_image_folder()
        
        # Print summary
        print("\n" + "=" * 50)
        print("✅ AWS Textract processing complete!")
        print("=" * 50)
        print(f"📁 Output directory: {output_dir}")
        print(f"📊 Processed: {results['successful_images']}/{results['total_images']} images")
        print(f"📈 Success rate: {results['success_rate']:.1f}%")
        
        if results['successful_images'] > 0:
            avg_confidence = sum(
                r['confidence'] for r in results['images'] if r['success']
            ) / results['successful_images']
            print(f"🎯 Average confidence: {avg_confidence:.1f}%")
        
        print("\n💡 Next steps:")
        print("1. Review the OCR text files in the output directory")
        print("2. Run the AWS Textract review generator to create a side-by-side document")
        print("3. Check low-confidence words for accuracy")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
