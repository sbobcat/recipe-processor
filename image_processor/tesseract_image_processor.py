#!/usr/bin/env python3
"""
Tesseract Image Processor
Processes image folders directly with Tesseract OCR
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

try:
    from PIL import Image
except ImportError:
    print("Missing Pillow. Install with: pip install Pillow")
    sys.exit(1)

try:
    import pytesseract
except ImportError:
    print("Missing pytesseract. Install with: pip install pytesseract")
    print("Also ensure Tesseract OCR is installed on your system:")
    print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("  Linux: sudo apt-get install tesseract-ocr")
    print("  Mac: brew install tesseract")
    sys.exit(1)

# Import base image processor
try:
    from base_image_processor import ImageProcessor
except ImportError:
    # Try relative import if running as script
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from base_image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class TesseractImageProcessor(ImageProcessor):
    """
    Tesseract OCR processor for image folders.
    Extends ImageProcessor base class for local Tesseract processing.
    """
    
    # Confidence threshold for flagging low-confidence words
    LOW_CONFIDENCE_THRESHOLD = 80.0
    
    def __init__(self, image_folder: str, output_dir: str, lang: str = 'eng', config: str = ''):
        """
        Initialize Tesseract image processor.
        
        Args:
            image_folder: Path to folder containing images
            output_dir: Path to output directory for results
            lang: Tesseract language code (default: 'eng')
            config: Additional Tesseract configuration options
        """
        super().__init__(image_folder, output_dir)
        
        self.lang = lang
        self.config = config
        
        # Verify Tesseract installation
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract version: {version}")
        except Exception as e:
            logger.error(f"Tesseract setup error: {e}")
            logger.error("Make sure Tesseract OCR is installed and in your PATH")
            raise
    
    def _extract_text_with_confidence(self, image_path: Path) -> Dict[str, Any]:
        """
        Extract text from image with confidence scores using Tesseract.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with OCR results and confidence scores
        """
        try:
            # Open image
            img = Image.open(image_path)
            
            # Get detailed OCR data with confidence scores
            ocr_data = pytesseract.image_to_data(
                img,
                lang=self.lang,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and confidence information
            lines = []
            words = []
            current_line = []
            current_line_confidences = []
            last_block = None
            last_par = None
            last_line = None
            
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                conf = float(ocr_data['conf'][i])
                level = ocr_data['level'][i]
                block_num = ocr_data['block_num'][i]
                par_num = ocr_data['par_num'][i]
                line_num = ocr_data['line_num'][i]
                
                # Skip empty text
                if not text:
                    continue
                
                # Track words with confidence
                if conf >= 0:  # Tesseract uses -1 for no confidence
                    words.append({
                        'text': text,
                        'confidence': conf
                    })
                
                # Detect line breaks
                if (last_block != block_num or last_par != par_num or last_line != line_num):
                    # Save previous line if it exists
                    if current_line:
                        line_text = ' '.join(current_line)
                        line_conf = (
                            sum(current_line_confidences) / len(current_line_confidences)
                            if current_line_confidences else 0
                        )
                        lines.append({
                            'text': line_text,
                            'confidence': line_conf
                        })
                    # Start new line
                    current_line = [text]
                    current_line_confidences = [conf] if conf >= 0 else []
                else:
                    # Continue current line
                    current_line.append(text)
                    if conf >= 0:
                        current_line_confidences.append(conf)
                
                last_block = block_num
                last_par = par_num
                last_line = line_num
            
            # Add final line
            if current_line:
                line_text = ' '.join(current_line)
                line_conf = (
                    sum(current_line_confidences) / len(current_line_confidences)
                    if current_line_confidences else 0
                )
                lines.append({
                    'text': line_text,
                    'confidence': line_conf
                })
            
            # Combine into full text
            full_text = '\n'.join([line['text'] for line in lines])
            avg_confidence = (
                sum([word['confidence'] for word in words]) / len(words)
                if words else 0
            )
            
            return {
                'text': full_text,
                'confidence': avg_confidence,
                'lines': lines,
                'words': words,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Tesseract OCR error for {image_path.name}: {e}")
            return {
                'text': '',
                'confidence': 0,
                'lines': [],
                'words': [],
                'error': str(e),
                'success': False
            }
    
    def process_single_image(
        self,
        image_path: Path,
        output_dir: Path,
        image_num: int
    ) -> Dict[str, Any]:
        """
        Process a single image with Tesseract OCR.
        
        Args:
            image_path: Path to image file
            output_dir: Directory for output files
            image_num: Image number in sequence
            
        Returns:
            Dictionary with processing results
        """
        logger.info(f"Processing image {image_num}: {image_path.name}")
        
        # Extract text with Tesseract
        ocr_result = self._extract_text_with_confidence(image_path)
        
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
        Process all images in the folder with Tesseract OCR.
        
        Returns:
            Dictionary with overall processing results
        """
        logger.info(f"Starting Tesseract image processing")
        logger.info(f"Image folder: {self.image_folder}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Language: {self.lang}")
        
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
        summary_file = self.output_dir / f"{self.image_folder.name}_tesseract_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n{'=' * 50}")
        logger.info("Tesseract Processing Complete")
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
        description='Process image folder with Tesseract OCR'
    )
    parser.add_argument(
        'image_folder',
        help='Path to folder containing images'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output directory (default: image_folder/tesseract_output)'
    )
    parser.add_argument(
        '-l', '--lang',
        default='eng',
        help='Tesseract language code (default: eng)'
    )
    parser.add_argument(
        '-c', '--config',
        default='',
        help='Additional Tesseract configuration options'
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = str(Path(args.image_folder) / 'tesseract_output')
    
    try:
        # Create processor
        processor = TesseractImageProcessor(
            args.image_folder,
            output_dir,
            lang=args.lang,
            config=args.config
        )
        
        # Process images
        results = processor.process_image_folder()
        
        # Print summary
        print("\n" + "=" * 50)
        print("✅ Tesseract processing complete!")
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
        print("2. Run the Tesseract review generator to create a side-by-side document")
        print("3. Check low-confidence words for accuracy")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
