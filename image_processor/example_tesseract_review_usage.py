#!/usr/bin/env python3
"""
Example usage of Tesseract Side-by-Side Review Generator
Demonstrates how to create review documents from Tesseract OCR results
"""

import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    from tesseract_sidebyside_generator import TesseractSideBySideGenerator
except ImportError:
    logger.error("Could not import TesseractSideBySideGenerator")
    logger.error("Make sure you're running from the image_processor directory")
    sys.exit(1)


def main():
    """Example usage of Tesseract review generator."""
    
    # Example 1: Basic usage with default output path
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    tesseract_output_dir = r"C:\path\to\tesseract_output"
    
    print(f"\nProcessing Tesseract results from: {tesseract_output_dir}")
    print("This will create a review document in the parent directory")
    
    try:
        generator = TesseractSideBySideGenerator(tesseract_output_dir)
        doc_path = generator.create_review_document()
        
        print(f"\n✅ Success! Review document created:")
        print(f"   {doc_path}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open the document in Microsoft Word")
        print(f"   2. Compare images with OCR text")
        print(f"   3. Edit any incorrect text directly in the document")
        print(f"   4. Save your corrections")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. You've run Tesseract image processing first")
        print("   2. The output directory exists and contains results")
        print("   3. The summary JSON file is present")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Custom output path
    print("\n" + "=" * 60)
    print("Example 2: Custom Output Path")
    print("=" * 60)
    
    custom_output = r"C:\path\to\custom\review_document.docx"
    
    print(f"\nProcessing with custom output path:")
    print(f"   Output: {custom_output}")
    
    try:
        generator = TesseractSideBySideGenerator(tesseract_output_dir)
        doc_path = generator.create_review_document(output_path=custom_output)
        
        print(f"\n✅ Success! Review document created at custom location:")
        print(f"   {doc_path}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    # Example 3: Batch processing multiple folders
    print("\n" + "=" * 60)
    print("Example 3: Batch Processing Multiple Folders")
    print("=" * 60)
    
    output_folders = [
        r"C:\images\batch1\tesseract_output",
        r"C:\images\batch2\tesseract_output",
        r"C:\images\batch3\tesseract_output",
    ]
    
    print(f"\nProcessing {len(output_folders)} folders...")
    
    for i, folder in enumerate(output_folders, 1):
        print(f"\n[{i}/{len(output_folders)}] Processing: {folder}")
        
        try:
            generator = TesseractSideBySideGenerator(folder)
            doc_path = generator.create_review_document()
            print(f"   ✅ Created: {doc_path.name}")
            
        except FileNotFoundError as e:
            print(f"   ⚠️ Skipped: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print("\n💡 Tips for using review documents:")
    print("   • Tesseract works best with printed text")
    print("   • Use Word's Track Changes to record your edits")
    print("   • Compare carefully with original images")
    print("   • Save frequently as you work")
    print("   • Consider using Find & Replace for common errors")


if __name__ == "__main__":
    main()
