# PDF OCR Processor

**Version 1.1.0** | [Changelog](CHANGELOG.md) | [Releases](../../releases)

A document processing system that combines individual scanned PDF files and extracts text using either local (Kraken OCR) or cloud-based (AWS Textract) OCR engines. The system generates human-reviewable documents that display original images alongside extracted text for validation and correction.

The drive for this project was that my father-in-law had gotten his mother's old spiral bound recipe notebook. This contained a number of clipped and handwritten recipes taped into the pages. I wanted to accomplish 2 things, first was to scan in the pages and create a single PDF with all the pages and second was to create OCR'd text that could be updated from the recipes to make it easier to transcribe those recipes elsewhere. 

Example of the pages that I scanned:

- ![Cover page image](./assets/page-001.png)
- ![Recipe page image](./assets/page-010.png)
- ![Recipe page image](./assets/page-012.png)
 
For me creating the scanned files was fastest done by plugging a usb stick into my Canon printer/scanner and scanning the pages and writing to the usb stick. There I transfered the files to a folder to combine the images into a PDF. From there I wanted to play with different ways to OCR the text and have a way to easily compare the scan with the text from that scan.

I initially went to use Tesaract for the OCR. However, it cannot handle cursive, or handwriting. So I had to switch to Kraken which had modules for analysing handwriting. I also wanted to try out AWS Textract and compare the two results. 

I have released a v1 MVP product that will take scanned files, combine them to a single PDF and then process them through Kraken or AWS Textract and then produce a combined word document that provides a side by side comparision of the image file and its OCR text.
## 🎯 Features

- **PDF Combination**: Merge multiple individual PDF files into a single document with proper ordering
- **Dual OCR Processing**: Choose between local Kraken OCR or AWS Textract for handwritten text recognition
- **Image Folder Processing**: Process image folders directly with Tesseract (local) or AWS Textract (cloud) without PDF conversion
- **Review Documents**: Generate Word documents with side-by-side image and text comparison
- **Confidence Scoring**: AWS Textract provides confidence scores for quality assessment
- **Error Handling**: Robust error handling with detailed logging and recovery options
- **Windows-Platform Focus**: Works on Windows with WSL integration for local processing. Can be used on Linux or OSX assuming deployment of PowerShell to support the image combinor

## 📋 Prerequisites

### System Requirements
- **Windows 10/11** with PowerShell 7.5+
- **Python 3.10+** with pip
- **WSL (Windows Subsystem for Linux)** - for local Kraken OCR processing (PDF workflow)
- **Tesseract OCR** - for local image OCR processing (Image workflow, optional)
- **AWS Account** - for cloud-based OCR processing (optional)

### Required Python Packages
```bash
pip install PyMuPDF Pillow python-docx boto3
```

### PowerShell Modules
```powershell
Install-Module PSWritePDF -Force
```

### Optional: Tesseract OCR (for image processing)
```bash
# Windows: Download installer from
# https://github.com/UB-Mannheim/tesseract/wiki

# Or use Chocolatey
choco install tesseract

# Verify installation
tesseract --version
```

## 📚 Documentation

- **[README.md](README.md)** - Complete usage guide and reference (this file)
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Quick 5-minute setup instructions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world usage examples and workflows
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[config_template.py](config_template.py)** - Configuration template for customization
- **[image_processor/README.md](image_processor/README.md)** - Image processing base classes
- **[image_processor/README_REVIEW_GENERATORS.md](image_processor/README_REVIEW_GENERATORS.md)** - Review document generators
- **[aws_processor/README_IMAGE_PROCESSOR.md](aws_processor/README_IMAGE_PROCESSOR.md)** - AWS Textract image processor

## 🔍 System Information

Check your system setup and version:
```bash
# Get version number only
python version_info.py --version

# Get complete system status
python version_info.py
```

## 🚀 Quick Start

### PDF Processing Workflow

#### 1. PDF Combination
Combine individual scanned PDFs into a single document:

```powershell
# Navigate to your project directory
cd C:\path\to\recipe-processor

# Run the PDF combiner (dry-run first)
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\path\to\scanned\pdfs" -DryRun

# If order looks correct, run actual combination
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\path\to\scanned\pdfs"
```

