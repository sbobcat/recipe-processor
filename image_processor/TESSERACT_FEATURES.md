# Tesseract Image Processor - Enhanced Features

## Overview

The `TesseractImageProcessor` class provides comprehensive OCR processing for image folders with advanced preprocessing and configuration options.

## Key Features

### 1. Configurable Language Models

Support for multiple Tesseract language models:

```python
# English (default)
processor = TesseractImageProcessor(image_folder, output_dir, lang='eng')

# French
processor = TesseractImageProcessor(image_folder, output_dir, lang='fra')

# German
processor = TesseractImageProcessor(image_folder, output_dir, lang='deu')

# Spanish
processor = TesseractImageProcessor(image_folder, output_dir, lang='spa')

# Multiple languages
processor = TesseractImageProcessor(image_folder, output_dir, lang='eng+fra')
```

### 2. Automatic Rotation Detection and Correction

Automatically detects and corrects text orientation:

```python
# Enable auto-rotation (default)
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    auto_rotate=True
)

# Disable auto-rotation
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    auto_rotate=False
)
```

### 3. Image Preprocessing Options

#### Deskewing (Straighten Tilted Images)

Corrects skewed/tilted images for better OCR accuracy:

```python
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    deskew=True
)
```

**Note:** Requires `scipy` package: `pip install scipy`

#### Denoising (Remove Noise and Artifacts)

Removes salt-and-pepper noise and image artifacts:

```python
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    denoise=True
)
```

#### Contrast Enhancement

Enhances image contrast and sharpness for better text recognition:

```python
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    enhance_contrast=True
)
```

#### Enable All Preprocessing

Enable all preprocessing options at once:

```python
processor = TesseractImageProcessor(
    image_folder,
    output_dir,
    preprocess=True  # Enables deskew, denoise, and enhance_contrast
)
```

### 4. Batch Processing with Memory Management

Efficiently processes large image collections:

- Sequential processing to manage memory usage
- Automatic garbage collection every 10 images
- Progress tracking and status reporting
- Graceful error handling with partial result preservation

```python
processor = TesseractImageProcessor(image_folder, output_dir)
results = processor.process_image_folder()

# Results include:
# - Total images processed
# - Success/failure counts
# - Processing time statistics
# - Confidence scores
# - Low-confidence image tracking
```

### 5. Comprehensive Statistics and Reporting

Detailed processing statistics:

```python
results = processor.process_image_folder()

# Statistics included:
print(f"Total images: {results['total_images']}")
print(f"Successful: {results['successful_images']}")
print(f"Failed: {results['failed_images']}")
print(f"Success rate: {results['success_rate']:.1f}%")
print(f"Processing time: {results['processing_time_seconds']:.1f}s")
print(f"Average time per image: {results['average_time_per_image']:.2f}s")

# Confidence statistics:
conf_stats = results['confidence_stats']
print(f"Average confidence: {conf_stats['average']:.1f}%")
print(f"Min confidence: {conf_stats['min']:.1f}%")
print(f"Max confidence: {conf_stats['max']:.1f}%")
print(f"Median confidence: {conf_stats['median']:.1f}%")

# Low confidence tracking:
print(f"Low confidence images: {results['low_confidence_images']}")
print(f"Low confidence %: {results['low_confidence_percentage']:.1f}%")
```

### 6. Confidence Score Analysis

Automatic flagging of low-confidence words:

- Words with confidence < 80% are flagged for manual review
- Low-confidence words are listed in output text files
- Summary includes count and percentage of low-confidence images

## Command-Line Usage

```bash
# Basic usage
python tesseract_image_processor.py /path/to/images

# With output directory
python tesseract_image_processor.py /path/to/images -o /path/to/output

# With language selection
python tesseract_image_processor.py /path/to/images -l fra

# With all preprocessing
python tesseract_image_processor.py /path/to/images --preprocess

# With individual preprocessing options
python tesseract_image_processor.py /path/to/images --deskew --denoise

# Disable auto-rotation
python tesseract_image_processor.py /path/to/images --no-auto-rotate

# Full example with all options
python tesseract_image_processor.py /path/to/images \
    -o /path/to/output \
    -l eng \
    --preprocess \
    --config "--psm 3"
```

