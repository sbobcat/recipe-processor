# Combine Ann's Recipe PDFs in Correct Order
# This script combines SCN_xxxx.pdf files in numerical order with comprehensive validation

param(
    [string]$InputFolder = "C:\Code\pers\recipe-processor\test-data",
    [string]$OutputFile = "Anns_Complete_Recipe_Book.pdf",
    [switch]$DryRun
)

# Function to validate input parameters
function Test-InputValidation {
    param(
        [string]$InputFolder,
        [string]$OutputFile
    )
    
    $errors = @()
    
    # Validate input folder exists
    if (-not (Test-Path $InputFolder -PathType Container)) {
        $errors += "Input folder does not exist: $InputFolder"
    }
    
    # Validate input folder is accessible
    try {
        Get-ChildItem $InputFolder -ErrorAction Stop | Out-Null
    } catch {
        $errors += "Cannot access input folder: $InputFolder. Error: $($_.Exception.Message)"
    }
    
    # Validate output file name
    if ([string]::IsNullOrWhiteSpace($OutputFile)) {
        $errors += "Output file name cannot be empty"
    }
    
    # Validate output file extension
    if (-not $OutputFile.EndsWith('.pdf', [System.StringComparison]::OrdinalIgnoreCase)) {
        $errors += "Output file must have .pdf extension: $OutputFile"
    }
    
    # Check for invalid characters in output filename
    $invalidChars = [System.IO.Path]::GetInvalidFileNameChars()
    $fileName = [System.IO.Path]::GetFileName($OutputFile)
    foreach ($char in $invalidChars) {
        if ($fileName.Contains($char)) {
            $errors += "Output filename contains invalid character '$char': $OutputFile"
            break
        }
    }
    
    return $errors
}

# Function to check PSWritePDF module availability
function Test-PSWritePDFModule {
    try {
        $module = Get-Module -ListAvailable -Name PSWritePDF
        if (-not $module) {
            Write-Host "X PSWritePDF module is not installed" -ForegroundColor Red
            Write-Host "  To install, run: Install-Module PSWritePDF -Scope CurrentUser" -ForegroundColor Yellow
            Write-Host "  Or with admin privileges: Install-Module PSWritePDF" -ForegroundColor Yellow
            return $false
        }
        
        # Try to import the module
        Import-Module PSWritePDF -ErrorAction Stop
        
        # Verify the Merge-PDF command is available
        if (-not (Get-Command Merge-PDF -ErrorAction SilentlyContinue)) {
            Write-Host "X PSWritePDF module is installed but Merge-PDF command is not available" -ForegroundColor Red
            return $false
        }
        
        Write-Host "✓ PSWritePDF module is available" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "X Error loading PSWritePDF module: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Try reinstalling: Uninstall-Module PSWritePDF; Install-Module PSWritePDF" -ForegroundColor Yellow
        return $false
    }
}

# Function to test PDF file integrity
function Test-PDFIntegrity {
    param([string]$FilePath)
    
    try {
        # Basic file size check
        $fileInfo = Get-Item $FilePath
        if ($fileInfo.Length -eq 0) {
            return "File is empty (0 bytes)"
        }
        
        # Check PDF header
        $bytes = [System.IO.File]::ReadAllBytes($FilePath)
        if ($bytes.Length -lt 4) {
            return "File too small to be a valid PDF"
        }
        
        # Check for PDF signature (%PDF)
        $header = [System.Text.Encoding]::ASCII.GetString($bytes[0..3])
        if ($header -ne '%PDF') {
            return "File does not have valid PDF header signature"
        }
        
        # Check for EOF marker (basic validation)
        $content = [System.Text.Encoding]::ASCII.GetString($bytes)
        if ($content -notmatch '%%EOF') {
            return "File appears to be truncated (missing EOF marker)"
        }
        
        return $null # No errors found
    } catch {
        return "Error reading file: $($_.Exception.Message)"
    }
}