#### 2. OCR Processing

**Option A: AWS Textract (Cloud-based)**
```bash
# Configure AWS credentials first
aws configure

# Run AWS OCR processing
python aws_processor/kraken_alternative_aws.py
```

**Option B: Kraken OCR (Local)**
```bash
# In WSL environment with Kraken installed
python local_processor/process_recipes_kraken_python_only.py
```

#### 3. Generate Review Document
```bash
# For Kraken results
python local_processor/kraken_sidebyside_generator.py

# For AWS Textract results  
python aws_processor/aws_textract_sidebyside_generator.py
```

### Image Processing Workflow

#### 1. Process Image Folder

**Option A: Tesseract (Local, for printed text)**
```bash
# Process images with Tesseract
python image_processor/tesseract_image_processor.py "C:\path\to\images" -o "C:\output\tesseract"

# Generate review document
python image_processor/tesseract_sidebyside_generator.py "C:\output\tesseract"
```

**Option B: AWS Textract (Cloud, for handwriting)**
```bash
# Configure AWS credentials first
aws configure

# Process images with AWS Textract
python aws_processor/aws_textract_image_processor.py "C:\path\to\images" -o "C:\output\aws"

# Generate review document
python image_processor/aws_textract_image_sidebyside_generator.py "C:\output\aws"
```

## 📖 Detailed Usage Guide

### PDF Combination Workflow

The PDF combiner processes individual scanned files (SCN_0000.pdf, SCN_0001.pdf, etc.) and combines them into a single document.

**Input Requirements:**
- Individual PDF files named with pattern `SCN_*.pdf`
- Files should be in numerical order
- All files should be in the same directory

**Usage:**
```powershell
# Basic usage
.\image_combinor\combine_recipe_pdfs.ps1

# Custom input folder and output name
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\MyPDFs" -OutputFile "MyDocument.pdf"

# Dry run to verify order without combining
.\image_combinor\combine_recipe_pdfs.ps1 -DryRun
```

**Output:**
- Single combined PDF file
- File size and location information
- Processing summary

### AWS Textract OCR Workflow

AWS Textract provides cloud-based OCR with handwriting detection and confidence scoring.

**Setup:**
1. **Install AWS CLI:**
   ```bash
   # Download from: https://aws.amazon.com/cli/
   aws --version
   ```

2. **Configure AWS Credentials:**
   ```bash
   aws configure
   # Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)
   ```

3. **Verify Access:**
   ```bash
   aws sts get-caller-identity
   ```

**Usage:**
```python
# Edit paths in aws_processor/kraken_alternative_aws.py
pdf_path = Path(r"C:\path\to\your\Combined_PDF.pdf")
output_dir = Path(r"C:\path\to\output\directory")

# Run processing
python aws_processor/kraken_alternative_aws.py
```

**Output Files:**
- `page_001_ocr.txt`, `page_002_ocr.txt`, etc. - Individual page text files
- `{PDF_name}_summary.json` - Processing summary with confidence scores
- Low-confidence words flagged for review

**Configuration Options:**
- **Region**: Default `us-east-1`, change in script if needed
- **Confidence Threshold**: Default 80%, words below this are flagged
- **Image Resolution**: 216 DPI (3x scaling) for optimal recognition

### Kraken OCR Workflow (Local Processing)

Kraken OCR provides local handwriting recognition optimized for historical documents.

**Setup:**
1. **Install WSL:**
   ```powershell
   # In PowerShell as Administrator
   wsl --install
   # Restart computer when prompted
   ```

2. **Install Kraken in WSL:**
   ```bash
   # In WSL terminal
   sudo apt update
   sudo apt install python3-pip
   pip3 install kraken
   
   # Download models (adjust paths as needed)
   kraken get 10.5281/zenodo.2577813  # blla.mlmodel
   kraken get 10.5281/zenodo.4274889  # McCATMuS_nfd_nofix_V1.mlmodel
   ```

3. **Verify Installation:**
   ```bash
   kraken --help
   ls ~/.kraken/  # Check models are downloaded
   ```

