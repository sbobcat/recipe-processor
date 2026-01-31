# Image Review Generators

Generate side-by-side comparison documents from OCR results for easy review and correction.

## Overview

The image review generators create Microsoft Word documents that display original images alongside their OCR text in a two-column layout. This makes it easy to review OCR accuracy and make corrections directly in the document.

Two generators are available:
- **TesseractSideBySideGenerator**: For Tesseract OCR results
- **AWSTextractImageSideBySideGenerator**: For AWS Textract image OCR results

## Features

### Common Features (Both Generators)

- **Side-by-Side Layout**: Original images on the left, OCR text on the right
- **Image Quality Preservation**: Maintains aspect ratios and image quality
- **Editable Text**: OCR text can be edited directly in Word
- **Processing Statistics**: Summary of success rates and confidence scores
- **Error Reporting**: Clear indication of failed images with error messages
- **Progress Tracking**: Detailed logging during document generation
- **Metadata Inclusion**: Processing information and configuration details

### Tesseract-Specific Features

- Optimized for printed text OCR results
- Displays confidence scores when available
- Color-coded confidence indicators (green/orange/red)
- Handles various image formats and sizes

### AWS Textract-Specific Features

- **Confidence Score Highlighting**: Low-confidence text highlighted in yellow
- **Word-Level Confidence**: Detailed confidence scores for each word
- **Low-Confidence Flagging**: Automatic identification of words needing review
- **Color-Coded Headers**: Visual confidence indicators (green/orange/red)
- **Detailed Statistics**: Confidence distribution analysis

## Requirements

```bash
pip install python-docx Pillow
```

## Usage

### Tesseract Review Generator

#### Command Line

```bash
python tesseract_sidebyside_generator.py <output_dir> [-o OUTPUT_PATH]
```

Example:
```bash
python tesseract_sidebyside_generator.py C:\images\tesseract_output
python tesseract_sidebyside_generator.py C:\images\tesseract_output -o C:\reviews\my_review.docx
```

#### Python API

```python
from tesseract_sidebyside_generator import TesseractSideBySideGenerator

# Create generator
generator = TesseractSideBySideGenerator("C:\\images\\tesseract_output")

# Generate review document (default location)
doc_path = generator.create_review_document()

# Or specify custom output path
doc_path = generator.create_review_document(output_path="C:\\reviews\\custom.docx")

print(f"Review document created: {doc_path}")
```

### AWS Textract Review Generator

#### Command Line

```bash
python aws_textract_image_sidebyside_generator.py <output_dir> [-o OUTPUT_PATH]
```

Example:
```bash
python aws_textract_image_sidebyside_generator.py C:\images\aws_textract_output
python aws_textract_image_sidebyside_generator.py C:\images\aws_textract_output -o C:\reviews\aws_review.docx
```

#### Python API

```python
from aws_textract_image_sidebyside_generator import AWSTextractImageSideBySideGenerator

# Create generator
generator = AWSTextractImageSideBySideGenerator("C:\\images\\aws_textract_output")

# Generate review document (default location)
doc_path = generator.create_review_document()

# Or specify custom output path
doc_path = generator.create_review_document(output_path="C:\\reviews\\aws_custom.docx")

print(f"Review document created: {doc_path}")
```

## Input Requirements

### Directory Structure

Both generators expect the following structure:

```
output_directory/
├── *_summary.json          # Processing summary (required)
├── image_001_ocr.txt       # OCR text files
├── image_002_ocr.txt
└── ...
```

The original images should be accessible at the paths specified in the summary JSON.

### Summary JSON Format

**Tesseract Summary** (`*_tesseract_summary.json`):
```json
{
  "folder_name": "path/to/images",
  "total_images": 10,
  "successful_images": 9,
  "failed_images": 1,
  "success_rate": 90.0,
  "images": [
    {
      "image_number": 1,
      "image_file": "path/to/image_001.jpg",
      "text_file": "path/to/image_001_ocr.txt",
      "text": "Extracted text...",
      "success": true,
      "confidence": 85.5
    }
  ]
}
```

**AWS Textract Summary** (`*_aws_summary.json`):
```json
{
  "folder_name": "path/to/images",
  "total_images": 10,
  "successful_images": 9,
  "failed_images": 1,
  "success_rate": 90.0,
  "images": [
    {
      "image_number": 1,
      "image_file": "path/to/image_001.jpg",
      "text_file": "path/to/image_001_ocr.txt",
      "text": "Extracted text...",
      "success": true,
      "confidence": 92.3,
      "word_count": 150
    }
  ]
}
```

## Output Document Structure

### Document Layout

1. **Header Section**
   - Title
   - Processing information (total images, success rate, etc.)
   - Instructions for reviewers
   - Confidence scoring explanation (AWS only)

