#!/usr/bin/env python3
"""
Create a mock processing_results.json file from existing Kraken output
"""

import json
from pathlib import Path

def create_mock_results():
    """Create a mock results file from existing Kraken output."""
    kraken_dir = Path("test-data/kraken_output")
    
    # Find all text files
    text_files = list(kraken_dir.glob("page_*_text.txt"))
    text_files.sort()
    
    print(f"Found {len(text_files)} text files")
    
    # Create results structure
    results = {
        "pdf_file": "test-data/Anns_Complete_Recipe_Book.pdf",
        "total_pages": len(text_files),
        "successful_pages": len(text_files),
        "failed_pages": 0,
        "segmentation_model": "blla.mlmodel",
        "recognition_model": "McCATMuS_nfd_nofix_V1.mlmodel",
        "pages": []
    }
    
    # Process each text file
    for i, text_file in enumerate(text_files, 1):
        # Read the text content
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                text_content = f.read().strip()
        except:
            text_content = ""
        
        # Create page result
        page_result = {
            "page_number": i,
            "image_file": f"test-data/kraken_output/page_images/page-{i:03d}.png",
            "text_file": str(text_file),
            "text": text_content,
            "success": True
        }
        
        results["pages"].append(page_result)
        print(f"Added page {i}: {len(text_content)} characters")
    
    # Save results file
    results_file = kraken_dir / "processing_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Created mock results file: {results_file}")
    return results_file

if __name__ == "__main__":
    create_mock_results()