**Usage:**
```python
# Edit paths in local_processor/process_recipes_kraken_python_only.py
wsl_pdf_path = "/mnt/c/path/to/your/Combined_PDF.pdf"
wsl_output_dir = "/mnt/c/path/to/output/directory"

# Run processing (in WSL)
python3 local_processor/process_recipes_kraken_python_only.py
```

**Output Files:**
- `page_001_text.txt`, `page_002_text.txt`, etc. - Individual page text files
- `page_images/page-001.png`, etc. - Extracted page images (300 DPI)
- `all_pages_combined.txt` - All text in one file
- `processing_results.json` - Processing summary

**Model Configuration:**
- **Segmentation Model**: `blla.mlmodel` (baseline layout analysis)
- **Recognition Model**: `McCATMuS_nfd_nofix_V1.mlmodel` (handwriting optimized)
- **Command Structure**: `kraken -i <image> <output> segment -bl -i blla.mlmodel ocr -m McCATMuS_nfd_nofix_V1.mlmodel`

### Review Document Generation

Generate Word documents with side-by-side comparison of original images and OCR text.

#### For Kraken Results:
```python
# Edit path in local_processor/kraken_sidebyside_generator.py
kraken_output_dir = r"C:\path\to\kraken_output"

# Run generator
python local_processor/kraken_sidebyside_generator.py
```

#### For AWS Textract Results:
```python
# Edit path in aws_processor/aws_textract_sidebyside_generator.py  
aws_output_dir = r"C:\path\to\aws_textract_output"

# Run generator
python aws_processor/aws_textract_sidebyside_generator.py
```

**Output:**
- Word document (.docx) with two-column layout
- Left column: Original page images
- Right column: OCR text (editable)
- Processing metadata and statistics
- Summary of failed pages (if any)

**Document Features:**
- **Editable Text**: Correct OCR errors directly in Word
- **Image Quality**: High-resolution images for comparison
- **Confidence Highlighting**: Low-confidence words highlighted (AWS only)
- **Processing Stats**: Success rates, model information, page counts

## 📸 Image Folder Processing

The system can process folders of images directly without requiring PDF conversion. This is ideal for collections of scanned images, photos of documents, or any image-based text extraction needs.

### Supported Image Formats

- **JPEG** (.jpg, .jpeg) - Most common format for scanned documents
- **PNG** (.png) - Lossless format, good for screenshots
- **BMP** (.bmp) - Uncompressed bitmap format
- **TIFF** (.tiff, .tif) - High-quality archival format

### Image Quality Requirements

- **Minimum Resolution**: 300x300 pixels
- **Recommended DPI**: 300 DPI for optimal OCR accuracy
- **Maximum Size**: 5MB per image (automatically compressed if larger for AWS)

### Image Processing Methods

#### Option A: Tesseract OCR (Local Processing)

Tesseract is ideal for printed text and provides fast, free local processing.

**Installation:**

```bash
# Windows: Download installer from GitHub
# https://github.com/UB-Mannheim/tesseract/wiki

# Or use Chocolatey
choco install tesseract

# Verify installation
tesseract --version
```

**Language Support:**

Tesseract supports 100+ languages. Install additional language packs as needed:

```bash
# During installation, select language packs
# Or download from: https://github.com/tesseract-ocr/tessdata

# Common languages:
# - eng: English
# - fra: French
# - deu: German
# - spa: Spanish
```

**Usage:**

```bash
# Process image folder with Tesseract
python image_processor/tesseract_image_processor.py "C:\path\to\images" -o "C:\output\tesseract_results"

# Generate review document
python image_processor/tesseract_sidebyside_generator.py "C:\output\tesseract_results"
```

**Best For:**
- Printed text (books, documents, forms)
- High-contrast text
- Clean, well-lit scans
- Offline processing requirements
- Cost-sensitive projects (free)

**Limitations:**
- Poor performance on handwritten text
- Struggles with low-quality images
- Limited confidence scoring

#### Option B: AWS Textract (Cloud Processing)

AWS Textract provides superior accuracy for both printed and handwritten text with detailed confidence scoring.

**Setup:**

```bash
# Configure AWS credentials (one-time)
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Verify access
aws sts get-caller-identity
```

