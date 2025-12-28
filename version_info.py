#!/usr/bin/env python3
"""
Version Information and System Check for PDF OCR Processor
"""

import sys
from pathlib import Path
import subprocess
import importlib.util

def get_version():
    """Get the current version from VERSION file."""
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "Unknown"

def check_python_dependencies():
    """Check if required Python packages are installed."""
    required_packages = {
        'fitz': 'PyMuPDF',
        'PIL': 'Pillow', 
        'docx': 'python-docx',
        'boto3': 'boto3'
    }
    
    installed = {}
    for import_name, package_name in required_packages.items():
        try:
            spec = importlib.util.find_spec(import_name)
            if spec is not None:
                # Try to get version if possible
                try:
                    module = importlib.import_module(import_name)
                    version = getattr(module, '__version__', 'installed')
                except:
                    version = 'installed'
                installed[package_name] = version
            else:
                installed[package_name] = 'NOT INSTALLED'
        except Exception:
            installed[package_name] = 'ERROR'
    
    return installed

def check_powershell_modules():
    """Check if required PowerShell modules are available."""
    try:
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Module -ListAvailable PSWritePDF | Select-Object Name, Version'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'PSWritePDF' in result.stdout:
            return 'installed'
        else:
            return 'NOT INSTALLED'
    except Exception:
        return 'ERROR (PowerShell not available)'

def check_aws_cli():
    """Check if AWS CLI is installed and configured."""
    try:
        # Check if AWS CLI is installed
        result = subprocess.run(['aws', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return 'NOT INSTALLED'
        
        # Check if credentials are configured
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return 'installed and configured'
        else:
            return 'installed but not configured'
    except Exception:
        return 'NOT AVAILABLE'

def check_wsl_kraken():
    """Check if WSL and Kraken are available."""
    try:
        # Check if WSL is available
        result = subprocess.run(['wsl', '--list'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return 'WSL not installed'
        
        # Check if Kraken is available in WSL
        result = subprocess.run(['wsl', 'which', 'kraken'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return 'WSL and Kraken available'
        else:
            return 'WSL available, Kraken not installed'
    except Exception:
        return 'WSL not available'

def print_system_info():
    """Print comprehensive system information."""
    version = get_version()
    
    print("=" * 60)
    print(f"PDF OCR PROCESSOR - VERSION {version}")
    print("=" * 60)
    
    print(f"\n🐍 PYTHON ENVIRONMENT")
    print(f"   Python Version: {sys.version.split()[0]}")
    print(f"   Python Path: {sys.executable}")
    
    print(f"\n📦 PYTHON DEPENDENCIES")
    deps = check_python_dependencies()
    for package, status in deps.items():
        status_icon = "✅" if status not in ['NOT INSTALLED', 'ERROR'] else "❌"
        print(f"   {status_icon} {package}: {status}")
    
    print(f"\n💻 POWERSHELL MODULES")
    ps_status = check_powershell_modules()
    ps_icon = "✅" if ps_status == 'installed' else "❌"
    print(f"   {ps_icon} PSWritePDF: {ps_status}")
    
    print(f"\n☁️  AWS INTEGRATION")
    aws_status = check_aws_cli()
    aws_icon = "✅" if 'configured' in aws_status else "⚠️" if 'installed' in aws_status else "❌"
    print(f"   {aws_icon} AWS CLI: {aws_status}")
    
    print(f"\n🐧 LOCAL PROCESSING (WSL/KRAKEN)")
    wsl_status = check_wsl_kraken()
    wsl_icon = "✅" if 'Kraken available' in wsl_status else "⚠️" if 'WSL available' in wsl_status else "❌"
    print(f"   {wsl_icon} WSL/Kraken: {wsl_status}")
    
    print(f"\n📁 PROJECT FILES")
    project_files = [
        'image_combinor/combine_recipe_pdfs.ps1',
        'aws_processor/kraken_alternative_aws.py',
        'local_processor/process_recipes_kraken_python_only.py',
        'README.md',
        'CHANGELOG.md'
    ]
    
    for file_path in project_files:
        file_exists = Path(file_path).exists()
        file_icon = "✅" if file_exists else "❌"
        print(f"   {file_icon} {file_path}")
    
    print(f"\n🎯 READINESS ASSESSMENT")
    
    # Check overall readiness
    python_ready = all(status not in ['NOT INSTALLED', 'ERROR'] for status in deps.values())
    ps_ready = ps_status == 'installed'
    aws_ready = 'configured' in aws_status
    kraken_ready = 'Kraken available' in wsl_status
    
    print(f"   📄 PDF Combination: {'✅ Ready' if ps_ready else '❌ Not Ready (PSWritePDF needed)'}")
    print(f"   ☁️  AWS OCR Processing: {'✅ Ready' if python_ready and aws_ready else '❌ Not Ready (AWS CLI/credentials needed)'}")
    print(f"   🏠 Local OCR Processing: {'✅ Ready' if python_ready and kraken_ready else '❌ Not Ready (WSL/Kraken needed)'}")
    print(f"   📝 Review Generation: {'✅ Ready' if python_ready else '❌ Not Ready (Python packages needed)'}")
    
    if python_ready and (aws_ready or kraken_ready) and ps_ready:
        print(f"\n🎉 SYSTEM STATUS: READY FOR USE!")
    else:
        print(f"\n⚠️  SYSTEM STATUS: SETUP REQUIRED")
        print(f"   See SETUP_GUIDE.md for installation instructions")
    
    print("=" * 60)

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        print(get_version())
    else:
        print_system_info()

if __name__ == "__main__":
    main()