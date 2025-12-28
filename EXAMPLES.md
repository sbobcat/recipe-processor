# Usage Examples

Real-world examples of using the PDF OCR Processor for different scenarios.

## 📚 Example 1: Processing Recipe Collection

### Scenario
You have 53 scanned recipe pages (SCN_0000.pdf through SCN_0052.pdf) that you want to convert to searchable text.

### Step-by-Step Process

#### 1. Organize Your Files
```
C:\MyRecipes\
├── SCN_0000.pdf
├── SCN_0001.pdf
├── SCN_0002.pdf
├── ...
└── SCN_0052.pdf
```

#### 2. Update Configuration
Edit the PowerShell script:
```powershell
# In image_combinor/combine_recipe_pdfs.ps1, line 8:
$InputFolder = "C:\MyRecipes"
$OutputFile = "My_Recipe_Collection.pdf"
```

#### 3. Combine PDFs
```powershell
# Test first (dry run)
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\MyRecipes" -DryRun

# Output shows:
# Found 53 PDF files:
#   SCN_0000.pdf
#   SCN_0001.pdf
#   ...
# First few files in order:
#   SCN_0000.pdf
#   SCN_0001.pdf
#   SCN_0002.pdf
# Does this order look correct? (y/n): y

# If order is correct, run actual combination:
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\MyRecipes"
```

#### 4. Process with AWS Textract
```python
# Edit aws_processor/kraken_alternative_aws.py, lines 108-109:
pdf_path = Path(r"C:\MyRecipes\My_Recipe_Collection.pdf")
output_dir = Path(r"C:\MyRecipes\aws_textract_output")

# Run processing:
python aws_processor/kraken_alternative_aws.py
```

**Expected Output:**
```
Processing: My_Recipe_Collection.pdf
Extracted 53 pages
  OCR processing page 1/53
  OCR processing page 2/53
  ...
✅ Processing complete!
📄 Processed 53 pages
📁 Output saved to: C:\MyRecipes\aws_textract_output
📊 Average confidence: 82.4%
⚠️  3 pages may need extra review (low confidence)
   Page 15: 68.2%
   Page 23: 71.5%
   Page 41: 69.8%
```

#### 5. Generate Review Document
```python
# Edit aws_processor/aws_textract_sidebyside_generator.py:
aws_output_dir = r"C:\MyRecipes\aws_textract_output"

# Run generator:
python aws_processor/aws_textract_sidebyside_generator.py
```

**Result:** Word document with 53 pages, each showing original image on left and OCR text on right.

---

## 📄 Example 2: Processing Historical Documents

### Scenario
You have old handwritten documents that need OCR processing using local Kraken OCR for privacy.

#### 1. Setup WSL and Kraken
```bash
# Install WSL (one-time setup)
wsl --install

# In WSL terminal:
sudo apt update
sudo apt install python3-pip
pip3 install kraken

# Download handwriting models:
kraken get 10.5281/zenodo.2577813  # blla.mlmodel
kraken get 10.5281/zenodo.4274889  # McCATMuS_nfd_nofix_V1.mlmodel
```

#### 2. Prepare Documents
```
C:\HistoricalDocs\
├── SCN_0000.pdf  # Page 1 of document
├── SCN_0001.pdf  # Page 2 of document
├── ...
└── SCN_0025.pdf  # Page 26 of document
```

#### 3. Combine and Process
```powershell
# Combine PDFs
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\HistoricalDocs" -OutputFile "Historical_Document.pdf"
```

```python
# Edit local_processor/process_recipes_kraken_python_only.py:
wsl_pdf_path = "/mnt/c/HistoricalDocs/Historical_Document.pdf"
wsl_output_dir = "/mnt/c/HistoricalDocs/kraken_output"

# Run in WSL:
python3 local_processor/process_recipes_kraken_python_only.py
```

#### 4. Review Results
```python
# Generate review document (in Windows):
python local_processor/kraken_sidebyside_generator.py
```

---

## 🔄 Example 3: Comparing OCR Methods

### Scenario
You want to compare AWS Textract vs Kraken OCR on the same document to see which works better.

#### 1. Process with Both Methods
```bash
# First, process with AWS Textract
python aws_processor/kraken_alternative_aws.py

# Then, process with Kraken (in WSL)
python3 local_processor/process_recipes_kraken_python_only.py
```

#### 2. Generate Both Review Documents
```bash
# AWS review document
python aws_processor/aws_textract_sidebyside_generator.py

# Kraken review document  
python local_processor/kraken_sidebyside_generator.py
```

#### 3. Compare Results
You'll have two Word documents:
- `Recipe_Book_AWS_Textract_Review.docx` - AWS results with confidence scores
- `Recipe_Book_Kraken_Review.docx` - Kraken results

**Comparison Tips:**
- AWS Textract shows confidence scores for each word
- Kraken may be better for historical/stylized handwriting
- AWS is faster but requires internet connection
- Kraken runs locally (better for sensitive documents)

---

## 🛠️ Example 4: Batch Processing Multiple Documents

### Scenario
You have multiple separate document collections to process.