**Usage:**

```bash
# Process image folder with AWS Textract
python aws_processor/aws_textract_image_processor.py "C:\path\to\images" -o "C:\output\aws_results"

# Generate review document
python image_processor/aws_textract_image_sidebyside_generator.py "C:\output\aws_results"
```

**Best For:**
- Handwritten text (notes, forms, historical documents)
- Mixed printed and handwritten content
- Low-quality or degraded images
- High accuracy requirements
- Confidence scoring needs

**Limitations:**
- Requires AWS account and credentials
- Costs $1.50 per 1,000 images (first 1M pages/month)
- Requires internet connection
- Rate limits apply (2 requests/second default)

### Image Processing Workflow

#### Complete Tesseract Workflow

```bash
# Step 1: Organize your images
# Place all images in a single folder
# Images will be sorted naturally: IMG_1.jpg, IMG_2.jpg, IMG_10.jpg

# Step 2: Process images with Tesseract
python image_processor/tesseract_image_processor.py "C:\MyImages" -o "C:\Output\Tesseract"

# Step 3: Generate review document
python image_processor/tesseract_sidebyside_generator.py "C:\Output\Tesseract"

# Step 4: Review and edit
# Open the generated .docx file in Microsoft Word
# Compare images with OCR text and make corrections
```

#### Complete AWS Textract Workflow

```bash
# Step 1: Organize your images
# Place all images in a single folder

# Step 2: Configure AWS (one-time setup)
aws configure

# Step 3: Process images with AWS Textract
python aws_processor/aws_textract_image_processor.py "C:\MyImages" -o "C:\Output\AWS"

# Step 4: Generate review document
python image_processor/aws_textract_image_sidebyside_generator.py "C:\Output\AWS"

# Step 5: Review and edit
# Open the generated .docx file in Microsoft Word
# Focus on yellow-highlighted low-confidence words
# Compare images with OCR text and make corrections
```

### Image Processing Output

For each processed image, the system creates:

**Text Files:**
```
image_001_ocr.txt  - Extracted text from image 1
image_002_ocr.txt  - Extracted text from image 2
...
```

**Summary JSON:**
```json
{
  "folder_name": "MyImages",
  "total_images": 10,
  "successful_images": 9,
  "failed_images": 1,
  "success_rate": 90.0,
  "average_confidence": 87.5,
  "images": [...]
}
```

**Review Document:**
- Word document (.docx) with side-by-side layout
- Left column: Original images
- Right column: OCR text (editable)
- Confidence scores and statistics
- Error summary for failed images

### Differences: PDF vs Image Processing

| Feature | PDF Processing | Image Processing |
|---------|---------------|------------------|
| **Input** | PDF files | Image files (JPEG, PNG, etc.) |
| **Conversion** | PDF → Images → OCR | Direct OCR processing |
| **Use Case** | Scanned documents, books | Photo collections, individual scans |
| **Combination Step** | Required (PowerShell) | Not needed |
| **Local OCR** | Kraken (handwriting) | Tesseract (printed text) |
| **Cloud OCR** | AWS Textract | AWS Textract |
| **Performance** | Extra conversion step | Direct processing |
| **Best For** | Multi-page documents | Individual images or photo sets |

### Image Processing Tips

**For Best OCR Results:**
- Use 300 DPI or higher resolution
- Ensure good lighting and contrast
- Avoid shadows and glare
- Keep text horizontal (not rotated)
- Use high-quality scans or photos

**File Organization:**
- Use numerical naming: IMG_001.jpg, IMG_002.jpg, etc.
- Keep all images in a single folder
- Don't mix different document sets
- Maintain consistent image quality

**Choosing Between Tesseract and AWS:**
- **Use Tesseract** for: Printed text, offline processing, cost-free projects
- **Use AWS Textract** for: Handwritten text, high accuracy needs, confidence scoring

**Performance Optimization:**
- Process images in batches of 50-100
- Use JPEG format with 85% quality for smaller files
- Close other applications during processing
- Monitor disk space for output files

### Tesseract Installation and Configuration

#### Windows Installation