2. **Image Sections** (one per successful image)
   - Image number and filename
   - Confidence score (color-coded)
   - Two-column table:
     - Left: Original image (3.8" width, aspect ratio preserved)
     - Right: OCR text (Calibri 10pt, editable)
   - Low-confidence warning (AWS only)

3. **Error Section** (if any failures)
   - List of failed images with error messages

4. **Statistics Section**
   - Total images processed
   - Success/failure counts
   - Average confidence score
   - Confidence distribution (high/medium/low)

### Confidence Color Coding

- **Green**: High confidence (≥85%)
- **Orange**: Medium confidence (70-84%)
- **Red**: Low confidence (<70%)

### Text Highlighting (AWS Only)

- **Yellow**: Low-confidence text (<80%) requiring review

## Example Usage Scripts

### Tesseract Example

See `example_tesseract_review_usage.py` for:
- Basic usage with default output
- Custom output path
- Batch processing multiple folders

Run with:
```bash
python example_tesseract_review_usage.py
```

### AWS Textract Example

See `example_aws_review_usage.py` for:
- Basic usage with default output
- Custom output path
- Batch processing multiple folders
- Confidence score analysis

Run with:
```bash
python example_aws_review_usage.py
```

## Workflow Integration

### Complete Tesseract Workflow

1. **Process Images**:
   ```bash
   python tesseract_image_processor.py C:\images\folder -o C:\output\tesseract
   ```

2. **Generate Review Document**:
   ```bash
   python tesseract_sidebyside_generator.py C:\output\tesseract
   ```

3. **Review and Edit**:
   - Open the generated .docx file in Microsoft Word
   - Compare images with OCR text
   - Edit text directly in the document
   - Use Track Changes to record corrections

### Complete AWS Textract Workflow

1. **Process Images**:
   ```bash
   python aws_textract_image_processor.py C:\images\folder -o C:\output\aws
   ```

2. **Generate Review Document**:
   ```bash
   python aws_textract_image_sidebyside_generator.py C:\output\aws
   ```

3. **Review and Edit**:
   - Open the generated .docx file in Microsoft Word
   - Check yellow-highlighted low-confidence words
   - Compare images with OCR text
   - Edit text directly in the document
   - Use Track Changes to record corrections

## Tips for Reviewers

### General Tips

- **Use Track Changes**: Enable Word's Track Changes feature to record all edits
- **Save Frequently**: Save your work regularly to avoid losing corrections
- **Zoom In**: Use Word's zoom feature to see image details clearly
- **Find & Replace**: Use for common OCR errors (e.g., "0" vs "O")
- **Compare Carefully**: Always verify against the original image

### Tesseract-Specific Tips

- Tesseract works best with printed text
- Check for common OCR errors (l vs 1, O vs 0, etc.)
- Pay attention to special characters and punctuation
- Verify proper spacing between words

### AWS Textract-Specific Tips

- Focus on yellow-highlighted low-confidence words first
- Check confidence scores to prioritize review effort
- AWS Textract handles handwritten text better than Tesseract
- Verify numbers and dates carefully
- Check for proper line breaks and formatting

## Troubleshooting

### Generator Not Found Error

```
FileNotFoundError: No summary JSON file found
```

**Solution**: Make sure you've run the OCR processor first and the output directory contains the summary JSON file.

### Image Not Found Error

```
[Image not found: path/to/image.jpg]
```

**Solution**: Ensure the original images are still at the paths specified in the summary JSON. Don't move or delete images after processing.

### Import Error

```
Missing python-docx. Install with: pip install python-docx
```

**Solution**: Install required dependencies:
```bash
pip install python-docx Pillow
```

### Large File Size

If the generated document is very large (>50MB):

- Consider processing images in smaller batches
- Reduce image resolution before OCR processing
- Compress images before adding to the document

### Memory Issues

If you encounter memory errors with large image sets:

- Process images in smaller batches
- Close other applications to free up memory
- Use 64-bit Python for better memory handling

## Performance Considerations

### Document Generation Speed

- **Small batches** (1-10 images): < 1 minute
- **Medium batches** (10-50 images): 1-5 minutes
- **Large batches** (50-100 images): 5-15 minutes
- **Very large batches** (100+ images): 15+ minutes

### File Size Estimates

- **Per image**: ~100-500 KB (depends on image size and resolution)
- **10 images**: ~1-5 MB
- **50 images**: ~5-25 MB
- **100 images**: ~10-50 MB

### Optimization Tips

- Use compressed images (JPEG with 85% quality)
- Limit image resolution to 300 DPI
- Process in batches of 50-100 images
- Close the Word document between batches

## Comparison: Tesseract vs AWS Textract

| Feature | Tesseract | AWS Textract |
|---------|-----------|--------------|
| Best For | Printed text | Printed & handwritten |
| Confidence Scores | Optional | Always included |
| Highlighting | No | Yes (low-confidence) |
| Cost | Free | Pay per image |
| Speed | Fast | Moderate (API calls) |
| Accuracy (Printed) | High | Very High |
| Accuracy (Handwritten) | Low | High |
| Setup | Local installation | AWS credentials |

## Related Files

- `tesseract_sidebyside_generator.py` - Tesseract review generator
- `aws_textract_image_sidebyside_generator.py` - AWS Textract review generator
- `example_tesseract_review_usage.py` - Tesseract usage examples
- `example_aws_review_usage.py` - AWS Textract usage examples
- `base_image_processor.py` - Base image processor class
- `../aws_processor/aws_textract_image_processor.py` - AWS image processor

## Next Steps

1. Process your images with Tesseract or AWS Textract
2. Generate a review document using the appropriate generator
3. Open the document in Microsoft Word
4. Review and correct the OCR text
5. Save your corrections
6. Extract the corrected text for your application

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the example usage scripts
3. Check the main README for general setup instructions
4. Verify all dependencies are installed correctly
