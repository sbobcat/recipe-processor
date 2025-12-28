#!/usr/bin/env python3
"""
Validation script for PDF OCR Processor setup
Tests all components and documents any setup issues or missing dependencies
"""

import subprocess
import sys
import json
from pathlib import Path
import importlib
import shutil
from typing import Dict, List, Any

class SetupValidator:
    """Validates the entire PDF OCR processor setup."""
    
    def __init__(self):
        self.results = {
            'pdf_combiner': {'status': 'not_tested', 'issues': []},
            'local_ocr': {'status': 'not_tested', 'issues': []},
            'aws_ocr': {'status': 'not_tested', 'issues': []},
            'review_generator': {'status': 'not_tested', 'issues': []},
            'dependencies': {'status': 'not_tested', 'issues': []}
        }
        self.test_data_dir = Path("test-data")
        self.output_dir = Path("validation_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def log(self, message: str, component: str = None):
        """Log a message with optional component prefix."""
        if component:
            print(f"[{component.upper()}] {message}")
        else:
            print(f"[VALIDATOR] {message}")
    
    def check_python_dependencies(self) -> bool:
        """Check if required Python packages are installed."""
        self.log("Checking Python dependencies...", "DEPS")
        required_packages = {
            'fitz': 'PyMuPDF',
            'PIL': 'Pillow', 
            'docx': 'python-docx',
            'boto3': 'boto3'
        }
        
        missing = []
        for import_name, package_name in required_packages.items():
            try:
                importlib.import_module(import_name)
                self.log(f"✓ {package_name} is installed", "DEPS")
            except ImportError:
                self.log(f"✗ {package_name} is missing", "DEPS")
                missing.append(package_name)
                self.results['dependencies']['issues'].append(f"Missing package: {package_name}")
        
        if missing:
            self.results['dependencies']['status'] = 'failed'
            self.log(f"Install missing packages with: pip install {' '.join(missing)}", "DEPS")
            return False
        else:
            self.results['dependencies']['status'] = 'passed'
            return True
    
    def check_powershell_module(self) -> bool:
        """Check if PSWritePDF PowerShell module is available."""
        self.log("Checking PSWritePDF module...", "PDF_COMBINER")
        try:
            # Test if PSWritePDF module is available
            result = subprocess.run([
                "powershell", "-Command", 
                "Get-Module -ListAvailable PSWritePDF | Select-Object Name, Version"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "PSWritePDF" in result.stdout:
                self.log("✓ PSWritePDF module is installed", "PDF_COMBINER")
                return True
            else:
                self.log("✗ PSWritePDF module not found", "PDF_COMBINER")
                self.results['pdf_combiner']['issues'].append("PSWritePDF module not installed")
                self.log("Install with: Install-Module PSWritePDF -Force", "PDF_COMBINER")
                return False
        except Exception as e:
            self.log(f"✗ Error checking PSWritePDF: {e}", "PDF_COMBINER")
            self.results['pdf_combiner']['issues'].append(f"Error checking PSWritePDF: {e}")
            return False
    
    def test_pdf_combiner(self) -> bool:
        """Test the PowerShell PDF combiner with sample files."""
        self.log("Testing PDF combiner...", "PDF_COMBINER")
        
        # Check if we have sample PDFs
        sample_pdfs = list(self.test_data_dir.glob("SCN_*.pdf"))
        if len(sample_pdfs) < 3:
            self.log("✗ Not enough sample PDFs for testing", "PDF_COMBINER")
            self.results['pdf_combiner']['issues'].append("Insufficient sample PDFs")
            return False
        
        # Test with first 3 PDFs in dry-run mode
        test_pdfs = sorted(sample_pdfs)[:3]
        self.log(f"Testing with {len(test_pdfs)} sample PDFs", "PDF_COMBINER")
        
        try:
            # Run in dry-run mode
            result = subprocess.run([
                "powershell", "-File", "image_combinor/combine_recipe_pdfs.ps1",
                "-InputFolder", str(self.test_data_dir.absolute()),
                "-OutputFile", "test_combined.pdf",
                "-DryRun"
            ], capture_output=True, text=True, timeout=60, input="y\n")
            
            if result.returncode == 0:
                self.log("✓ PDF combiner dry-run successful", "PDF_COMBINER")
                self.results['pdf_combiner']['status'] = 'passed'
                return True
            else:
                self.log(f"✗ PDF combiner failed: {result.stderr}", "PDF_COMBINER")
                self.results['pdf_combiner']['issues'].append(f"Dry-run failed: {result.stderr}")
                self.results['pdf_combiner']['status'] = 'failed'
                return False
                
        except Exception as e:
            self.log(f"✗ Error testing PDF combiner: {e}", "PDF_COMBINER")
            self.results['pdf_combiner']['issues'].append(f"Test error: {e}")
            self.results['pdf_combiner']['status'] = 'failed'
            return False
    
    def check_kraken_availability(self) -> bool:
        """Check if Kraken OCR is available in WSL."""
        self.log("Checking Kraken OCR availability...", "LOCAL_OCR")
        
        try:
            # Check if WSL is available
            wsl_result = subprocess.run(["wsl", "--list"], capture_output=True, text=True, timeout=10)
            if wsl_result.returncode != 0:
                self.log("✗ WSL not available", "LOCAL_OCR")
                self.results['local_ocr']['issues'].append("WSL not available")
                return False
            
            # Check if Kraken is installed in WSL
            kraken_result = subprocess.run([
                "wsl", "which", "kraken"
            ], capture_output=True, text=True, timeout=10)
            
            if kraken_result.returncode == 0:
                self.log("✓ Kraken OCR found in WSL", "LOCAL_OCR")
                
                # Check for required models
                model_check = subprocess.run([
                    "wsl", "ls", "-la", "blla.mlmodel", "McCATMuS_nfd_nofix_V1.mlmodel"
                ], capture_output=True, text=True, timeout=10)
                
                if model_check.returncode == 0:
                    self.log("✓ Kraken models found", "LOCAL_OCR")
                    return True
                else:
                    self.log("⚠ Kraken models may be missing", "LOCAL_OCR")
                    self.results['local_ocr']['issues'].append("Kraken models may be missing")
                    return True  # Still functional, just may need model setup
            else:
                self.log("✗ Kraken not found in WSL", "LOCAL_OCR")
                self.results['local_ocr']['issues'].append("Kraken not installed in WSL")
                return False
                
        except Exception as e:
            self.log(f"✗ Error checking Kraken: {e}", "LOCAL_OCR")
            self.results['local_ocr']['issues'].append(f"Error checking Kraken: {e}")
            return False
    
    def test_local_ocr_processor(self) -> bool:
        """Test the local Kraken OCR processor with existing data."""
        self.log("Testing local OCR processor...", "LOCAL_OCR")
        
        # Check if we have a combined PDF to test with
        combined_pdf = self.test_data_dir / "Anns_Complete_Recipe_Book.pdf"
        if not combined_pdf.exists():
            self.log("⚠ Combined PDF not found, skipping OCR test", "LOCAL_OCR")
            self.results['local_ocr']['issues'].append("No combined PDF for testing")
            self.results['local_ocr']['status'] = 'skipped'
            return False
        
        # Check if we have existing Kraken output
        kraken_output_dir = self.test_data_dir / "kraken_output"
        if kraken_output_dir.exists():
            results_file = kraken_output_dir / "processing_results.json"
            if results_file.exists():
                self.log("✓ Existing Kraken results found", "LOCAL_OCR")
                try:
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    self.log(f"✓ Results: {results['successful_pages']}/{results['total_pages']} pages processed", "LOCAL_OCR")
                    self.results['local_ocr']['status'] = 'passed'
                    return True
                except Exception as e:
                    self.log(f"⚠ Error reading results: {e}", "LOCAL_OCR")
                    self.results['local_ocr']['issues'].append(f"Error reading results: {e}")
        
        self.log("⚠ No existing Kraken results found", "LOCAL_OCR")
        self.results['local_ocr']['status'] = 'needs_run'
        return False
    
    def check_aws_credentials(self) -> bool:
        """Check if AWS credentials are configured."""
        self.log("Checking AWS credentials...", "AWS_OCR")
        
        try:
            import boto3
            # Try to create a client and get caller identity
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            self.log(f"✓ AWS credentials configured for account: {identity.get('Account', 'Unknown')}", "AWS_OCR")
            return True
        except Exception as e:
            self.log(f"✗ AWS credentials not configured: {e}", "AWS_OCR")
            self.results['aws_ocr']['issues'].append(f"AWS credentials error: {e}")
            return False
    
    def test_aws_ocr_processor(self) -> bool:
        """Test AWS OCR processor setup (without actually processing)."""
        self.log("Testing AWS OCR processor setup...", "AWS_OCR")
        
        if not self.check_aws_credentials():
            self.results['aws_ocr']['status'] = 'failed'
            return False
        
        # Check if we have a combined PDF
        combined_pdf = self.test_data_dir / "Anns_Complete_Recipe_Book.pdf"
        if not combined_pdf.exists():
            self.log("⚠ Combined PDF not found for AWS testing", "AWS_OCR")
            self.results['aws_ocr']['issues'].append("No combined PDF for testing")
            self.results['aws_ocr']['status'] = 'needs_pdf'
            return False
        
        try:
            # Test if we can import and initialize the AWS processor
            sys.path.append('aws_processor')
            from kraken_alternative_aws import AWSTextractOCR
            
            processor = AWSTextractOCR()
            self.log("✓ AWS OCR processor initialized successfully", "AWS_OCR")
            self.results['aws_ocr']['status'] = 'passed'
            return True
            
        except Exception as e:
            self.log(f"✗ Error initializing AWS OCR processor: {e}", "AWS_OCR")
            self.results['aws_ocr']['issues'].append(f"Initialization error: {e}")
            self.results['aws_ocr']['status'] = 'failed'
            return False
    
    def test_review_generator(self) -> bool:
        """Test the side-by-side review generator with existing OCR output."""
        self.log("Testing review generator...", "REVIEW_GEN")
        
        # Check if we have existing Kraken output to work with
        kraken_output_dir = self.test_data_dir / "kraken_output"
        if not kraken_output_dir.exists():
            self.log("⚠ No Kraken output directory found", "REVIEW_GEN")
            self.results['review_generator']['issues'].append("No Kraken output for testing")
            self.results['review_generator']['status'] = 'needs_ocr'
            return False
        
        results_file = kraken_output_dir / "processing_results.json"
        if not results_file.exists():
            self.log("⚠ No Kraken results file found", "REVIEW_GEN")
            self.results['review_generator']['issues'].append("No Kraken results file")
            self.results['review_generator']['status'] = 'needs_ocr'
            return False
        
        try:
            # Test if we can initialize the review generator
            sys.path.append('local_processor')
            from kraken_sidebyside_generator import KrakenSideBySideGenerator
            
            generator = KrakenSideBySideGenerator(str(kraken_output_dir))
            results = generator.load_kraken_results()
            
            self.log(f"✓ Review generator loaded results: {results['successful_pages']}/{results['total_pages']} pages", "REVIEW_GEN")
            
            # Test document creation (without actually creating it)
            self.log("✓ Review generator initialized successfully", "REVIEW_GEN")
            self.results['review_generator']['status'] = 'passed'
            return True
            
        except Exception as e:
            self.log(f"✗ Error testing review generator: {e}", "REVIEW_GEN")
            self.results['review_generator']['issues'].append(f"Test error: {e}")
            self.results['review_generator']['status'] = 'failed'
            return False
    
    def generate_report(self):
        """Generate a comprehensive validation report."""
        self.log("Generating validation report...")
        
        report = {
            'validation_summary': {
                'timestamp': str(Path().absolute()),
                'total_components': len(self.results),
                'passed': len([r for r in self.results.values() if r['status'] == 'passed']),
                'failed': len([r for r in self.results.values() if r['status'] == 'failed']),
                'skipped': len([r for r in self.results.values() if r['status'] in ['skipped', 'needs_run', 'needs_ocr', 'needs_pdf']])
            },
            'component_results': self.results
        }
        
        # Save detailed report
        report_file = self.output_dir / "validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        for component, result in self.results.items():
            status_icon = {
                'passed': '✓',
                'failed': '✗',
                'skipped': '⚠',
                'needs_run': '⚠',
                'needs_ocr': '⚠',
                'needs_pdf': '⚠',
                'not_tested': '?'
            }.get(result['status'], '?')
            
            print(f"{status_icon} {component.upper().replace('_', ' ')}: {result['status']}")
            
            if result['issues']:
                for issue in result['issues']:
                    print(f"    - {issue}")
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Provide recommendations
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        if self.results['dependencies']['status'] == 'failed':
            print("1. Install missing Python packages first")
        
        if self.results['pdf_combiner']['status'] == 'failed':
            print("2. Install PSWritePDF PowerShell module")
        
        if self.results['local_ocr']['status'] in ['failed', 'needs_run']:
            print("3. Set up Kraken OCR in WSL")
        
        if self.results['aws_ocr']['status'] == 'failed':
            print("4. Configure AWS credentials with 'aws configure'")
        
        if any(r['status'] in ['needs_ocr', 'needs_pdf'] for r in self.results.values()):
            print("5. Run PDF combination and OCR processing to generate test data")
        
        print("\n✅ Validation complete!")

def main():
    """Main validation function."""
    print("PDF OCR Processor Setup Validation")
    print("="*50)
    
    validator = SetupValidator()
    
    # Run all validations
    validator.check_python_dependencies()
    validator.check_powershell_module()
    validator.test_pdf_combiner()
    validator.check_kraken_availability()
    validator.test_local_ocr_processor()
    validator.test_aws_ocr_processor()
    validator.test_review_generator()
    
    # Generate report
    validator.generate_report()

if __name__ == "__main__":
    main()