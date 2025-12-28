# Changelog

All notable changes to the PDF OCR Processor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Configuration management system with JSON/YAML support
- Comprehensive error handling and logging framework
- Performance optimizations for large documents
- Property-based testing suite
- Integration tests for complete workflows

## [1.0.0] - 2024-12-28

### Added
- **PDF Combination System**
  - PowerShell script to combine individual SCN_*.pdf files
  - Numerical sorting with user confirmation
  - Dry-run mode for validation
  - PSWritePDF module integration

- **AWS Textract OCR Processing**
  - Cloud-based handwriting recognition
  - Confidence scoring and low-confidence word flagging
  - 216 DPI image extraction for optimal recognition
  - Individual page text files and processing summary

- **Local Kraken OCR Processing**
  - WSL-based local handwriting recognition
  - blla.mlmodel segmentation and McCATMuS_nfd_nofix_V1.mlmodel recognition
  - 300 DPI image extraction
  - Python-only PDF processing with PyMuPDF

- **Review Document Generation**
  - Side-by-side Word document creation
  - Original images (left) and OCR text (right) layout
  - Support for both Kraken and AWS Textract results
  - Editable text formatting with processing metadata

- **Comprehensive Documentation**
  - Complete README with setup and usage instructions
  - Quick setup guide for 5-minute installation
  - Troubleshooting guide for common issues
  - Real-world usage examples and workflows
  - Configuration template for easy customization

### Technical Details
- **Dependencies**: PyMuPDF, Pillow, python-docx, boto3, PSWritePDF
- **Platforms**: Windows 10/11 with optional WSL for local processing
- **AWS Integration**: Textract detect_document_text API
- **Kraken Integration**: Command-line interface with specific model configuration

### File Structure
```
├── aws_processor/
│   ├── kraken_alternative_aws.py
│   └── aws_textract_sidebyside_generator.py
├── image_combinor/
│   └── combine_recipe_pdfs.ps1
├── local_processor/
│   ├── process_recipes_kraken_python_only.py
│   └── kraken_sidebyside_generator.py
├── test-data/
├── .kiro/specs/pdf-ocr-processor/
├── Documentation files (README.md, SETUP_GUIDE.md, etc.)
└── Configuration templates
```

## [0.2.0] - 2024-12-27 (Pre-release)

### Added
- Initial AWS Textract integration
- Basic review document generation for Kraken results
- Validation and testing framework

### Changed
- Improved error handling in OCR processors
- Enhanced progress reporting

## [0.1.0] - 2024-12-27 (Initial Development)

### Added
- Basic PDF combination functionality
- Initial Kraken OCR integration
- Proof of concept for handwritten text recognition

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes or major architectural changes
- **MINOR** version (0.X.0): New functionality in a backwards compatible manner
- **PATCH** version (0.0.X): Backwards compatible bug fixes

### Version Guidelines

**Major Version Changes (2.0.0, 3.0.0, etc.):**
- Breaking changes to file formats or command-line interfaces
- Major architectural redesigns
- Removal of deprecated features
- Changes requiring user migration steps

**Minor Version Changes (1.1.0, 1.2.0, etc.):**
- New OCR processing methods or engines
- Additional output formats
- New configuration options
- Enhanced review document features
- Performance improvements

**Patch Version Changes (1.0.1, 1.0.2, etc.):**
- Bug fixes in existing functionality
- Documentation updates
- Dependency updates
- Security patches
- Minor performance optimizations

## Release Process

### Creating a New Release

1. **Update Version Numbers**
   - Update version in `VERSION` file
   - Update version references in documentation
   - Update any version strings in code

2. **Update Changelog**
   - Move items from `[Unreleased]` to new version section
   - Add release date
   - Ensure all changes are documented

3. **Create Git Tag**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. **Test Release**
   - Verify all components work with clean installation
   - Test both AWS and Kraken workflows
   - Validate documentation accuracy

### Hotfix Process

For critical bug fixes:

1. Create hotfix branch from main
2. Apply minimal fix
3. Update patch version (e.g., 1.0.0 → 1.0.1)
4. Update changelog
5. Create release tag
6. Merge back to main

## Migration Guides

### Upgrading from 0.x to 1.0.0

**Breaking Changes:**
- File path configuration moved to centralized config system
- PowerShell script parameters standardized
- Output directory structure reorganized

**Migration Steps:**
1. Back up existing configuration and output files
2. Update file paths using new config_template.py
3. Test with small sample before processing large collections
4. Update any custom scripts to use new interfaces

**Compatibility:**
- Existing OCR output files remain compatible
- Review documents from previous versions can still be opened
- PDF combination results are fully compatible

---

## Support and Compatibility

### Supported Versions

| Version | Status | Support Level | End of Life |
|---------|--------|---------------|-------------|
| 1.0.x   | Active | Full support  | TBD         |
| 0.2.x   | Legacy | Security only | 2025-06-01  |
| 0.1.x   | Legacy | None          | 2024-12-31  |

### Compatibility Matrix

| Component | Windows 10 | Windows 11 | WSL 1 | WSL 2 | Python 3.8+ |
|-----------|------------|------------|-------|-------|-------------|
| PDF Combiner | ✅ | ✅ | N/A | N/A | N/A |
| AWS OCR | ✅ | ✅ | N/A | N/A | ✅ |
| Kraken OCR | ✅ | ✅ | ✅ | ✅ | ✅ |
| Review Generator | ✅ | ✅ | N/A | N/A | ✅ |