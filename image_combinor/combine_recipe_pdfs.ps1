# Combine Ann's Recipe PDFs in Correct Order
# This script combines SCN_xxxx.pdf files in numerical order

param(
    [string]$InputFolder = "C:\Users\steph\OneDrive\Documents\Scanned Documents\annsrecipes",
    [string]$OutputFile = "Anns_Complete_Recipe_Book.pdf",
    [switch]$DryRun
)

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

# Change to the recipe folder
Set-Location $InputFolder

if (-not $DryRun) {
    # Import the PSWritePDF module (must be pre-installed)
    Import-Module PSWritePDF
}

# Get all SCN_*.pdf files and sort them numerically
$pdfFiles = Get-ChildItem -Path $InputFolder -Filter "SCN_*.pdf" |
    Sort-Object { [int]($_.BaseName -replace 'SCN_', '') }

if ($pdfFiles.Count -eq 0) {
    Write-Host "X No SCN_*.pdf files found in $InputFolder" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($pdfFiles.Count) PDF files:" -ForegroundColor Green
foreach ($file in $pdfFiles) {
    Write-Host "  $($file.Name)" -ForegroundColor Gray
}

# Verify the order looks correct
Write-Host "`nFirst few files in order:" -ForegroundColor Yellow
$pdfFiles | Select-Object -First 5 | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }
Write-Host "Last few files in order:" -ForegroundColor Yellow
$pdfFiles | Select-Object -Last 5 | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }

$confirm = Read-Host "`nDoes this order look correct? (y/n)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Operation cancelled" -ForegroundColor Yellow
    exit 0
}

if ($DryRun) {
    Write-Host "`n[DRY RUN] Would combine these PDFs in this order:" -ForegroundColor Yellow
    $outputPath = Join-Path $OutputFolder $OutputFile
    Write-Host "[DRY RUN] Output would be: $outputPath" -ForegroundColor Yellow
    Write-Host "[DRY RUN] No files were actually modified" -ForegroundColor Green
    exit 0
}

# Combine the PDFs
Write-Host "`nCombining PDFs..." -ForegroundColor Green
try {
    $inputPaths = $pdfFiles | ForEach-Object { $_.FullName }
    $outputPath = Join-Path $OutputFolder $OutputFile
    Merge-PDF -InputFile $inputPaths -OutputFile $outputPath

    Write-Host "OK Successfully created: $OutputFile" -ForegroundColor Green

    # Show file info
    $outputInfo = Get-Item $outputPath
    Write-Host "File size: $([math]::Round($outputInfo.Length / 1MB, 2)) MB" -ForegroundColor Cyan
    Write-Host "Location: $($outputInfo.FullName)" -ForegroundColor Cyan

} catch {
    Write-Host "X Error combining PDFs: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n Recipe book compilation complete!" -ForegroundColor Green
