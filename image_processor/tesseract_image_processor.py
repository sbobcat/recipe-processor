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
    
    def __init__(
        self,
        image_folder: str,
        output_dir: str,
        lang: str = 'eng',
        config: str = '',
        auto_rotate: bool = True,
        preprocess: bool = False,
        deskew: bool = False,
        denoise: bool = False,
        enhance_contrast: bool = False
    ):
        """
        Initialize Tesseract image processor.
        
        Args:
            image_folder: Path to folder containing images
            output_dir: Path to output directory for results
            lang: Tesseract language code (default: 'eng')
            config: Additional Tesseract configuration options
            auto_rotate: Enable automatic rotation detection and correction (default: True)
            preprocess: Enable all preprocessing options (default: False)
            deskew: Enable deskewing (straighten tilted images) (default: False)
            denoise: Enable denoising (remove noise/artifacts) (default: False)
            enhance_contrast: Enable contrast enhancement (default: False)
        """
        super().__init__(image_folder, output_dir, auto_rotate=auto_rotate)
        
        self.lang = lang
        self.config = config
        
        # Preprocessing options
        self.preprocess = preprocess
        self.deskew = deskew or preprocess
        self.denoise = denoise or preprocess
        self.enhance_contrast = enhance_contrast or preprocess
        
        # Create preprocessed images directory if preprocessing is enabled
        if self.deskew or self.denoise or self.enhance_contrast:
            self.preprocessed_dir = self.output_dir / 'preprocessed_images'
            self.preprocessed_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.preprocessed_dir = None
        
        # Verify Tesseract installation
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract version: {version}")
            logger.info(f"Language: {self.lang}")
            if self.deskew or self.denoise or self.enhance_contrast:
                logger.info(
                    f"Preprocessing enabled: "
                    f"deskew={self.deskew}, denoise={self.denoise}, "
                    f"enhance_contrast={self.enhance_contrast}"
                )
        except Exception as e:
            logger.error(f"Tesseract setup error: {e}")
            logger.error("Make sure Tesseract OCR is installed and in your PATH")
            raise
    
    def _preprocess_image(self, image_path: Path) -> Path:
        """
        Apply preprocessing to image before OCR.
        
        Args:
            image_path: Path to original image file
            
        Returns:
            Path to preprocessed image (or original if no preprocessing)
        """
        # Skip if no preprocessing enabled
        if not (self.deskew or self.denoise or self.enhance_contrast):
            return image_path
        
        try:
            # Open image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Apply deskewing
            if self.deskew:
                img = self._deskew_image(img)
            
            # Apply denoising
            if self.denoise:
                img = self._denoise_image(img)
            
            # Apply contrast enhancement
            if self.enhance_contrast:
                img = self._enhance_contrast(img)
            
            # Save preprocessed image
            preprocessed_path = self.preprocessed_dir / f"preprocessed_{image_path.name}"
            img.save(preprocessed_path)
            
            logger.debug(f"Preprocessed image saved: {preprocessed_path.name}")
            return preprocessed_path
            
        except Exception as e:
            logger.warning(f"Preprocessing failed for {image_path.name}: {e}")
            logger.warning("Using original image")
            return image_path
    
    def _deskew_image(self, img: Image.Image) -> Image.Image:
        """
        Deskew (straighten) a tilted image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Deskewed PIL Image object
        """
        try:
            import numpy as np
            from scipy import ndimage
            
            # Convert to grayscale
            if img.mode != 'L':
                gray = img.convert('L')
            else:
                gray = img
            
            # Convert to numpy array
            img_array = np.array(gray)
            
            # Calculate skew angle using projection profile method
            # This is a simplified deskewing - for production, consider using
            # more sophisticated methods like Hough transform
            
            # Threshold the image
            threshold = np.mean(img_array)
            binary = img_array < threshold
            
            # Calculate angle
            angles = np.linspace(-5, 5, 50)  # Check angles from -5 to +5 degrees
            scores = []
            
            for angle in angles:
                rotated = ndimage.rotate(binary, angle, reshape=False, order=0)
                hist = np.sum(rotated, axis=1)
                score = np.sum((hist[1:] - hist[:-1]) ** 2)
                scores.append(score)
            
            # Find angle with maximum score (most horizontal lines)
            best_angle = angles[np.argmax(scores)]
            
            # Only rotate if angle is significant (> 0.5 degrees)
            if abs(best_angle) > 0.5:
                logger.debug(f"Deskewing by {best_angle:.2f} degrees")
                img = img.rotate(best_angle, expand=True, fillcolor='white')
            
            return img
            
        except ImportError:
            logger.warning("scipy not available for deskewing. Install with: pip install scipy")
            return img
        except Exception as e:
            logger.warning(f"Deskewing failed: {e}")
            return img
    
    def _denoise_image(self, img: Image.Image) -> Image.Image:
        """
        Remove noise from image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Denoised PIL Image object
        """
        try:
            from PIL import ImageFilter
            
            # Apply median filter to remove salt-and-pepper noise
            img = img.filter(ImageFilter.MedianFilter(size=3))
            
            logger.debug("Applied denoising filter")
            return img
            
        except Exception as e:
            logger.warning(f"Denoising failed: {e}")
            return img
    
    def _enhance_contrast(self, img: Image.Image) -> Image.Image:
        """
        Enhance image contrast for better OCR.
        
        Args:
            img: PIL Image object
            
        Returns:
            Contrast-enhanced PIL Image object
        """
        try:
            from PIL import ImageEnhance
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)  # Increase contrast by 50%
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.3)  # Increase sharpness by 30%
            
            logger.debug("Applied contrast enhancement")
            return img
            
        except Exception as e:
            logger.warning(f"Contrast enhancement failed: {e}")
            return img
    
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
        
        try:
            # Detect and correct rotation if enabled
            corrected_path, rotation_metadata = self.detect_and_correct_rotation(image_path)
            
            # Apply preprocessing if enabled
            processed_path = self._preprocess_image(corrected_path)
            
            # Extract text with Tesseract using processed image
            ocr_result = self._extract_text_with_confidence(processed_path)
            
            # Save results to text file
            text_filename = f"image_{image_num:03d}_ocr.txt"
            text_file_path = output_dir / text_filename
            
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
            
            # Return result
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': str(text_file_path),
                'text': ocr_result.get('text', ''),
                'success': ocr_result.get('success', False),
                'confidence': ocr_result.get('confidence', 0),
                'word_count': len(ocr_result.get('words', [])),
                'rotation': rotation_metadata,
                'preprocessing_applied': (self.deskew or self.denoise or self.enhance_contrast),
                'error': ocr_result.get('error', '') if not ocr_result.get('success', False) else None
            }
            
        except Exception as e:
            logger.error(f"Failed to process image {image_num}: {e}")
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': '',
                'text': '',
                'success': False,
                'confidence': 0,
                'word_count': 0,
                'error': str(e)
            }
    
    def process_image_folder(self) -> Dict[str, Any]:
        """
        Process all images in the folder with Tesseract OCR.
        Implements memory-efficient batch processing.
        
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
        
        # Process each image with memory management
        results = []
        start_time = time.time()
        
        for i, image_path in enumerate(valid_images, start=1):
            self.update_progress(i, len(valid_images), "processing")
            
            # Process single image
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
            
            # Memory management: Force garbage collection every 10 images
            if i % 10 == 0:
                import gc
                gc.collect()
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create summary with enhanced statistics
        summary = self.create_processing_summary(results)
        
        # Add additional statistics
        summary['processing_time_seconds'] = processing_time
        summary['average_time_per_image'] = processing_time / len(valid_images) if valid_images else 0
        summary['language'] = self.lang
        summary['preprocessing_enabled'] = (self.deskew or self.denoise or self.enhance_contrast)
        summary['preprocessing_options'] = {
            'deskew': self.deskew,
            'denoise': self.denoise,
            'enhance_contrast': self.enhance_contrast
        }
        
        # Calculate confidence statistics
        successful_results = [r for r in results if r['success']]
        if successful_results:
            confidences = [r['confidence'] for r in successful_results]
            summary['confidence_stats'] = {
                'average': sum(confidences) / len(confidences),
                'min': min(confidences),
                'max': max(confidences),
                'median': sorted(confidences)[len(confidences) // 2]
            }
            
            # Count low confidence results
            low_conf_count = sum(1 for c in confidences if c < self.LOW_CONFIDENCE_THRESHOLD)
            summary['low_confidence_images'] = low_conf_count
            summary['low_confidence_percentage'] = (low_conf_count / len(confidences) * 100)
        
        # Add validation errors to summary
        if validation_errors:
            summary['validation_errors'] = validation_errors
        
        # Save summary to JSON
        summary_file = self.output_dir / f"{self.image_folder.name}_tesseract_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        # Print comprehensive summary
        logger.info(f"\n{'=' * 50}")
        logger.info("Tesseract Processing Complete")
        logger.info(f"{'=' * 50}")
        logger.info(f"Total images: {summary['total_images']}")
        logger.info(f"Successful: {summary['successful_images']}")
        logger.info(f"Failed: {summary['failed_images']}")
        logger.info(f"Success rate: {summary['success_rate']:.1f}%")
        logger.info(f"Processing time: {processing_time:.1f}s")
        logger.info(f"Average time per image: {summary['average_time_per_image']:.2f}s")
        
        if summary['successful_images'] > 0:
            logger.info(f"Average confidence: {summary['confidence_stats']['average']:.1f}%")
            logger.info(f"Confidence range: {summary['confidence_stats']['min']:.1f}% - {summary['confidence_stats']['max']:.1f}%")
            if summary.get('low_confidence_images', 0) > 0:
                logger.info(
                    f"Low confidence images: {summary['low_confidence_images']} "
                    f"({summary['low_confidence_percentage']:.1f}%)"
                )
        
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
        help='Tesseract language code (default: eng). Examples: eng, fra, deu, spa'
    )
    parser.add_argument(
        '-c', '--config',
        default='',
        help='Additional Tesseract configuration options'
    )
    parser.add_argument(
        '--no-auto-rotate',
        action='store_true',
        help='Disable automatic rotation detection and correction'
    )
    parser.add_argument(
        '--preprocess',
        action='store_true',
        help='Enable all preprocessing options (deskew, denoise, enhance contrast)'
    )
    parser.add_argument(
        '--deskew',
        action='store_true',
        help='Enable deskewing (straighten tilted images)'
    )
    parser.add_argument(
        '--denoise',
        action='store_true',
        help='Enable denoising (remove noise and artifacts)'
    )
    parser.add_argument(
        '--enhance-contrast',
        action='store_true',
        help='Enable contrast enhancement for better OCR'
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
            config=args.config,
            auto_rotate=not args.no_auto_rotate,
            preprocess=args.preprocess,
            deskew=args.deskew,
            denoise=args.denoise,
            enhance_contrast=args.enhance_contrast
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
        print(f"⏱️  Processing time: {results.get('processing_time_seconds', 0):.1f}s")
        
        if results['successful_images'] > 0:
            conf_stats = results.get('confidence_stats', {})
            print(f"🎯 Average confidence: {conf_stats.get('average', 0):.1f}%")
            print(f"📉 Confidence range: {conf_stats.get('min', 0):.1f}% - {conf_stats.get('max', 0):.1f}%")
            
            if results.get('low_confidence_images', 0) > 0:
                print(
                    f"⚠️  Low confidence images: {results['low_confidence_images']} "
                    f"({results.get('low_confidence_percentage', 0):.1f}%)"
                )
        
        print("\n💡 Next steps:")
        print("1. Review the OCR text files in the output directory")
        print("2. Run the Tesseract review generator to create a side-by-side document")
        print("3. Check low-confidence words for accuracy")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