**Method 1: Official Installer**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (tesseract-ocr-w64-setup-v5.x.x.exe)
3. During installation:
   - Select installation directory (default: C:\Program Files\Tesseract-OCR)
   - Choose language packs (at minimum: English)
   - Add Tesseract to PATH (recommended)
4. Verify installation:
   ```bash
   tesseract --version
   ```

**Method 2: Chocolatey**
```bash
# Install Chocolatey first if not installed
# Then install Tesseract
choco install tesseract

# Verify installation
tesseract --version
```

#### Language Configuration

Tesseract supports 100+ languages. Install additional languages as needed:

**During Installation:**
- Select language packs in the installer

**Manual Installation:**
1. Download language files from: https://github.com/tesseract-ocr/tessdata
2. Copy .traineddata files to: C:\Program Files\Tesseract-OCR\tessdata\
3. Verify available languages:
   ```bash
   tesseract --list-langs
   ```

**Common Language Codes:**
- `eng` - English
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Chinese Simplified
- `chi_tra` - Chinese Traditional
- `jpn` - Japanese
- `kor` - Korean

**Using Multiple Languages:**
```bash
# Process with multiple languages
tesseract image.jpg output -l eng+fra
```

#### Configuration Options

Tesseract can be configured for different use cases:

**Page Segmentation Modes (PSM):**
- `0` - Orientation and script detection only
- `1` - Automatic page segmentation with OSD
- `3` - Fully automatic page segmentation (default)
- `6` - Assume a single uniform block of text
- `7` - Treat the image as a single text line
- `11` - Sparse text. Find as much text as possible

**OCR Engine Modes (OEM):**
- `0` - Legacy engine only
- `1` - Neural nets LSTM engine only
- `2` - Legacy + LSTM engines
- `3` - Default, based on what is available

**Example Configuration:**
```python
# In tesseract_image_processor.py, modify the command:
cmd = [
    'tesseract',
    str(image_path),
    str(output_base),
    '-l', 'eng',      # Language
    '--psm', '3',     # Page segmentation mode
    '--oem', '1',     # OCR engine mode
    'txt'             # Output format
]
```

#### Troubleshooting Tesseract

**Error: "tesseract is not recognized"**
- Add Tesseract to PATH:
  1. Open System Properties → Environment Variables
  2. Edit PATH variable
  3. Add: C:\Program Files\Tesseract-OCR
  4. Restart terminal/IDE

**Error: "Failed loading language 'eng'"**
- Verify language files exist in tessdata folder
- Reinstall Tesseract with language packs
- Check file permissions on tessdata folder

**Poor OCR Accuracy:**
- Increase image resolution (300 DPI minimum)
- Improve image quality (contrast, lighting)
- Try different PSM modes
- Use appropriate language pack
- Preprocess images (deskew, denoise)

### Example: Processing Recipe Images

Here's a complete example of processing a collection of recipe images:

```bash
# Scenario: You have 50 photos of recipe cards

# Step 1: Organize images
# Place all photos in: C:\Recipes\Images\
# Rename to: recipe_001.jpg, recipe_002.jpg, etc.

# Step 2: Choose processing method

# Option A: Tesseract (for printed recipe cards)
python image_processor/tesseract_image_processor.py "C:\Recipes\Images" -o "C:\Recipes\Tesseract_Output"
python image_processor/tesseract_sidebyside_generator.py "C:\Recipes\Tesseract_Output"

# Option B: AWS Textract (for handwritten recipes)
python aws_processor/aws_textract_image_processor.py "C:\Recipes\Images" -o "C:\Recipes\AWS_Output"
python image_processor/aws_textract_image_sidebyside_generator.py "C:\Recipes\AWS_Output"

# Step 3: Review results
# Open the generated .docx file
# Compare images with OCR text
# Correct any errors directly in Word
# Save the corrected document

# Step 4: Extract corrected text
# Copy text from Word document to your recipe database
# Or export as plain text for further processing
```

**Document Features:**
- **Editable Text**: Correct OCR errors directly in Word
- **Image Quality**: High-resolution images for comparison
- **Confidence Highlighting**: Low-confidence words highlighted (AWS only)
- **Processing Stats**: Success rates, model information, page counts

## ⚙️ Configuration Options

