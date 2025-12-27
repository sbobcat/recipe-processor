#!/usr/bin/env python3
"""
Kraken OCR processor using only Python libraries
No system dependencies required except Kraken itself
"""

import subprocess
import json
from pathlib import Path
import sys
import shutil
import io

try:
    import fitz  # PyMuPDF for PDF handling
    from PIL import Image
except ImportError:
    print("Missing required packages. Install with:")
    print("pip install PyMuPDF Pillow")
    sys.exit(1)

class KrakenProcessorPythonOnly:
    def __init__(self, segmentation_model="blla.mlmodel", recognition_model="McCATMuS_nfd_nofix_V1.mlmodel"):
        """Initialize with the correct model names from your testing."""
        self.segmentation_model = segmentation_model
        self.recognition_model = recognition_model
        
        # Check if Kraken is available
        if not shutil.which("kraken"):
            print("Kraken not found. Make sure it's installed and in PATH.")
            sys.exit(1)
    
    def extract_pdf_pages_python(self, pdf_path, output_dir):
        """Extract PDF pages using PyMuPDF (pure Python)."""
        images_dir = Path(output_dir) / "page_images"
        images_dir.mkdir(exist_ok=True)
        
        print("Extracting pages from PDF using PyMuPDF...")
        
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(str(pdf_path))
            image_files = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Render page to image at high resolution (300 DPI equivalent)
                mat = fitz.Matrix(300/72, 300/72)  # 300 DPI scaling
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # Save as PNG
                image_path = images_dir / f"page-{page_num+1:03d}.png"
                pix.save(str(image_path))
                image_files.append(image_path)
                
                print(f"  Extracted page {page_num+1}")
            
            doc.close()
            print(f"Extracted {len(image_files)} pages using PyMuPDF")
            return image_files
            
        except Exception as e:
            print(f"Error extracting PDF pages: {e}")
            return []
    
    def process_single_page(self, image_path, output_dir, page_num):
        """Process a single page image with Kraken OCR."""
        image_path = Path(image_path)
        output_dir = Path(output_dir)
        
        # Output files
        text_output = output_dir / f"page_{page_num:03d}_text.txt"
        
        print(f"  Processing page {page_num}: {image_path.name}")
        
        # Correct Kraken command structure based on your testing:
        # kraken -i <imagefilename> <textoutputfilename> segment -bl -i blla.mlmodel ocr -m McCATMuS_nfd_nofix_V1.mlmodel
        ocr_cmd = [
            "kraken",
            "-i", str(image_path),
            str(text_output),
            "segment",
            "-bl",
            "-i", "blla.mlmodel",
            "ocr", 
            "-m", "McCATMuS_nfd_nofix_V1.mlmodel"
        ]
        
        result = subprocess.run(ocr_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Read the OCR result
            if text_output.exists():
                with open(text_output, 'r', encoding='utf-8') as f:
                    ocr_text = f.read().strip()
            else:
                ocr_text = ""
            
            return {
                'page_number': page_num,
                'image_file': str(image_path),
                'text_file': str(text_output),
                'text': ocr_text,
                'success': True
            }
        else:
            print(f"    ✗ Error processing page {page_num}: {result.stderr}")
            return {
                'page_number': page_num,
                'image_file': str(image_path),
                'text_file': str(text_output),
                'text': "",
                'success': False,
                'error': result.stderr
            }
    
    def process_pdf_with_kraken(self, pdf_path, output_dir):
        """Process PDF using Kraken OCR with Python-only PDF extraction."""
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print(f"Processing: {pdf_path}")
        print(f"Output directory: {output_dir}")
        print(f"Using recognition model: {self.recognition_model}")
        
        # Step 1: Extract PDF pages using PyMuPDF
        image_files = self.extract_pdf_pages_python(pdf_path, output_dir)
        
        if not image_files:
            print("No images extracted from PDF")
            return False
        
        # Step 2: Process each page with Kraken OCR
        all_results = []
        
        for i, image_file in enumerate(image_files, 1):
            result = self.process_single_page(image_file, output_dir, i)
            all_results.append(result)
            
            if result['success']:
                print(f"    ✓ Page {i} processed successfully")
            else:
                print(f"    ✗ Page {i} failed")
        
        # Step 3: Create combined outputs
        self._create_combined_outputs(pdf_path, output_dir, all_results)
        
        return True
    
    def _create_combined_outputs(self, pdf_path, output_dir, results):
        """Create combined text file and JSON results."""
        combined_text_file = output_dir / "all_pages_combined.txt"
        results_json_file = output_dir / "processing_results.json"
        
        # Write combined text
        with open(combined_text_file, 'w', encoding='utf-8') as f:
            f.write("Ann's Recipes - Kraken OCR Results\n")
            f.write("=" * 50 + "\n")
            f.write(f"Source PDF: {pdf_path.name}\n")
            f.write(f"Recognition Model: {self.recognition_model}\n")
            f.write(f"Total Pages: {len(results)}\n")
            f.write(f"Successful Pages: {len([r for r in results if r['success']])}\n")
            f.write("=" * 50 + "\n\n")
            
            for result in results:
                f.write(f"PAGE {result['page_number']}\n")
                f.write("-" * 20 + "\n")
                if result['success']:
                    f.write(result['text'])
                    if not result['text'].strip():
                        f.write("[No text detected on this page]")
                else:
                    f.write(f"[OCR Error: {result.get('error', 'Unknown error')}]")
                f.write("\n\n" + "=" * 50 + "\n\n")
        
        # Write JSON results
        summary = {
            'pdf_file': str(pdf_path),
            'total_pages': len(results),
            'successful_pages': len([r for r in results if r['success']]),
            'failed_pages': len([r for r in results if not r['success']]),
            'segmentation_model': self.segmentation_model,
            'recognition_model': self.recognition_model,
            'pages': results
        }
        
        with open(results_json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Processing complete!")
        print(f"📄 Combined text: {combined_text_file}")
        print(f"📊 Results JSON: {results_json_file}")
        print(f"📈 Success rate: {summary['successful_pages']}/{summary['total_pages']} pages")

def main():
    """Main processing function."""
    # Windows path converted to WSL path
    wsl_pdf_path = "/mnt/c/Users/steph/OneDrive/Documents/Scanned Documents/annsrecipes/Anns_Complete_Recipe_Book.pdf"
    wsl_output_dir = "/mnt/c/Users/steph/OneDrive/Documents/Scanned Documents/annsrecipes/kraken_output"
    
    # Check if PDF exists
    if not Path(wsl_pdf_path).exists():
        print(f"PDF not found at: {wsl_pdf_path}")
        print("Make sure you've combined your PDFs first!")
        sys.exit(1)
    
    try:
        # Initialize processor
        print("Initializing Kraken processor (Python-only version)...")
        processor = KrakenProcessorPythonOnly()
        
        # Process the PDF
        success = processor.process_pdf_with_kraken(wsl_pdf_path, wsl_output_dir)
        
        if success:
            print("\n🎉 Kraken OCR processing complete!")
            print(f"Check your results in: {wsl_output_dir}")
        else:
            print("❌ Processing failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()