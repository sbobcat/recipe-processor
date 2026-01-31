#!/usr/bin/env python3
"""
Example usage of AWS Textract Image Side-by-Side Review Generator
Demonstrates how to create review documents from AWS Textract image OCR results
"""

import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    from aws_textract_image_sidebyside_generator import AWSTextractImageSideBySideGenerator
except ImportError:
    logger.error("Could not import AWSTextractImageSideBySideGenerator")
    logger.error("Make sure you're running from the image_processor directory")
    sys.exit(1)


def main():
    """Example usage of AWS Textract image review generator."""
    
    # Example 1: Basic usage with default output path
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    aws_output_dir = r"C:\path\to\aws_textract_output"
    
    print(f"\nProcessing AWS Textract results from: {aws_output_dir}")
    print("This will create a review document in the parent directory")
    
    try:
        generator = AWSTextractImageSideBySideGenerator(aws_output_dir)
        doc_path = generator.create_review_document()
        
        print(f"\n✅ Success! Review document created:")
        print(f"   {doc_path}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open the document in Microsoft Word")
        print(f"   2. Compare images with OCR text")
        print(f"   3. Check yellow-highlighted low-confidence words")
        print(f"   4. Edit any incorrect text directly in the document")
        print(f"   5. Save your corrections")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. You've run AWS Textract image processing first")
        print("   2. The output directory exists and contains results")
        print("   3. The summary JSON file is present")
        print("   4. AWS credentials are configured (aws configure)")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Custom output path
    print("\n" + "=" * 60)
    print("Example 2: Custom Output Path")
    print("=" * 60)
    
    custom_output = r"C:\path\to\custom\aws_review_document.docx"
    
    print(f"\nProcessing with custom output path:")
    print(f"   Output: {custom_output}")
    
    try:
        generator = AWSTextractImageSideBySideGenerator(aws_output_dir)
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
        r"C:\images\batch1\aws_textract_output",
        r"C:\images\batch2\aws_textract_output",
        r"C:\images\batch3\aws_textract_output",
    ]
    
    print(f"\nProcessing {len(output_folders)} folders...")
    
    for i, folder in enumerate(output_folders, 1):
        print(f"\n[{i}/{len(output_folders)}] Processing: {folder}")
        
        try:
            generator = AWSTextractImageSideBySideGenerator(folder)
            doc_path = generator.create_review_document()
            print(f"   ✅ Created: {doc_path.name}")
            
        except FileNotFoundError as e:
            print(f"   ⚠️ Skipped: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Example 4: Analyzing confidence scores
    print("\n" + "=" * 60)
    print("Example 4: Analyzing Confidence Scores")
    print("=" * 60)
    
    print(f"\nLoading results to analyze confidence scores...")
    
    try:
        generator = AWSTextractImageSideBySideGenerator(aws_output_dir)
        results = generator.load_aws_results()
        
        successful_images = [img for img in results['images'] if img.get('success', False)]
        
        if successful_images:
            confidences = [img.get('confidence', 0) for img in successful_images]
            avg_confidence = sum(confidences) / len(confidences)
            min_confidence = min(confidences)
            max_confidence = max(confidences)
            
            print(f"\n📊 Confidence Score Analysis:")
            print(f"   Average: {avg_confidence:.1f}%")
            print(f"   Minimum: {min_confidence:.1f}%")
            print(f"   Maximum: {max_confidence:.1f}%")
            
            # Count by confidence level
            high = len([c for c in confidences if c >= 85])
            medium = len([c for c in confidences if 70 <= c < 85])
            low = len([c for c in confidences if c < 70])
            
            print(f"\n   Distribution:")
            print(f"   • High confidence (≥85%): {high} images")
            print(f"   • Medium confidence (70-84%): {medium} images")
            print(f"   • Low confidence (<70%): {low} images")
            
            if low > 0:
                print(f"\n   ⚠️ {low} images have low confidence scores")
                print(f"      These will be highlighted in the review document")
        else:
            print("\n   No successful images found")
            
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print("\n💡 Tips for using AWS Textract review documents:")
    print("   • Yellow highlighting indicates low confidence text")
    print("   • AWS Textract works well with both printed and handwritten text")
    print("   • Use Word's Track Changes to record your edits")
    print("   • Pay special attention to highlighted low-confidence words")
    print("   • Compare carefully with original images")
    print("   • Save frequently as you work")
    print("   • Consider the confidence scores when reviewing")


if __name__ == "__main__":
    main()
