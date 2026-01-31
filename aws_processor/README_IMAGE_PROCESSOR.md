# AWS Textract Image Processor

Process image folders directly with AWS Textract OCR without PDF conversion.

## Overview

The AWS Textract Image Processor extends the base `ImageProcessor` class to provide cloud-based OCR processing for image folders. It processes images directly without requiring PDF conversion, making it ideal for collections of scanned images.

## Features

- **Direct Image Processing**: Process JPEG, PNG, BMP, and TIFF images without PDF conversion
- **Confidence Scoring**: AWS Textract provides confidence scores for each word and line
- **Low-Confidence Flagging**: Automatically identifies words below 80% confidence threshold
- **Batch Processing**: Efficiently processes multiple images with progress tracking
- **Rate Limiting**: Built-in rate limiting to respect AWS API limits (2 requests/second)
- **Retry Logic**: Automatic retry with exponential backoff for AWS service failures
- **Error Handling**: Graceful error handling with detailed error messages
- **Image Validation**: Validates image format, resolution, and quality before processing
- **Natural Sorting**: Maintains correct image order (IMG_1, IMG_2, IMG_10, not IMG_1, IMG_10, IMG_2)

## Requirements

```bash
pip install boto3 Pillow
```

AWS credentials must be configured:
```bash
aws configure
```

## Usage

### Command Line

```bash
python aws_textract_image_processor.py <image_folder> [-o OUTPUT_DIR] [-r REGION]
```

Example:
```bash
python aws_textract_image_processor.py C:\images\recipes -o C:\output\aws_results
```

### Python API

```python
from aws_textract_image_processor import AWSTextractImageProcessor

# Create processor
processor = AWSTextractImageProcessor(
    image_folder="C:\\images\\recipes",
    output_dir="C:\\output\\aws_results",
    region="us-east-1"
)

# Process all images
results = processor.process_image_folder()

# Check results
print(f"Processed: {results['successful_images']}/{results['total_images']}")
print(f"Average confidence: {results['average_confidence']:.1f}%")
```

### Example Usage Script

See `example_aws_image_usage.py` for a complete example with error handling and result display.

## Output Files

For each processed image, the processor creates:

1. **Text File** (`image_001_ocr.txt`):
   - Extracted text with confidence score
   - List of low-confidence words (< 80%)
   - Error messages if processing failed

2. **Summary JSON** (`folder_name_aws_summary.json`):
   - Overall processing statistics
   - Per-image results with confidence scores
   - Validation errors for invalid images

## Configuration

### Rate Limiting

Default: 2 requests per second (adjustable in class constants)

```python
processor.MAX_REQUESTS_PER_SECOND = 2
```

### Confidence Threshold

Default: 80% (words below this are flagged for review)

```python
processor.LOW_CONFIDENCE_THRESHOLD = 80.0
```

### Retry Settings

```python
processor.MAX_RETRIES = 3
processor.RETRY_DELAY_SECONDS = 2
```

## Error Handling

The processor handles various error scenarios:

- **Rate Limit Exceeded**: Automatic retry with exponential backoff
- **Invalid Image Format**: Skips invalid images and continues processing
- **Image Too Large**: Automatic compression for images > 5MB
- **AWS Service Errors**: Retry logic with detailed error messages
- **Connection Errors**: Graceful failure with error logging

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Image Requirements

- **Minimum Resolution**: 300x300 pixels
- **Recommended DPI**: 300 DPI for best OCR accuracy
- **Maximum Size**: 5MB (automatically compressed if larger)

## AWS Textract Limits

- **Synchronous API**: 5MB per image
- **Rate Limits**: Varies by account (default: 2 requests/second)
- **Service Quotas**: Check AWS console for your account limits

## Testing

Run the test suite to verify functionality:

```bash
python test_aws_image_processor.py
```

Tests include:
- Initialization with mocked AWS client
- Image discovery and validation
- Mock processing with sample responses
- Rate limiting verification
- Error handling scenarios

## Integration with Review Generator

After processing images, use the AWS Textract review generator to create side-by-side comparison documents:

```python
from aws_textract_sidebyside_generator import AWSTextractSideBySideGenerator

generator = AWSTextractSideBySideGenerator("C:\\output\\aws_results")
doc_path = generator.create_review_document()
```

## Comparison with PDF Processing

| Feature | Image Processor | PDF Processor |
|---------|----------------|---------------|
| Input | Image files | PDF files |
| Conversion | None required | PDF → Images |
| Use Case | Image collections | Scanned documents |
| Performance | Direct processing | Extra conversion step |
| Output | Per-image results | Per-page results |

## Troubleshooting

### AWS Credentials Not Found
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

### Rate Limit Exceeded
- Reduce `MAX_REQUESTS_PER_SECOND`
- Request quota increase in AWS console
- Use asynchronous API for large batches

### Image Quality Issues
- Ensure images are at least 300 DPI
- Check image resolution meets minimum requirements
- Verify images are not corrupted

### Low Confidence Scores
- Increase image resolution
- Improve scan quality
- Use preprocessing (deskew, denoise)
- Consider manual review for handwritten text

## Cost Considerations

AWS Textract charges per page/image processed. Check current pricing:
https://aws.amazon.com/textract/pricing/

Typical costs (as of 2024):
- Detect Document Text API: $1.50 per 1,000 pages
- First 1 million pages/month: $1.50 per 1,000 pages
- Over 1 million pages/month: $0.60 per 1,000 pages

## Next Steps

1. Process your image folder with AWS Textract
2. Review the OCR text files and summary JSON
3. Generate a side-by-side review document
4. Compare results with local Tesseract processing
5. Choose the best OCR method for your use case

## Related Files

- `aws_textract_image_processor.py` - Main processor class
- `example_aws_image_usage.py` - Example usage script
- `test_aws_image_processor.py` - Test suite
- `kraken_alternative_aws.py` - PDF-based AWS processor
- `aws_textract_sidebyside_generator.py` - Review document generator
- `../image_processor/base_image_processor.py` - Base class
