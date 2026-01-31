#!/usr/bin/env python3
"""
Example usage of AWS Textract Image Processor
Demonstrates how to process a folder of images with AWS Textract
"""

from pathlib import Path
from aws_textract_image_processor import AWSTextractImageProcessor

def main():
    """Example usage of AWS Textract image processor."""
    
    # Configuration
    image_folder = Path(r"C:\Code\pers\recipe-processor\assets")
    output_dir = Path(r"C:\Code\pers\recipe-processor\test-data\image_processor_test\aws_output")
    
    print("AWS Textract Image Processor - Example Usage")
    print("=" * 50)
    print(f"Image folder: {image_folder}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if folder exists
    if not image_folder.exists():
        print(f"❌ Image folder not found: {image_folder}")
        print("Please update the path in this script to point to your image folder.")
        return
    
    try:
        # Create processor
        print("Initializing AWS Textract processor...")
        processor = AWSTextractImageProcessor(
            str(image_folder),
            str(output_dir),
            region='us-east-1'
        )
        
        # Process images
        print("\nProcessing images with AWS Textract...")
        print("(This may take a while depending on the number of images)")
        print()
        
        results = processor.process_image_folder()
        
        # Display results
        print("\n" + "=" * 50)
        print("Processing Complete!")
        print("=" * 50)
        print(f"Total images: {results['total_images']}")
        print(f"Successful: {results['successful_images']}")
        print(f"Failed: {results['failed_images']}")
        print(f"Success rate: {results['success_rate']:.1f}%")
        
        if results['successful_images'] > 0:
            # Calculate average confidence
            successful_results = [r for r in results['images'] if r['success']]
            avg_confidence = sum(r['confidence'] for r in successful_results) / len(successful_results)
            print(f"Average confidence: {avg_confidence:.1f}%")
            
            # Show confidence distribution
            high_conf = len([r for r in successful_results if r['confidence'] >= 85])
            med_conf = len([r for r in successful_results if 70 <= r['confidence'] < 85])
            low_conf = len([r for r in successful_results if r['confidence'] < 70])
            
            print(f"\nConfidence distribution:")
            print(f"  High (≥85%): {high_conf} images")
            print(f"  Medium (70-84%): {med_conf} images")
            print(f"  Low (<70%): {low_conf} images")
        
        print(f"\n📁 Output saved to: {output_dir}")
        print("\n💡 Next steps:")
        print("1. Review the OCR text files in the output directory")
        print("2. Check the summary JSON file for detailed results")
        print("3. Run the AWS Textract review generator to create a side-by-side document")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure the image folder path is correct.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure AWS credentials are configured (run: aws configure)")
        print("2. Verify you have access to AWS Textract service")
        print("3. Check that the image folder contains valid image files")


if __name__ == "__main__":
    main()