# Function to check available disk space
function Test-DiskSpace {
    param(
        [string]$OutputPath,
        [array]$InputFiles
    )
    
    try {
        # Calculate total size of input files
        $totalInputSize = 0
        foreach ($file in $InputFiles) {
            $totalInputSize += (Get-Item $file.FullName).Length
        }
        
        # Get drive information for output location
        $outputDrive = [System.IO.Path]::GetPathRoot($OutputPath)
        $drive = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DeviceID -eq $outputDrive.TrimEnd('\') }
        
        if (-not $drive) {
            return "Cannot determine disk space for output location: $OutputPath"
        }
        
        $freeSpace = [long]$drive.FreeSpace
        $requiredSpace = [long]($totalInputSize * 1.5) # Add 50% buffer for processing
        
        Write-Host "Disk space check:" -ForegroundColor Cyan
        Write-Host "  Total input size: $([math]::Round($totalInputSize / 1MB, 2)) MB" -ForegroundColor Gray
        Write-Host "  Required space (with buffer): $([math]::Round($requiredSpace / 1MB, 2)) MB" -ForegroundColor Gray
        Write-Host "  Available space: $([math]::Round($freeSpace / 1MB, 2)) MB" -ForegroundColor Gray
        
        if ($freeSpace -lt $requiredSpace) {
            return "Insufficient disk space. Required: $([math]::Round($requiredSpace / 1MB, 2)) MB, Available: $([math]::Round($freeSpace / 1MB, 2)) MB"
        }
        
        Write-Host "✓ Sufficient disk space available" -ForegroundColor Green
        return $null # No errors
    } catch {
        return "Error checking disk space: $($_.Exception.Message)"
    }
}

# Set output folder to same as input folder
$OutputFolder = $InputFolder

if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
}

Write-Host "Combining Recipe PDFs..." -ForegroundColor Green
Write-Host "Input folder: $InputFolder" -ForegroundColor Cyan
Write-Host "Output folder: $OutputFolder" -ForegroundColor Cyan
Write-Host "Output file: $OutputFile" -ForegroundColor Cyan

