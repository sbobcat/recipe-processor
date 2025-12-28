#!/usr/bin/env python3
"""
AWS Textract OCR for Handwritten Recipes
Better alternative to Kraken for Windows users with cursive text
"""

import boto3
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF
from PIL import Image
import io
import base64

class AWSTextractOCR:
    """AWS Textract OCR processor optimized for handwritten recipes."""
    
    def __init__(self, region='us-east-1'):
        """Initialize AWS Textract client."""
        try:
            self.textract = boto3.client('textract', region_name=region)
            # Test connection
            self.textract.get_caller_identity = boto3.client('sts').get_caller_identity
        except Exception as e:
            print(f"AWS setup error: {e}")
            print("Make sure you've run: aws configure")
            sys.exit(1)
    
    def pdf_to_images(self, pdf_path: Path) -> List[bytes]:
        """Convert PDF pages to high-quality images for OCR."""
        doc = fitz.open(str(pdf_path))
        images = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # High resolution for better handwriting recognition
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 216 DPI
            img_data = pix.tobytes("png")
            images.append(img_data)
        
        doc.close()
        return images
    
    def extract_handwritten_text(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Extract text using AWS Textract with handwriting detection.
        Returns both raw text and confidence scores.
        """
        try:
            # Use detect_document_text for handwriting
            response = self.textract.detect_document_text(
                Document={'Bytes': image_bytes}
            )
            
            # Extract text with confidence scores
            lines = []
            words = []
            
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    lines.append({
                        'text': block['Text'],
                        'confidence': block['Confidence']
                    })
                elif block['BlockType'] == 'WORD':
                    words.append({
                        'text': block['Text'],
                        'confidence': block['Confidence']
                    })
            
            # Combine into full text
            full_text = '\n'.join([line['text'] for line in lines])
            avg_confidence = sum([line['confidence'] for line in lines]) / len(lines) if lines else 0
            
            return {
                'text': full_text,
                'confidence': avg_confidence,
                'lines': lines,
                'words': words
            }
            
        except Exception as e:
            print(f"Textract error: {e}")
            return {
                'text': '',
                'confidence': 0,
                'lines': [],
                'words': [],
                'error': str(e)
            }
    
    def process_recipe_pdf(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Process entire recipe PDF and return structured results."""
        print(f"Processing: {pdf_path.name}")
        
        # Convert to images
        images = self.pdf_to_images(pdf_path)
        print(f"Extracted {len(images)} pages")
        
        results = {
            'pdf_name': pdf_path.name,
            'total_pages': len(images),
            'pages': []
        }
        
        # Process each page
        for i, image_bytes in enumerate(images):
            page_num = i + 1
            print(f"  OCR processing page {page_num}/{len(images)}")
            
            ocr_result = self.extract_handwritten_text(image_bytes)
            
            page_result = {
                'page_number': page_num,
                'text': ocr_result['text'],
                'confidence': ocr_result['confidence'],
                'word_count': len(ocr_result['words']),
                'has_error': 'error' in ocr_result
            }
            
            results['pages'].append(page_result)
            
            # Save individual page text
            page_file = output_dir / f"page_{page_num:03d}_ocr.txt"
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(f"Page {page_num} - Confidence: {ocr_result['confidence']:.1f}%\n")
                f.write("="*50 + "\n")
                f.write(ocr_result['text'])
                f.write("\n\n" + "="*50 + "\n")
                f.write("LOW CONFIDENCE WORDS (may need review):\n")
                
                # Flag low confidence words
                low_conf_words = [w for w in ocr_result['words'] if w['confidence'] < 80]
                if low_conf_words:
                    for word in low_conf_words:
                        f.write(f"  '{word['text']}' ({word['confidence']:.1f}%)\n")
                else:
                    f.write("  None - all words have good confidence!\n")
        
        # Save summary
        summary_file = output_dir / f"{pdf_path.stem}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    """Main processing function."""
    # Configuration
    pdf_path = Path(r"C:\Code\pers\recipe-processor\test-data\Anns_Complete_Recipe_Book.pdf")
    output_dir = Path(pdf_path.parent / "aws_textract_output")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if PDF exists
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        print("Make sure you've combined your PDFs first!")
        sys.exit(1)
    
    try:
        # Initialize processor
        processor = AWSTextractOCR()
        
        # Process the PDF
        results = processor.process_recipe_pdf(pdf_path, output_dir)
        
        # Print summary
        print(f"\n✅ Processing complete!")
        print(f"📄 Processed {results['total_pages']} pages")
        print(f"📁 Output saved to: {output_dir}")
        
        # Calculate average confidence
        avg_conf = sum([p['confidence'] for p in results['pages']]) / len(results['pages'])
        print(f"📊 Average confidence: {avg_conf:.1f}%")
        
        # Show pages with low confidence
        low_conf_pages = [p for p in results['pages'] if p['confidence'] < 70]
        if low_conf_pages:
            print(f"⚠️  {len(low_conf_pages)} pages may need extra review (low confidence)")
            for page in low_conf_pages:
                print(f"   Page {page['page_number']}: {page['confidence']:.1f}%")
        
        print(f"\n💡 Next step: Run the side-by-side generator with these results")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()