### File Paths
All scripts use hardcoded paths that should be updated for your environment:

**PDF Combiner:**
```powershell
# In image_combinor/combine_recipe_pdfs.ps1
$InputFolder = "C:\your\path\to\scanned\pdfs"
$OutputFile = "Your_Combined_Document.pdf"
```

**AWS Processor:**
```python
# In aws_processor/kraken_alternative_aws.py
pdf_path = Path(r"C:\your\path\to\Combined_PDF.pdf")
output_dir = Path(r"C:\your\path\to\aws_output")
```

**Kraken Processor:**
```python
# In local_processor/process_recipes_kraken_python_only.py
wsl_pdf_path = "/mnt/c/your/path/to/Combined_PDF.pdf"
wsl_output_dir = "/mnt/c/your/path/to/kraken_output"
```

### OCR Settings

**AWS Textract:**
- **Region**: `us-east-1` (change in `AWSTextractOCR.__init__()`)
- **Confidence Threshold**: 80% (change in `extract_handwritten_text()`)
- **Image Resolution**: 216 DPI (change `Matrix(3, 3)` in `pdf_to_images()`)

**Kraken OCR:**
- **Image Resolution**: 300 DPI (change `Matrix(300/72, 300/72)` in `extract_pdf_pages_python()`)
- **Models**: Update model names in `KrakenProcessorPythonOnly.__init__()`
- **Command Options**: Modify `ocr_cmd` in `process_single_page()`

## 🔧 Troubleshooting

### Common Issues

#### PDF Combination Issues

**Error: "PSWritePDF module not found"**
```powershell
# Install the module
Install-Module PSWritePDF -Force -AllowClobber

# If still failing, try:
Import-Module PSWritePDF -Force
```

**Error: "No SCN_*.pdf files found"**
- Verify files are named correctly (SCN_0000.pdf, SCN_0001.pdf, etc.)
- Check the input folder path is correct
- Ensure files are not corrupted

**Error: "Access denied" or permission issues**
- Run PowerShell as Administrator
- Check file permissions on input and output directories
- Ensure files are not open in another application

#### AWS Textract Issues

**Error: "AWS setup error" or credential issues**
```bash
# Reconfigure AWS credentials
aws configure

# Test access
aws sts get-caller-identity

# Check region settings
aws configure get region
```

**Error: "Textract error: InvalidParameterException"**
- Check image size limits (max 10MB per image)
- Verify image format is supported (PNG, JPEG)
- Ensure PDF is not corrupted

**Error: "Rate limit exceeded"**
- AWS Textract has rate limits (varies by region)
- Add delays between API calls if processing many pages
- Consider using asynchronous processing for large documents

#### Kraken OCR Issues

**Error: "Kraken not found"**
```bash
# In WSL, verify installation
which kraken
kraken --help

# If not installed:
pip3 install kraken
```

**Error: "Model not found"**
```bash
# Check available models
kraken list

# Download missing models
kraken get 10.5281/zenodo.2577813  # blla.mlmodel
kraken get 10.5281/zenodo.4274889  # McCATMuS_nfd_nofix_V1.mlmodel

# Verify model location
ls ~/.kraken/
```

**Error: "Permission denied" on WSL paths**
- Ensure WSL can access Windows files via `/mnt/c/`
- Check file permissions: `chmod 644 /mnt/c/path/to/file.pdf`
- Verify paths use forward slashes in WSL

**Poor OCR Accuracy:**
- Increase image resolution (300 DPI minimum)
- Improve image quality (contrast, lighting)
- Try different PSM modes
- Use appropriate language pack
- Preprocess images (deskew, denoise)

#### Image Processing Issues

**Error: "No supported images found in folder"**
- Verify images have supported extensions (.jpg, .jpeg, .png, .bmp, .tiff, .tif)
- Check folder path is correct
- Ensure images are not corrupted
- Verify file permissions

**Error: "Image resolution too low"**
- Images must be at least 300x300 pixels
- Rescan images at higher resolution (300 DPI recommended)
- Use higher quality camera/scanner settings

