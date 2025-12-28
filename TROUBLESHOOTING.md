# Troubleshooting Guide

Common issues and solutions for the PDF OCR Processor.

## 🚨 Critical Issues

### PowerShell Execution Policy
**Error:** "Execution of scripts is disabled on this system"
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy to allow scripts (run as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: bypass for single script
powershell -ExecutionPolicy Bypass -File .\image_combinor\combine_recipe_pdfs.ps1
```

### Missing Dependencies
**Error:** Various "module not found" errors
```bash
# Install all Python dependencies at once
pip install PyMuPDF Pillow python-docx boto3

# If pip fails, try:
python -m pip install --upgrade pip
python -m pip install PyMuPDF Pillow python-docx boto3

# For PowerShell module:
Install-Module PSWritePDF -Force -AllowClobber
```

## 📄 PDF Combination Issues

### File Not Found Errors
**Error:** "No SCN_*.pdf files found"

**Solutions:**
1. **Check file naming:** Files must be named `SCN_0000.pdf`, `SCN_0001.pdf`, etc.
2. **Verify path:** Ensure the input folder path is correct
3. **Check permissions:** Make sure you can read the files

```powershell
# Test file access
Get-ChildItem "C:\your\path\*.pdf" | Select-Object Name, Length
```

### PDF Corruption Issues
**Error:** "Failed to process PDF" or "Invalid PDF"

**Solutions:**
1. **Test individual files:** Open each PDF manually to verify they're not corrupted
2. **Re-scan damaged files:** If a file is corrupted, re-scan the original document
3. **Check file sizes:** Very small files (< 1KB) are likely corrupted

```powershell
# Check for suspiciously small files
Get-ChildItem "C:\your\path\*.pdf" | Where-Object {$_.Length -lt 1024} | Select-Object Name, Length
```

### Memory Issues with Large Files
**Error:** "Out of memory" or system slowdown

**Solutions:**
1. **Process in batches:** Combine smaller groups of PDFs first
2. **Close other applications:** Free up system memory
3. **Use 64-bit PowerShell:** Ensure you're using 64-bit version

```powershell
# Check PowerShell architecture
[Environment]::Is64BitProcess
```

## 🔧 AWS Textract Issues

### Credential Problems
**Error:** "Unable to locate credentials" or "Access denied"

**Solutions:**
1. **Configure AWS CLI:**
   ```bash
   aws configure
   # Enter: Access Key, Secret Key, Region (us-east-1), Format (json)
   ```

2. **Test credentials:**
   ```bash
   aws sts get-caller-identity
   ```

3. **Check permissions:** Ensure your AWS user has Textract permissions

### Rate Limiting
**Error:** "ThrottlingException" or "Rate exceeded"

**Solutions:**
1. **Add delays:** Modify the script to add delays between API calls
2. **Use smaller batches:** Process fewer pages at once
3. **Check service limits:** Review AWS Textract quotas in your region

```python
# Add delay between pages (in aws_processor/kraken_alternative_aws.py)
import time
# After each page processing:
time.sleep(1)  # 1 second delay
```

### Image Size Issues
**Error:** "InvalidParameterException: Request has invalid image"

**Solutions:**
1. **Check image size:** AWS Textract has a 10MB limit per image
2. **Reduce resolution:** Lower the DPI in the script if needed
3. **Split large PDFs:** Process very large documents in sections

```python
# Reduce image resolution (in pdf_to_images method)
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Reduced from 3,3 to 2,2
```

## 🐧 WSL and Kraken Issues

### WSL Installation Problems
**Error:** "WSL is not installed" or "Feature not enabled"

**Solutions:**
1. **Enable WSL feature:**
   ```powershell
   # Run as Administrator
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

2. **Install WSL:**
   ```powershell
   wsl --install
   # Restart computer when prompted
   ```

3. **Update WSL:**
   ```powershell
   wsl --update
   ```

### Kraken Installation Issues
**Error:** "kraken: command not found"

**Solutions:**
1. **Install in WSL:**
   ```bash
   # In WSL terminal
   sudo apt update
   sudo apt install python3-pip
   pip3 install kraken
   ```

2. **Check PATH:**
   ```bash
   echo $PATH
   which kraken
   ```

3. **Add to PATH if needed:**
   ```bash
   echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
   source ~/.bashrc
   ```

### Model Download Issues
**Error:** "Model not found" or download failures

**Solutions:**
1. **Manual model download:**
   ```bash
   # Download specific models
   kraken get 10.5281/zenodo.2577813  # blla.mlmodel
   kraken get 10.5281/zenodo.4274889  # McCATMuS_nfd_nofix_V1.mlmodel
   ```

2. **Check model location:**
   ```bash
   ls ~/.kraken/
   kraken list
   ```

3. **Alternative download:**
   ```bash
   # If kraken get fails, download manually from Zenodo
   wget https://zenodo.org/record/2577813/files/blla.mlmodel
   mv blla.mlmodel ~/.kraken/
   ```

### File Path Issues in WSL
**Error:** "No such file or directory" for Windows paths

**Solutions:**
1. **Use correct WSL paths:**
   - Windows: `C:\Users\name\file.pdf`
   - WSL: `/mnt/c/Users/name/file.pdf`

2. **Check file permissions:**
   ```bash
   ls -la /mnt/c/path/to/file.pdf
   chmod 644 /mnt/c/path/to/file.pdf  # If needed
   ```

3. **Verify WSL can access Windows files:**
   ```bash
   ls /mnt/c/
   ```

## 📝 Review Document Generation Issues

### Word Document Creation Failures
**Error:** "Failed to create document" or "Permission denied"

**Solutions:**
1. **Close existing documents:** Ensure no Word documents with the same name are open
2. **Check disk space:** Ensure adequate free space (documents can be 100MB+)
3. **Verify python-docx:**
   ```bash
   pip install --upgrade python-docx
   ```

### Image Loading Issues
**Error:** "Image not found" or "Failed to add image"

**Solutions:**
1. **Check image paths:** Verify the OCR output contains correct image file paths
2. **Verify images exist:**
   ```python
   # Check if images were created during OCR
   import os
   image_dir = "path/to/page_images"
   print(os.listdir(image_dir))
   ```

3. **Image format issues:** Ensure images are in PNG format

### Large Document Performance
**Issue:** Slow document generation or system freezing

**Solutions:**
1. **Process in batches:** Generate documents for smaller page ranges
2. **Reduce image quality:** Lower the image resolution in OCR processing
3. **Monitor memory usage:** Close other applications during generation

## 🔍 Debugging Tips

### Enable Verbose Logging
Add debug prints to scripts to track progress:

```python
# Add to any Python script
import logging
logging.basicConfig(level=logging.DEBUG)
print(f"Processing file: {file_path}")
print(f"Current step: {step_name}")
```

### Test Individual Components
Test each component separately:

```powershell
# Test PDF combination only
.\image_combinor\combine_recipe_pdfs.ps1 -DryRun

# Test single page OCR
# Edit scripts to process only first page
```

### Check System Resources
Monitor system performance during processing:

```powershell
# Check memory usage
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check disk space
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace/1GB,2)}}
```

## 📞 Getting Help

### Before Asking for Help
1. **Check this troubleshooting guide**
2. **Review error messages carefully**
3. **Test with a small sample first**
4. **Verify all dependencies are installed**

### Information to Include
When reporting issues, include:
- **Operating system version**
- **Python version** (`python --version`)
- **PowerShell version** (`$PSVersionTable.PSVersion`)
- **Complete error message**
- **Steps to reproduce the issue**
- **File sizes and types being processed**

### Log Files
Check these locations for additional error information:
- **PowerShell errors:** Check the PowerShell console output
- **Python errors:** Look for stack traces in the terminal
- **AWS errors:** Check AWS CloudTrail logs if needed
- **WSL errors:** Check `/var/log/` in WSL for system issues

---

**Still having issues?** Review the main [README.md](README.md) for detailed configuration options or check the project specifications in `.kiro/specs/pdf-ocr-processor/`.