#### Directory Structure
```
C:\Documents\
├── Recipes\
│   ├── SCN_0000.pdf ... SCN_0052.pdf
│   └── (will create: Recipe_Collection.pdf)
├── Letters\
│   ├── SCN_0000.pdf ... SCN_0025.pdf
│   └── (will create: Letter_Collection.pdf)
└── Notes\
    ├── SCN_0000.pdf ... SCN_0018.pdf
    └── (will create: Notes_Collection.pdf)
```

#### Batch Processing Script
Create a batch script `process_all.ps1`:

```powershell
# Process Recipes
Write-Host "Processing Recipes..." -ForegroundColor Green
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\Documents\Recipes" -OutputFile "Recipe_Collection.pdf"

# Process Letters  
Write-Host "Processing Letters..." -ForegroundColor Green
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\Documents\Letters" -OutputFile "Letter_Collection.pdf"

# Process Notes
Write-Host "Processing Notes..." -ForegroundColor Green
.\image_combinor\combine_recipe_pdfs.ps1 -InputFolder "C:\Documents\Notes" -OutputFile "Notes_Collection.pdf"

Write-Host "All documents combined!" -ForegroundColor Green
```

#### Run OCR on Each Collection
```bash
# Update paths in scripts for each collection and run:
# For Recipes:
python aws_processor/kraken_alternative_aws.py  # (with Recipe_Collection.pdf path)

# For Letters:
python aws_processor/kraken_alternative_aws.py  # (with Letter_Collection.pdf path)

# For Notes:
python aws_processor/kraken_alternative_aws.py  # (with Notes_Collection.pdf path)
```

---

## 🔧 Example 5: Troubleshooting Common Issues

### Issue: Files Not in Correct Order
```powershell
# Problem: Files appear as SCN_1.pdf, SCN_10.pdf, SCN_2.pdf (wrong order)
# Solution: Rename files with leading zeros

# PowerShell script to fix naming:
Get-ChildItem "C:\MyDocs\SCN_*.pdf" | ForEach-Object {
    if ($_.Name -match "SCN_(\d+)\.pdf") {
        $number = [int]$matches[1]
        $newName = "SCN_{0:D4}.pdf" -f $number
        if ($_.Name -ne $newName) {
            Rename-Item $_.FullName $newName
            Write-Host "Renamed $($_.Name) to $newName"
        }
    }
}
```

### Issue: AWS Rate Limiting
```python
# Problem: "ThrottlingException" when processing many pages
# Solution: Add delays between API calls

# In aws_processor/kraken_alternative_aws.py, add after line 85:
import time

# In the processing loop (around line 95), add:
time.sleep(0.5)  # 500ms delay between pages
```

### Issue: Large Memory Usage
```python
# Problem: System runs out of memory with large documents
# Solution: Process in smaller batches

# Modify scripts to process only a range of pages:
# In extract_pdf_pages_python method, add:
start_page = 0  # Start from page 0
end_page = 10   # Process only first 10 pages

for page_num in range(start_page, min(end_page, len(doc))):
    # ... existing code
```

---

## 📊 Example 6: Quality Assessment

### Checking OCR Accuracy
```python
# Create a simple accuracy checker
def check_ocr_quality(text_file_path):
    """Basic quality metrics for OCR text."""
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Basic metrics
    total_chars = len(text)
    alpha_chars = sum(c.isalpha() for c in text)
    digit_chars = sum(c.isdigit() for c in text)
    space_chars = sum(c.isspace() for c in text)
    
    # Calculate ratios
    alpha_ratio = alpha_chars / total_chars if total_chars > 0 else 0
    digit_ratio = digit_chars / total_chars if total_chars > 0 else 0
    
    print(f"Text Quality Metrics for {text_file_path}:")
    print(f"  Total characters: {total_chars}")
    print(f"  Alphabetic: {alpha_chars} ({alpha_ratio:.1%})")
    print(f"  Numeric: {digit_chars} ({digit_ratio:.1%})")
    print(f"  Whitespace: {space_chars}")
    
    # Quality assessment
    if alpha_ratio > 0.7:
        print("  Quality: Good (mostly readable text)")
    elif alpha_ratio > 0.4:
        print("  Quality: Fair (some readable text)")
    else:
        print("  Quality: Poor (mostly unreadable)")

# Usage:
check_ocr_quality("output/page_001_ocr.txt")
```

---

## 💡 Pro Tips

### 1. Optimize Image Quality
```python
# For better OCR results, experiment with different DPI settings:
# Lower DPI (faster, less accurate): Matrix(2, 2) = 144 DPI
# Standard DPI (balanced): Matrix(3, 3) = 216 DPI  
# Higher DPI (slower, more accurate): Matrix(4, 4) = 288 DPI
```

### 2. Selective Processing
```python
# Process only specific pages for testing:
# In any OCR script, modify the page loop:
for page_num in range(len(doc)):
    if page_num not in [0, 5, 10]:  # Process only pages 1, 6, 11
        continue
    # ... rest of processing
```

### 3. Monitor Progress
```python
# Add progress indicators to long-running processes:
from tqdm import tqdm  # pip install tqdm

for i, page in enumerate(tqdm(pages, desc="Processing pages")):
    # ... processing code
```

### 4. Backup Important Results
```powershell
# Create backups of successful OCR results:
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "output_directory" "backup_$timestamp" -Recurse
```

These examples should help you adapt the PDF OCR Processor to your specific needs. Remember to always test with a small sample first before processing large document collections!