## Output Files

The processor generates:

1. **Individual text files** (`image_001_ocr.txt`, `image_002_ocr.txt`, etc.)
   - OCR text for each image
   - Confidence scores
   - Low-confidence word list

2. **Summary JSON** (`folder_name_tesseract_summary.json`)
   - Complete processing statistics
   - Per-image results
   - Confidence analysis
   - Processing time metrics

3. **Preprocessed images** (if preprocessing enabled)
   - Saved in `preprocessed_images/` subdirectory
   - Original images are preserved

4. **Rotated images** (if auto-rotation enabled)
   - Saved in `rotated_images/` subdirectory
   - Original images are preserved

## Error Handling

The processor includes comprehensive error handling:

- **Invalid images**: Skipped with detailed error messages
- **Processing failures**: Recorded in results, processing continues
- **Missing dependencies**: Clear error messages with installation instructions
- **Partial processing**: Completed work is preserved
- **Memory management**: Automatic cleanup to prevent memory issues

## Requirements

### Required
- Python 3.7+
- Pillow (PIL)
- pytesseract
- Tesseract OCR (system installation)

### Optional
- scipy (for deskewing)

## Installation

```bash
# Install Python dependencies
pip install Pillow pytesseract

# Optional: Install scipy for deskewing
pip install scipy

# Install Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract

# Install additional language packs (optional)
# Windows: Download from UB-Mannheim releases
# Linux: sudo apt-get install tesseract-ocr-fra tesseract-ocr-deu
# Mac: brew install tesseract-lang
```

## Performance Tips

1. **Use preprocessing selectively**: Only enable preprocessing options that improve your specific use case
2. **Batch size**: The processor handles memory management automatically
3. **Language models**: Use specific language models for better accuracy
4. **Image quality**: Higher resolution images (300+ DPI) produce better results
5. **Auto-rotation**: Enable for mixed-orientation documents, disable for consistent orientation

## Examples

### Example 1: Basic Processing

```python
from tesseract_image_processor import TesseractImageProcessor

processor = TesseractImageProcessor(
    image_folder='./scanned_images',
    output_dir='./ocr_output'
)

results = processor.process_image_folder()
print(f"Processed {results['successful_images']} images successfully")
```

### Example 2: Advanced Processing with Preprocessing

```python
from tesseract_image_processor import TesseractImageProcessor

processor = TesseractImageProcessor(
    image_folder='./scanned_images',
    output_dir='./ocr_output',
    lang='eng',
    preprocess=True,  # Enable all preprocessing
    auto_rotate=True
)

results = processor.process_image_folder()

# Print detailed statistics
print(f"Success rate: {results['success_rate']:.1f}%")
print(f"Average confidence: {results['confidence_stats']['average']:.1f}%")
print(f"Processing time: {results['processing_time_seconds']:.1f}s")
```

### Example 3: Multi-Language Processing

```python
from tesseract_image_processor import TesseractImageProcessor

processor = TesseractImageProcessor(
    image_folder='./multilingual_docs',
    output_dir='./ocr_output',
    lang='eng+fra+deu',  # English, French, and German
    enhance_contrast=True
)

results = processor.process_image_folder()
```

## Troubleshooting

### Tesseract Not Found
```
ERROR: Tesseract setup error: tesseract is not installed or it's not in your PATH
```
**Solution**: Install Tesseract OCR and ensure it's in your system PATH

### Low Confidence Scores
**Solutions**:
- Enable preprocessing options (`--preprocess`)
- Increase image resolution (300+ DPI recommended)
- Use appropriate language model
- Enable contrast enhancement

### Deskewing Fails
```
WARNING: scipy not available for deskewing
```
**Solution**: Install scipy: `pip install scipy`

### Memory Issues with Large Batches
The processor automatically manages memory with garbage collection every 10 images. For very large batches, consider processing in smaller chunks.
