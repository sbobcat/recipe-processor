# Quick Setup Guide

This guide helps you get the PDF OCR Processor running quickly on your Windows system.

## ⚡ 5-Minute Setup

### 1. Install Python Dependencies
```bash
pip install PyMuPDF Pillow python-docx boto3
```

### 2. Install PowerShell Module
```powershell
# Run PowerShell as Administrator
Install-Module PSWritePDF -Force
```

### 3. Choose Your OCR Method

#### Option A: AWS Textract (Cloud-based, Recommended)
```bash
# Install AWS CLI from: https://aws.amazon.com/cli/
aws configure
# Enter your AWS credentials and region (us-east-1 recommended)
```

#### Option B: Kraken OCR (Local processing)
```powershell
# Install WSL
wsl --install
# Restart computer, then in WSL terminal:
sudo apt update && sudo apt install python3-pip
pip3 install kraken
```

## 🎯 First Run

### 1. Update File Paths
Edit these files with your actual paths:

**For PDF Combination:**
- `image_combinor/combine_recipe_pdfs.ps1` - Line 8: Update `$InputFolder`

**For AWS Processing:**
- `aws_processor/kraken_alternative_aws.py` - Lines 108-109: Update paths

**For Kraken Processing:**
- `local_processor/process_recipes_kraken_python_only.py` - Lines 156-157: Update paths

### 2. Test PDF Combination
```powershell
# Dry run first to verify file order
.\image_combinor\combine_recipe_pdfs.ps1 -DryRun

# If order looks good, combine for real
.\image_combinor\combine_recipe_pdfs.ps1
```

### 3. Run OCR Processing

**AWS Textract:**
```bash
python aws_processor/kraken_alternative_aws.py
```

**Kraken OCR (in WSL):**
```bash
python3 local_processor/process_recipes_kraken_python_only.py
```

### 4. Generate Review Document
```bash
# For AWS results
python aws_processor/aws_textract_sidebyside_generator.py

# For Kraken results
python local_processor/kraken_sidebyside_generator.py
```

## 🔧 Common Setup Issues

**"PSWritePDF not found"**
```powershell
# Try installing with different options
Install-Module PSWritePDF -Force -AllowClobber -Scope CurrentUser
```

**"AWS credentials not configured"**
```bash
# Verify configuration
aws sts get-caller-identity
# If fails, run: aws configure
```

**"Kraken not found in WSL"**
```bash
# Verify installation
which kraken
# If not found: pip3 install kraken
```

**"Permission denied on files"**
- Run PowerShell as Administrator
- Check file permissions
- Ensure files aren't open in other applications

## 📋 Checklist

- [ ] Python 3.8+ installed
- [ ] Required Python packages installed (`pip install PyMuPDF Pillow python-docx boto3`)
- [ ] PSWritePDF PowerShell module installed
- [ ] AWS CLI configured (for AWS processing) OR WSL with Kraken installed (for local processing)
- [ ] File paths updated in scripts
- [ ] Test data available (SCN_*.pdf files)

## 🎉 You're Ready!

Once setup is complete, see the main [README.md](README.md) for detailed usage instructions and troubleshooting.

---

**Quick Test:** Run `.\image_combinor\combine_recipe_pdfs.ps1 -DryRun` to verify your setup is working.