# Validate input parameters
Write-Host "`nValidating input parameters..." -ForegroundColor Cyan
$validationErrors = Test-InputValidation -InputFolder $InputFolder -OutputFile $OutputFile
if ($validationErrors.Count -gt 0) {
    Write-Host "X Input validation failed:" -ForegroundColor Red
    foreach ($error in $validationErrors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
    exit 1
}
Write-Host "✓ Input parameters are valid" -ForegroundColor Green

# Check PSWritePDF module (even in dry run mode for validation)
Write-Host "`nChecking dependencies..." -ForegroundColor Cyan
if (-not (Test-PSWritePDFModule)) {
    exit 1
}

# Change to the recipe folder
try {
    Set-Location $InputFolder -ErrorAction Stop
} catch {
    Write-Host "X Cannot change to input folder: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Get all SCN_*.pdf files and sort them numerically
Write-Host "`nScanning for PDF files..." -ForegroundColor Cyan
$pdfFiles = Get-ChildItem -Path $InputFolder -Filter "SCN_*.pdf" |
    Sort-Object { [int]($_.BaseName -replace 'SCN_', '') }

if ($pdfFiles.Count -eq 0) {
    Write-Host "X No SCN_*.pdf files found in $InputFolder" -ForegroundColor Red
    Write-Host "  Expected files with pattern: SCN_0000.pdf, SCN_0001.pdf, etc." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found $($pdfFiles.Count) PDF files" -ForegroundColor Green

# Validate PDF file integrity
Write-Host "`nValidating PDF file integrity..." -ForegroundColor Cyan
$corruptedFiles = @()
foreach ($file in $pdfFiles) {
    $integrityError = Test-PDFIntegrity -FilePath $file.FullName
    if ($integrityError) {
        $corruptedFiles += @{
            File = $file.Name
            Error = $integrityError
        }
        Write-Host "  X $($file.Name): $integrityError" -ForegroundColor Red
    } else {
        Write-Host "  ✓ $($file.Name): Valid" -ForegroundColor Gray
    }
}

if ($corruptedFiles.Count -gt 0) {
    Write-Host "`nX Found $($corruptedFiles.Count) corrupted or invalid PDF files:" -ForegroundColor Red
    foreach ($corrupt in $corruptedFiles) {
        Write-Host "  - $($corrupt.File): $($corrupt.Error)" -ForegroundColor Red
    }
    Write-Host "`nPlease fix or replace the corrupted files before proceeding." -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ All PDF files passed integrity validation" -ForegroundColor Green

# Check disk space before processing
if (-not $DryRun) {
    Write-Host "`nChecking disk space..." -ForegroundColor Cyan
    $outputPath = Join-Path $OutputFolder $OutputFile
    $diskSpaceError = Test-DiskSpace -OutputPath $outputPath -InputFiles $pdfFiles
    if ($diskSpaceError) {
        Write-Host "X $diskSpaceError" -ForegroundColor Red
        Write-Host "  Please free up disk space or choose a different output location." -ForegroundColor Yellow
        exit 1
    }
}

# Display file list and order
Write-Host "`nFiles to be combined (in order):" -ForegroundColor Green
for ($i = 0; $i -lt $pdfFiles.Count; $i++) {
    $file = $pdfFiles[$i]
    $size = [math]::Round((Get-Item $file.FullName).Length / 1KB, 1)
    Write-Host "  $($i + 1). $($file.Name) ($size KB)" -ForegroundColor Gray
}

# Show summary of first and last files for verification
Write-Host "`nOrder verification:" -ForegroundColor Yellow
Write-Host "  First file: $($pdfFiles[0].Name)" -ForegroundColor Gray
Write-Host "  Last file: $($pdfFiles[-1].Name)" -ForegroundColor Gray
Write-Host "  Total files: $($pdfFiles.Count)" -ForegroundColor Gray

$confirm = Read-Host "`nDoes this order look correct? (y/n)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Operation cancelled by user" -ForegroundColor Yellow
    exit 0
}

if ($DryRun) {
    Write-Host "`n[DRY RUN] Would combine these PDFs in this order:" -ForegroundColor Yellow
    $outputPath = Join-Path $OutputFolder $OutputFile
    Write-Host "[DRY RUN] Output would be: $outputPath" -ForegroundColor Yellow
    
    # Calculate estimated output size
    $totalSize = ($pdfFiles | ForEach-Object { (Get-Item $_.FullName).Length } | Measure-Object -Sum).Sum
    Write-Host "[DRY RUN] Estimated output size: $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor Yellow
    
    Write-Host "[DRY RUN] All validations passed - ready for actual processing" -ForegroundColor Green
    Write-Host "[DRY RUN] No files were actually modified" -ForegroundColor Green
    exit 0
}

# Final pre-processing validation
Write-Host "`nPerforming final pre-processing checks..." -ForegroundColor Cyan

# Verify output location is writable
$outputPath = Join-Path $OutputFolder $OutputFile
try {
    $testFile = Join-Path $OutputFolder "test_write_permissions.tmp"
    [System.IO.File]::WriteAllText($testFile, "test")
    Remove-Item $testFile -Force
    Write-Host "✓ Output location is writable" -ForegroundColor Green
} catch {
    Write-Host "X Cannot write to output location: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Check if output file already exists
if (Test-Path $outputPath) {
    $overwrite = Read-Host "Output file already exists. Overwrite? (y/n)"
    if ($overwrite -ne 'y' -and $overwrite -ne 'Y') {
        Write-Host "Operation cancelled - output file already exists" -ForegroundColor Yellow
        exit 0
    }
    try {
        Remove-Item $outputPath -Force
        Write-Host "✓ Existing output file removed" -ForegroundColor Green
    } catch {
        Write-Host "X Cannot remove existing output file: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Combine the PDFs
Write-Host "`nCombining PDFs..." -ForegroundColor Green
try {
    $inputPaths = $pdfFiles | ForEach-Object { $_.FullName }
    
    # Show progress
    Write-Host "Processing $($inputPaths.Count) files..." -ForegroundColor Cyan
    
    Merge-PDF -InputFile $inputPaths -OutputFile $outputPath -ErrorAction Stop

    # Verify output file was created successfully
    if (-not (Test-Path $outputPath)) {
        throw "Output file was not created successfully"
    }
    
    $outputInfo = Get-Item $outputPath
    if ($outputInfo.Length -eq 0) {
        throw "Output file is empty (0 bytes)"
    }
    
    Write-Host "✓ Successfully created: $OutputFile" -ForegroundColor Green

    # Show detailed file info
    Write-Host "`nOutput file details:" -ForegroundColor Cyan
    Write-Host "  File size: $([math]::Round($outputInfo.Length / 1MB, 2)) MB" -ForegroundColor Gray
    Write-Host "  Location: $($outputInfo.FullName)" -ForegroundColor Gray
    Write-Host "  Created: $($outputInfo.CreationTime)" -ForegroundColor Gray
    
    # Verify output file integrity
    $outputIntegrityError = Test-PDFIntegrity -FilePath $outputPath
    if ($outputIntegrityError) {
        Write-Host "! Warning: Output file may be corrupted: $outputIntegrityError" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Output file integrity verified" -ForegroundColor Green
    }

} catch {
    Write-Host "X Error combining PDFs: $($_.Exception.Message)" -ForegroundColor Red
    
    # Provide helpful troubleshooting information
    Write-Host "`nTroubleshooting suggestions:" -ForegroundColor Yellow
    Write-Host "  1. Ensure all input PDF files are not open in other applications" -ForegroundColor Gray
    Write-Host "  2. Check that PSWritePDF module is up to date: Update-Module PSWritePDF" -ForegroundColor Gray
    Write-Host "  3. Verify sufficient disk space and write permissions" -ForegroundColor Gray
    Write-Host "  4. Try processing a smaller subset of files to isolate the issue" -ForegroundColor Gray
    
    exit 1
}

Write-Host "`n✓ Recipe book compilation complete!" -ForegroundColor Green
Write-Host "  Combined $($pdfFiles.Count) PDF files into $OutputFile" -ForegroundColor Cyan
