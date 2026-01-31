#!/usr/bin/env python3
"""
Example usage of the ImageProcessor base class
Demonstrates how to create a custom image processor
"""

from pathlib import Path
from base_image_processor import ImageProcessor


class SimpleOCRProcessor(ImageProcessor):
    """
    Example implementation of ImageProcessor.
    Replace the OCR logic with your actual OCR engine (Tesseract, AWS Textract, etc.)
    """
    
    def process_single_image(self, image_path: Path, output_dir: Path, image_num: int):
        """
        Process a single image with OCR.
        
        This is where you would call your OCR engine (Tesseract, AWS Textract, etc.)
        """
        try:
            # TODO: Replace this with actual OCR processing
            # Example for Tesseract:
            # import pytesseract
            # ocr_text = pytesseract.image_to_string(Image.open(image_path))
            
            # For now, just create a placeholder
            ocr_text = f"OCR text would go here for {image_path.name}"
            
            # Save text to file
            text_file = output_dir / f"image_{image_num:03d}_text.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(ocr_text)
            
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': str(text_file),
                'text': ocr_text,
                'success': True
            }
            
        except Exception as e:
            return {
                'image_number': image_num,
                'image_file': str(image_path),
                'text_file': '',
                'text': '',
                'success': False,
                'error': str(e)
            }
    
    def process_image_folder(self):
        """
        Process all images in the folder.
        """
        print(f"Processing images from: {self.image_folder}")
        
        # Step 1: Discover images with natural sorting
        image_paths = self.discover_images()
        
        if not image_paths:
            print("No images found!")
            return self.create_processing_summary([])
        
        # Step 2: Validate images
        valid_images, errors = self.validate_all_images(image_paths)
        
        if errors:
            print(f"\n⚠️  {len(errors)} images failed validation:")
            for error in errors:
                print(f"  - {Path(error['path']).name}: {error['reason']}")
        
        if not valid_images:
            print("No valid images to process!")
            return self.create_processing_summary([])
        
        # Step 3: Process each valid image
        results = []
        print(f"\nProcessing {len(valid_images)} valid images...")
        
        for i, image_path in enumerate(valid_images, 1):
            self.update_progress(i, len(valid_images), "processing")
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
            
            if result['success']:
                print(f"  ✓ Processed: {image_path.name}")
            else:
                print(f"  ✗ Failed: {image_path.name} - {result.get('error', 'Unknown error')}")
        
        # Step 4: Create summary
        summary = self.create_processing_summary(results)
        
        print(f"\n{'='*60}")
        print(f"Processing Complete!")
        print(f"  Total: {summary['total_images']}")
        print(f"  Successful: {summary['successful_images']}")
        print(f"  Failed: {summary['failed_images']}")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")
        print(f"{'='*60}")
        
        return summary


def main():
    """Example usage."""
    # Configure paths
    image_folder = "path/to/your/images"
    output_folder = "path/to/output"
    
    # Create processor
    processor = SimpleOCRProcessor(image_folder, output_folder)
    
    # Process all images
    results = processor.process_image_folder()
    
    # Results are now available in the output folder


if __name__ == "__main__":
    main()
