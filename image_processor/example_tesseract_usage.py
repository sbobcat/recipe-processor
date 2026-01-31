#!/usr/bin/env python3
"""
Example usage of Tesseract Image Processor
Demonstrates how to process images with Tesseract OCR
"""

import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    from tesseract_image_processor import TesseractImageProcessor
except ImportError:
    logger.error("Could not import TesseractImageProcessor")
    logger.error("Make sure you're running from the image_processor directory")
    sys.exit(1)


def main():
    """Example usage of Tesseract image processor."""
    
    # Example 1: Basic usage with default settings
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    image_folder = r"C:\path\to\images"
    output_dir = r"C:\path\to\output\tesseract"
    
    print(f"\nProcessing images from: {image_folder}")
    print(f"Output directory: {output_dir}")
    
    try:
        processor = TesseractImageProcessor(image_folder, output_dir)
        results = processor.process_image_folder()
        
        print(f"\n✅ Success!")
        print(f"   Processed: {results['successful_images']}/{results['total_images']} images")
        print(f"   Success rate: {results['success_rate']:.1f}%")
        
        if results['successful_images'] > 0:
            avg_confidence = sum(
                r['confidence'] for r in results['images'] if r['success']
            ) / results['successful_images']
            print(f"   Average confidence: {avg_confidence:.1f}%")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure the image folder exists")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Custom language (e.g., Spanish)
    print("\n" + "=" * 60)
    print("Example 2: Custom Language")
    print("=" * 60)
    
    print(f"\nProcessing Spanish text with language code 'spa'")
    
    try:
        processor = TesseractImageProcessor(
            image_folder,
            output_dir,
            lang='spa'  # Spanish language
        )
        results = processor.process_image_folder()
        
        print(f"\n✅ Success with Spanish OCR!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure Spanish language data is installed:")
        print("   sudo apt-get install tesseract-ocr-spa  # Linux")
        print("   Or download from: https://github.com/tesseract-ocr/tessdata")
    
    # Example 3: Custom Tesseract configuration
    print("\n" + "=" * 60)
    print("Example 3: Custom Configuration")
    print("=" * 60)
    
    print(f"\nProcessing with custom Tesseract config (PSM 6 for uniform text)")
    
    try:
        processor = TesseractImageProcessor(
            image_folder,
            output_dir,
            config='--psm 6'  # Assume uniform block of text
        )
        results = processor.process_image_folder()
        
        print(f"\n✅ Success with custom config!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Example 4: Batch processing multiple folders
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    folders = [
        (r"C:\images\batch1", r"C:\output\batch1"),
        (r"C:\images\batch2", r"C:\output\batch2"),
        (r"C:\images\batch3", r"C:\output\batch3"),
    ]
    
    print(f"\nProcessing {len(folders)} folders...")
    
    for i, (img_folder, out_folder) in enumerate(folders, 1):
        print(f"\n[{i}/{len(folders)}] Processing: {img_folder}")
        
        try:
            processor = TesseractImageProcessor(img_folder, out_folder)
            results = processor.process_image_folder()
            print(f"   ✅ Processed: {results['successful_images']}/{results['total_images']} images")
            
        except FileNotFoundError as e:
            print(f"   ⚠️ Skipped: Folder not found")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("   1. Review the OCR text files in the output directory")
    print("   2. Run tesseract_sidebyside_generator.py to create a review document")
    print("   3. Check low-confidence words for accuracy")
    print("\n💡 Tesseract tips:")
    print("   • Works best with printed text (not handwritten)")
    print("   • Ensure images are at least 300 DPI for best results")
    print("   • Use --psm options to optimize for your text layout")
    print("   • Install additional language packs as needed")


if __name__ == "__main__":
    main()
