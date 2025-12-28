#!/usr/bin/env python3
"""
Test AWS OCR processor with provided credentials
"""

import sys
from pathlib import Path

# Add the aws_processor directory to path
sys.path.append('aws_processor')

try:
    from kraken_alternative_aws import AWSTextractOCR
    import boto3
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure boto3 is installed: pip install boto3")
    sys.exit(1)

def test_aws_credentials():
    """Test if AWS credentials are working."""
    print("Testing AWS credentials...")
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✓ AWS credentials working")
        print(f"  Account: {identity.get('Account', 'Unknown')}")
        print(f"  User/Role: {identity.get('Arn', 'Unknown')}")
        return True
    except Exception as e:
        print(f"✗ AWS credentials error: {e}")
        return False

def test_textract_access():
    """Test if AWS Textract service is accessible."""
    print("\nTesting AWS Textract access...")
    try:
        from PIL import Image
        import io
        
        textract = boto3.client('textract', region_name='us-east-1')
        
        # Create a simple test image with text using PIL
        img = Image.new('RGB', (200, 100), color='white')
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_data = img_bytes.getvalue()
        
        response = textract.detect_document_text(
            Document={'Bytes': img_data}
        )
        
        print("✓ AWS Textract service accessible")
        print(f"  Response received with {len(response.get('Blocks', []))} blocks")
        return True
        
    except Exception as e:
        print(f"✗ AWS Textract error: {e}")
        return False

def test_aws_processor_initialization():
    """Test if the AWS processor can be initialized."""
    print("\nTesting AWS processor initialization...")
    try:
        processor = AWSTextractOCR(region='us-east-1')
        print("✓ AWS OCR processor initialized successfully")
        return processor
    except Exception as e:
        print(f"✗ AWS processor initialization error: {e}")
        return None

def test_with_sample_pdf():
    """Test with the combined PDF if it exists."""
    print("\nTesting with sample PDF...")
    
    # Check for combined PDF
    combined_pdf = Path("test-data/Anns_Complete_Recipe_Book.pdf")
    if not combined_pdf.exists():
        print("⚠ Combined PDF not found, skipping PDF test")
        print(f"  Looking for: {combined_pdf.absolute()}")
        return False
    
    print(f"✓ Found combined PDF: {combined_pdf}")
    print(f"  Size: {combined_pdf.stat().st_size / (1024*1024):.2f} MB")
    
    # Test PDF to images conversion (just first page)
    try:
        processor = AWSTextractOCR(region='us-east-1')
        
        # Test PDF extraction
        import fitz
        doc = fitz.open(str(combined_pdf))
        print(f"✓ PDF opened successfully: {len(doc)} pages")
        
        # Extract just the first page as a test
        if len(doc) > 0:
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 216 DPI
            img_data = pix.tobytes("png")
            print(f"✓ First page extracted: {len(img_data)} bytes")
            
            # Test OCR on first page (this will use actual Textract credits)
            print("  Testing OCR on first page (this uses AWS credits)...")
            ocr_result = processor.extract_handwritten_text(img_data)
            
            if 'error' in ocr_result:
                print(f"✗ OCR error: {ocr_result['error']}")
                return False
            else:
                print(f"✓ OCR successful")
                print(f"  Confidence: {ocr_result['confidence']:.1f}%")
                print(f"  Text length: {len(ocr_result['text'])} characters")
                print(f"  Lines detected: {len(ocr_result['lines'])}")
                print(f"  Words detected: {len(ocr_result['words'])}")
                
                # Show first few lines of text
                if ocr_result['text']:
                    preview = ocr_result['text'][:200]
                    print(f"  Text preview: {preview}...")
                
                return True
        
        doc.close()
        
    except Exception as e:
        print(f"✗ PDF processing error: {e}")
        return False

def main():
    """Main test function."""
    print("AWS OCR Processor Validation")
    print("=" * 40)
    
    # Test AWS credentials
    if not test_aws_credentials():
        print("\n❌ AWS credentials test failed")
        return
    
    # Test Textract access
    if not test_textract_access():
        print("\n❌ AWS Textract access test failed")
        return
    
    # Test processor initialization
    processor = test_aws_processor_initialization()
    if not processor:
        print("\n❌ AWS processor initialization failed")
        return
    
    # Test with sample PDF
    pdf_success = test_with_sample_pdf()
    
    print("\n" + "=" * 40)
    print("AWS OCR VALIDATION SUMMARY")
    print("=" * 40)
    print("✓ AWS credentials: Working")
    print("✓ AWS Textract access: Working") 
    print("✓ AWS processor initialization: Working")
    
    if pdf_success:
        print("✓ PDF processing: Working")
        print("\n🎉 AWS OCR processor is fully functional!")
    else:
        print("⚠ PDF processing: Needs combined PDF or had errors")
        print("\n✅ AWS OCR processor setup is working, ready for PDF processing")

if __name__ == "__main__":
    main()