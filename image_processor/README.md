# Image Processor Module

Base classes and utilities for OCR processing of image folders.

## Overview

The `ImageProcessor` base class provides common functionality for processing folders of images with OCR engines. It handles:

- **Image Discovery**: Finds and sorts image files using natural sorting (IMG_1.jpg, IMG_2.jpg, IMG_10.jpg)
- **Format Validation**: Validates image formats (JPEG, PNG, BMP, TIFF)
- **Quality Validation**: Checks image resolution and DPI for OCR suitability
- **Progress Tracking**: Provides progress updates during batch processing
- **Error Handling**: Gracefully handles invalid images and processing failures

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Image Quality Requirements

- **Minimum Resolution**: 300x300 pixels
- **Recommended DPI**: 300 DPI (warnings shown if lower)

## Usage

### Basic Implementation

```python
from image_processor import ImageProcessor

class MyOCRProcessor(ImageProcessor):
    """Custom OCR processor implementation."""
    
    def process_single_image(self, image_path, output_dir, image_num):
        """Process a single image with your OCR engine."""
        # Your OCR logic here
        ocr_text = your_ocr_engine.process(image_path)
        
        # Save results
        text_file = output_dir / f"image_{image_num:03d}_text.txt"
        text_file.write_text(ocr_text)
        
        return {
            'image_number': image_num,
            'image_file': str(image_path),
            'text_file': str(text_file),
            'text': ocr_text,
            'success': True
        }
    
    def process_image_folder(self):
        """Process all images in the folder."""
        # Discover and validate images
        image_paths = self.discover_images()
        valid_images, errors = self.validate_all_images(image_paths)
        
        # Process each image
        results = []
        for i, image_path in enumerate(valid_images, 1):
            self.update_progress(i, len(valid_images))
            result = self.process_single_image(image_path, self.output_dir, i)
            results.append(result)
        
        return self.create_processing_summary(results)

# Use the processor
processor = MyOCRProcessor("path/to/images", "path/to/output")
results = processor.process_image_folder()
```

## Key Methods

### `discover_images()`
Finds all supported image files in the folder and sorts them naturally.

```python
image_paths = processor.discover_images()
# Returns: [Path('IMG_1.jpg'), Path('IMG_2.jpg'), Path('IMG_10.jpg')]
```

### `validate_image_format(image_path)`
Checks if an image file format is supported.

```python
is_valid = processor.validate_image_format(Path('image.jpg'))
# Returns: True or False
```

### `validate_image_quality(image_path)`
Validates image resolution and quality for OCR.

```python
is_valid, metadata = processor.validate_image_quality(Path('image.jpg'))
# Returns: (True, {'width': 2000, 'height': 1500, 'dpi': (300, 300), ...})
```

### `validate_all_images(image_paths)`
Validates a list of images for format and quality.

```python
valid_images, errors = processor.validate_all_images(image_paths)
# Returns: ([valid_paths], [{'path': '...', 'reason': '...'}])
```

### `update_progress(page_num, total, status)`
Updates and displays progress during batch processing.

```python
processor.update_progress(5, 10, "processing")
# Logs: "Progress: 5/10 (50.0%) - processing"
```

### `create_processing_summary(results)`
Creates a summary of processing results.

```python
summary = processor.create_processing_summary(results)
# Returns: {
#     'folder_name': '...',
#     'total_images': 10,
#     'successful_images': 9,
#     'failed_images': 1,
#     'success_rate': 90.0,
#     'images': [...]
# }
```

## Natural Sorting

The image processor uses natural sorting to ensure images are processed in the correct order:

```
Standard sorting:     Natural sorting:
IMG_1.jpg            IMG_1.jpg
IMG_10.jpg           IMG_2.jpg
IMG_2.jpg            IMG_10.jpg
IMG_20.jpg           IMG_20.jpg
```

This is especially important for scanned documents where page order matters.

## Error Handling

The processor handles various error conditions gracefully:

- **Missing folder**: Raises `FileNotFoundError`
- **Invalid format**: Logs warning and skips file
- **Low resolution**: Logs warning and skips file
- **Corrupted image**: Logs error and skips file
- **Processing failure**: Records error in results

## Testing

Run the test script to validate functionality:

```bash
python image_processor/test_base_processor.py
```

## Example

See `example_usage.py` for a complete example of implementing a custom OCR processor.

## Requirements

- Python 3.7+
- Pillow (PIL)

Install dependencies:
```bash
pip install Pillow
```
