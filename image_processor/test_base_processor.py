#!/usr/bin/env python3
"""
Test script for base image processor functionality
"""

import sys
from pathlib import Path
from base_image_processor import ImageProcessor

class TestImageProcessor(ImageProcessor):
    """Test implementation of ImageProcessor for validation."""
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Test implementation - just validates the image."""
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(output_dir / f"image_{image_num:03d}_text.txt"),
            'text': f"Test text for {image_path.name}",
            'success': True
        }
    
    def process_image_folder(self):
        """Test implementation - discovers and validates images."""
        # Discover images
        image_paths = self.discover_images()
        
        if not image_paths:
            print("No images found in folder")
            return self.create_processing_summary([])
        
        # Validate images
        valid_images, errors = self.validate_all_images(image_paths)
        
        if errors:
            print(f"\n⚠️  Validation errors:")
            for error in errors:
                print(f"  - {Path(error['path']).name}: {error['reason']}")
        
        # Process valid images
        results = []
        for i, image_path in enumerate(valid_images, 1):
            self.update_progress(i, len(valid_images), "processing")
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
        
        return self.create_processing_summary(results)


def main():
    """Test the base image processor."""
    # Use the assets folder which has some test images
    test_folder = Path(__file__).parent.parent / "assets"
    output_folder = Path(__file__).parent.parent / "test-data" / "image_processor_test"
    
    print(f"Testing Image Processor Base Class")
    print(f"Image folder: {test_folder}")
    print(f"Output folder: {output_folder}")
    print("=" * 60)
    
    try:
        # Create processor (disable auto-rotate for basic test)
        processor = TestImageProcessor(str(test_folder), str(output_folder), auto_rotate=False)
        
        # Process images
        results = processor.process_image_folder()
        
        # Display results
        print("\n" + "=" * 60)
        print("Processing Results:")
        print(f"  Total images: {results['total_images']}")
        print(f"  Successful: {results['successful_images']}")
        print(f"  Failed: {results['failed_images']}")
        print(f"  Success rate: {results['success_rate']:.1f}%")
        
        print("\nImage Details:")
        for img_result in results['images']:
            status = "✓" if img_result['success'] else "✗"
            print(f"  {status} Image {img_result['image_number']}: {Path(img_result['image_file']).name}")
        
        print("\n✅ Base image processor test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
