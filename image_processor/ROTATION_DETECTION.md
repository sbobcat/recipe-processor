# Automatic Image Rotation Detection and Correction

## Overview

The image processor now includes automatic text orientation detection and correction. This feature uses Tesseract's OSD (Orientation and Script Detection) to identify if images are rotated and automatically corrects them before OCR processing.

## Features

### Text Orientation Detection
- Detects if text is vertical (90° or 270°), upside down (180°), or correct (0°)
- Uses Tesseract's OSD capability for accurate detection
- Returns confidence scores for detected orientation

### Automatic Correction
- Automatically rotates images to correct orientation before OCR
- Preserves original images - rotated versions saved separately
- Configurable via command-line flag or constructor parameter

### Rotation Metadata Tracking
- Tracks rotation corrections in processing results
- Includes detected angle, confidence, and correction applied
- Metadata saved in processing summary JSON files

## Usage

### Enable/Disable Auto-Rotation

**Tesseract Image Processor:**
```python
from image_processor.tesseract_image_processor import TesseractImageProcessor

# Enable auto-rotation (default)
processor = TesseractImageProcessor(
    image_folder="path/to/images",
    output_dir="path/to/output",
    auto_rotate=True
)

# Disable auto-rotation
processor = TesseractImageProcessor(
    image_folder="path/to/images",
    output_dir="path/to/output",
    auto_rotate=False
)
```

**AWS Textract Image Processor:**
```python
from aws_processor.aws_textract_image_processor import AWSTextractImageProcessor

# Enable auto-rotation (default)
processor = AWSTextractImageProcessor(
    image_folder="path/to/images",
    output_dir="path/to/output",
    auto_rotate=True
)

# Disable auto-rotation
processor = AWSTextractImageProcessor(
    image_folder="path/to/images",
    output_dir="path/to/output",
    auto_rotate=False
)
```

### Command-Line Usage

**Disable auto-rotation:**
```bash
# Tesseract
python image_processor/tesseract_image_processor.py path/to/images --no-auto-rotate

# AWS Textract
python aws_processor/aws_textract_image_processor.py path/to/images --no-auto-rotate
```

**Enable auto-rotation (default):**
```bash
# Tesseract
python image_processor/tesseract_image_processor.py path/to/images

# AWS Textract
python aws_processor/aws_textract_image_processor.py path/to/images
```

## How It Works

### Detection Process
1. Before OCR processing, the system calls Tesseract's OSD on each image
2. OSD returns the detected orientation angle (0°, 90°, 180°, or 270°) and confidence
3. If confidence is above threshold (default: 1.5%), rotation is applied

### Rotation Mapping
- **0°**: No rotation needed (correct orientation)
- **90°**: Image rotated 90° clockwise → Apply 270° rotation to correct
- **180°**: Image upside down → Apply 180° rotation to correct
- **270°**: Image rotated 270° clockwise → Apply 90° rotation to correct

### File Management
- Original images are preserved in their original location
- Rotated images are saved to `output_dir/rotated_images/`
- OCR processing uses the corrected image
- Both original and corrected paths tracked in metadata

## Rotation Metadata

Each processed image includes rotation metadata in the results:

```python
{
    'image_number': 1,
    'image_file': 'path/to/original.jpg',
    'text_file': 'path/to/output.txt',
    'text': 'Extracted text...',
    'success': True,
    'confidence': 95.5,
    'rotation': {
        'original_path': 'path/to/original.jpg',
        'detected_angle': 90,
        'confidence': 98.5,
        'correction_applied': True,
        'correction_angle': 270,
        'corrected_path': 'path/to/rotated_images/rotated_original.jpg'
    }
}
```

## Configuration Options

### Confidence Threshold
The minimum confidence threshold for applying rotation can be adjusted:

```python
# In base_image_processor.py
corrected_path, metadata = processor.detect_and_correct_rotation(
    image_path,
    min_confidence=1.5  # Default: 1.5%
)
```

### Disable for Specific Images
You can disable rotation for specific images by setting `auto_rotate=False` when creating the processor.

## Requirements

- **pytesseract**: Required for rotation detection
- **Tesseract OCR**: Must be installed on the system
- **PIL/Pillow**: For image manipulation

If pytesseract is not available, rotation detection is automatically disabled with a warning.

## Testing

Run the rotation detection test suite:

```bash
python image_processor/test_rotation_detection.py
```

This tests:
- Enable/disable functionality
- Rotation angle mappings
- Detection with mocked Tesseract
- No rotation for correctly oriented images

## Performance Considerations

- OSD adds minimal overhead (typically < 1 second per image)
- Rotation is only applied when needed (detected angle ≠ 0°)
- Original images are preserved, no data loss
- Rotated images cached for reuse in subsequent processing

## Troubleshooting

### "Tesseract not available for rotation detection"
- Install pytesseract: `pip install pytesseract`
- Install Tesseract OCR on your system
- Ensure Tesseract is in your system PATH

### "Could not detect orientation"
- Image may have insufficient text for OSD
- Image quality may be too low
- Try disabling auto-rotation for problematic images

### Low confidence warnings
- OSD confidence below threshold (default: 1.5%)
- Rotation skipped to avoid incorrect corrections
- Consider manual review of these images
