#!/usr/bin/env python3
"""
Configuration Template for PDF OCR Processor
Copy this file to config.py and customize the paths for your environment
"""

from pathlib import Path

# =============================================================================
# FILE PATHS - UPDATE THESE FOR YOUR ENVIRONMENT
# =============================================================================

# PDF Input and Output Paths
PDF_INPUT_DIRECTORY = r"C:\Users\YourName\Documents\ScannedPDFs"
COMBINED_PDF_NAME = "Your_Recipe_Book.pdf"
COMBINED_PDF_PATH = Path(PDF_INPUT_DIRECTORY) / COMBINED_PDF_NAME

# Output Directories
AWS_OUTPUT_DIR = Path(PDF_INPUT_DIRECTORY) / "aws_textract_output"
KRAKEN_OUTPUT_DIR = Path(PDF_INPUT_DIRECTORY) / "kraken_output"

# WSL Paths (for Kraken processing)
# Convert Windows paths to WSL format: C:\Users\Name -> /mnt/c/Users/Name
WSL_PDF_PATH = "/mnt/c/Users/YourName/Documents/ScannedPDFs/Your_Recipe_Book.pdf"
WSL_OUTPUT_DIR = "/mnt/c/Users/YourName/Documents/ScannedPDFs/kraken_output"

# =============================================================================
# AWS CONFIGURATION
# =============================================================================

# AWS Settings
AWS_REGION = "us-east-1"  # Change if you prefer a different region
AWS_CONFIDENCE_THRESHOLD = 80  # Words below this confidence will be flagged

# =============================================================================
# KRAKEN CONFIGURATION  
# =============================================================================

# Kraken Model Settings
KRAKEN_SEGMENTATION_MODEL = "blla.mlmodel"
KRAKEN_RECOGNITION_MODEL = "McCATMuS_nfd_nofix_V1.mlmodel"

# =============================================================================
# IMAGE PROCESSING SETTINGS
# =============================================================================

# Image Resolution Settings
AWS_IMAGE_DPI = 216  # 3x scaling (Matrix(3,3)) = 216 DPI
KRAKEN_IMAGE_DPI = 300  # 300/72 scaling for Kraken

# =============================================================================
# REVIEW DOCUMENT SETTINGS
# =============================================================================

# Review Document Output Names
KRAKEN_REVIEW_DOC = "Recipe_Book_Kraken_Review.docx"
AWS_REVIEW_DOC = "Recipe_Book_AWS_Review.docx"

# Document Formatting
IMAGE_WIDTH_INCHES = 3.8
TEXT_FONT_NAME = "Calibri"
TEXT_FONT_SIZE = 10

# =============================================================================
# PROCESSING OPTIONS
# =============================================================================

# Processing Behavior
CONTINUE_ON_ERROR = True  # Continue processing other pages if one fails
SAVE_INTERMEDIATE_FILES = True  # Keep individual page text files
CREATE_COMBINED_TEXT = True  # Create single file with all text

# Progress Reporting
SHOW_PROGRESS = True  # Display progress messages during processing
VERBOSE_LOGGING = False  # Enable detailed debug logging

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def get_aws_config():
    """Get AWS processing configuration."""
    return {
        'pdf_path': COMBINED_PDF_PATH,
        'output_dir': AWS_OUTPUT_DIR,
        'region': AWS_REGION,
        'confidence_threshold': AWS_CONFIDENCE_THRESHOLD,
        'image_dpi': AWS_IMAGE_DPI
    }

def get_kraken_config():
    """Get Kraken processing configuration."""
    return {
        'pdf_path': WSL_PDF_PATH,
        'output_dir': WSL_OUTPUT_DIR,
        'segmentation_model': KRAKEN_SEGMENTATION_MODEL,
        'recognition_model': KRAKEN_RECOGNITION_MODEL,
        'image_dpi': KRAKEN_IMAGE_DPI
    }

def get_review_config(ocr_type='kraken'):
    """Get review document configuration."""
    if ocr_type.lower() == 'aws':
        output_name = AWS_REVIEW_DOC
        input_dir = AWS_OUTPUT_DIR
    else:
        output_name = KRAKEN_REVIEW_DOC
        input_dir = KRAKEN_OUTPUT_DIR
    
    return {
        'input_dir': input_dir,
        'output_name': output_name,
        'image_width': IMAGE_WIDTH_INCHES,
        'font_name': TEXT_FONT_NAME,
        'font_size': TEXT_FONT_SIZE
    }

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_paths():
    """Validate that all configured paths exist or can be created."""
    issues = []
    
    # Check input directory
    if not Path(PDF_INPUT_DIRECTORY).exists():
        issues.append(f"PDF input directory does not exist: {PDF_INPUT_DIRECTORY}")
    
    # Check combined PDF exists
    if not COMBINED_PDF_PATH.exists():
        issues.append(f"Combined PDF not found: {COMBINED_PDF_PATH}")
    
    # Check output directories can be created
    for output_dir in [AWS_OUTPUT_DIR, KRAKEN_OUTPUT_DIR]:
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            issues.append(f"Cannot create output directory {output_dir}: {e}")
    
    return issues

def print_config_summary():
    """Print a summary of the current configuration."""
    print("PDF OCR Processor Configuration Summary")
    print("=" * 50)
    print(f"Input Directory: {PDF_INPUT_DIRECTORY}")
    print(f"Combined PDF: {COMBINED_PDF_NAME}")
    print(f"AWS Output: {AWS_OUTPUT_DIR}")
    print(f"Kraken Output: {KRAKEN_OUTPUT_DIR}")
    print(f"AWS Region: {AWS_REGION}")
    print(f"Confidence Threshold: {AWS_CONFIDENCE_THRESHOLD}%")
    print(f"AWS Image DPI: {AWS_IMAGE_DPI}")
    print(f"Kraken Image DPI: {KRAKEN_IMAGE_DPI}")
    
    # Validate paths
    issues = validate_paths()
    if issues:
        print("\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"   • {issue}")
    else:
        print("\n✅ Configuration looks good!")

if __name__ == "__main__":
    print_config_summary()