**Error: "Tesseract not found"**
```bash
# Install Tesseract
choco install tesseract

# Or download from: https://github.com/UB-Mannheim/tesseract/wiki

# Add to PATH if needed
# System Properties → Environment Variables → PATH
# Add: C:\Program Files\Tesseract-OCR
```

**Error: "Failed loading language"**
- Verify language files exist in tessdata folder
- Reinstall Tesseract with required language packs
- Download language files from: https://github.com/tesseract-ocr/tessdata
- Copy .traineddata files to: C:\Program Files\Tesseract-OCR\tessdata\

**Poor Image OCR Results:**
- Use 300 DPI or higher resolution
- Ensure good lighting and contrast
- Avoid shadows, glare, and reflections
- Keep text horizontal (not rotated)
- Use high-quality scans or photos
- Try preprocessing (deskew, denoise, contrast enhancement)

**AWS Textract Image Processing Issues:**
- Check image size limits (max 5MB per image)
- Verify image format is supported (JPEG, PNG, BMP, TIFF)
- Ensure AWS credentials are configured correctly
- Monitor rate limits (2 requests/second default)
- Check AWS service quotas in console

#### Review Document Generation Issues

**Error: "Missing python-docx"**
```bash
pip install python-docx
```

**Error: "Image not found" in review document**
- Verify image paths in OCR output match actual file locations
- Check that page images were extracted successfully
- Ensure image files are not corrupted

**Error: "Document creation failed"**
- Check available disk space (Word documents can be large)
- Verify output directory exists and is writable
- Close any existing Word documents with the same name

### Performance Optimization

**Large Document Processing:**
- Process documents in smaller batches
- Monitor memory usage during processing
- Use SSD storage for faster I/O operations

**AWS Cost Optimization:**
- Use dry-run mode to verify setup before processing
- Monitor AWS billing for Textract usage
- Consider batch processing for multiple documents

**Kraken Performance:**
- Use high-resolution images (300 DPI) for better accuracy
- Ensure adequate RAM for large documents
- Consider using GPU acceleration if available

## 📁 Project Structure

```
recipe-processor/
├── aws_processor/
│   ├── kraken_alternative_aws.py          # AWS Textract OCR processor (PDF)
│   ├── aws_textract_sidebyside_generator.py  # AWS review document generator (PDF)
│   ├── aws_textract_image_processor.py    # AWS Textract image processor
│   ├── example_aws_image_usage.py         # AWS image processing examples
│   └── README_IMAGE_PROCESSOR.md          # AWS image processor documentation
├── image_combinor/
│   └── combine_recipe_pdfs.ps1            # PDF combination script
├── image_processor/
│   ├── base_image_processor.py            # Base class for image processing
│   ├── tesseract_image_processor.py       # Tesseract OCR processor (images)
│   ├── tesseract_sidebyside_generator.py  # Tesseract review generator
│   ├── aws_textract_image_sidebyside_generator.py  # AWS image review generator
│   ├── example_usage.py                   # Image processing examples
│   ├── example_tesseract_review_usage.py  # Tesseract review examples
│   ├── example_aws_review_usage.py        # AWS review examples
│   ├── README.md                          # Image processor documentation
│   └── README_REVIEW_GENERATORS.md        # Review generator documentation
├── local_processor/
│   ├── process_recipes_kraken_python_only.py  # Kraken OCR processor (PDF)
│   └── kraken_sidebyside_generator.py     # Kraken review document generator (PDF)
├── test-data/
│   ├── SCN_0000.pdf ... SCN_0052.pdf     # Individual scanned PDFs
│   ├── Anns_Complete_Recipe_Book.pdf     # Combined PDF
│   ├── aws_textract_output/              # AWS processing results (PDF)
│   ├── kraken_output/                    # Kraken processing results (PDF)
│   └── image_processor_test/             # Image processing test data
├── .kiro/
│   └── specs/pdf-ocr-processor/          # Project specifications
├── README.md                             # This documentation
└── .gitignore                           # Git ignore rules
```

## 🔄 Complete Workflow Examples

### Workflow 1: PDF Processing (Multi-Page Documents)

Here's a complete example of processing a set of recipe PDFs:

#### Step 1: Prepare Individual PDFs
```
# Ensure your scanned PDFs are named:
SCN_0000.pdf, SCN_0001.pdf, SCN_0002.pdf, ... SCN_0052.pdf
```

#### Step 2: Combine PDFs
```powershell
# Test the combination order first
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\MyRecipes" -DryRun

# If order is correct, combine
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\MyRecipes" -OutputFile "My_Recipe_Book.pdf"
```

#### Step 3: Choose OCR Method

**Option A: AWS Textract (Recommended for handwriting)**
```bash
# Configure AWS (one-time setup)
aws configure

# Edit paths in aws_processor/kraken_alternative_aws.py
# Run OCR processing
python aws_processor/kraken_alternative_aws.py

# Generate review document
python aws_processor/aws_textract_sidebyside_generator.py
```

**Option B: Kraken OCR (Local processing)**
```bash
# Setup WSL and Kraken (one-time setup)
# Edit paths in local_processor/process_recipes_kraken_python_only.py

# In WSL terminal:
python3 local_processor/process_recipes_kraken_python_only.py

# Generate review document (in Windows):
python local_processor/kraken_sidebyside_generator.py
```

#### Step 4: Review and Edit
1. Open the generated Word document
2. Compare original images (left) with OCR text (right)
3. Edit OCR text directly in Word to correct any errors
4. Save the corrected document

### Workflow 2: Image Folder Processing (Individual Images)

Here's a complete example of processing a folder of recipe card images:

#### Step 1: Organize Images
```
# Place all images in a single folder:
C:\MyRecipes\Images\
  recipe_001.jpg
  recipe_002.jpg
  recipe_003.jpg
  ...
```

#### Step 2: Choose OCR Method

**Option A: Tesseract (Recommended for printed text)**
```bash
# Process images with Tesseract
python image_processor/tesseract_image_processor.py "C:\MyRecipes\Images" -o "C:\MyRecipes\Tesseract_Output"

# Generate review document
python image_processor/tesseract_sidebyside_generator.py "C:\MyRecipes\Tesseract_Output"
```

**Option B: AWS Textract (Recommended for handwriting)**
```bash
# Configure AWS (one-time setup)
aws configure

# Process images with AWS Textract
python aws_processor/aws_textract_image_processor.py "C:\MyRecipes\Images" -o "C:\MyRecipes\AWS_Output"

# Generate review document
python image_processor/aws_textract_image_sidebyside_generator.py "C:\MyRecipes\AWS_Output"
```

#### Step 3: Review and Edit
1. Open the generated Word document
2. Compare original images (left) with OCR text (right)
3. For AWS: Focus on yellow-highlighted low-confidence words
4. Edit OCR text directly in Word to correct any errors
5. Save the corrected document

### Choosing the Right Workflow

**Use PDF Processing When:**
- You have multi-page scanned documents
- Pages are already combined into PDFs
- You need to maintain document structure
- Working with books, manuals, or reports

**Use Image Processing When:**
- You have individual image files (photos, scans)
- Images are not yet combined into PDFs
- You want to skip the PDF combination step
- Working with recipe cards, forms, or individual pages

**Use Kraken/Tesseract When:**
- You need offline processing
- Cost is a concern (free)
- Processing printed text (Tesseract)
- You have WSL/Linux available (Kraken)

**Use AWS Textract When:**
- Processing handwritten text
- You need high accuracy
- Confidence scoring is important
- You have AWS credentials and budget

## 🤝 Contributing

This project follows a specification-driven development approach. See `.kiro/specs/pdf-ocr-processor/` for detailed requirements, design, and implementation tasks.

### Development Workflow
1. Check current version: `python version_info.py --version`
2. Review [CHANGELOG.md](CHANGELOG.md) for recent changes
3. Follow the task list in `.kiro/specs/pdf-ocr-processor/tasks.md`
4. Update version and changelog for releases

### Versioning
This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- See [CHANGELOG.md](CHANGELOG.md) for version history and migration guides

## 📄 License

This project is for personal use. Ensure compliance with AWS service terms and Kraken OCR licensing when using in production environments.

---

**Need Help?** Check the troubleshooting section above or review the detailed specifications in `.kiro/specs/pdf-ocr-processor/`.