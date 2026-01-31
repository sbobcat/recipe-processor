# Project Reorganization Plan (v2.0.0)

## Overview

This document outlines the comprehensive reorganization of the PDF OCR Processor project to improve maintainability, readability, and professional structure. This represents a major version change (v2.0.0) with breaking changes to import paths and file locations.

## Goals

1. **Centralize Documentation** - Move all documentation to `docs/` directory
2. **Organize Tests** - Consolidate all tests in `tests/` with clear structure
3. **Modularize Code** - Separate concerns into logical modules (processors, generators, utils)
4. **Configuration Management** - Replace hardcoded paths with YAML configuration files
5. **Entry Points** - Provide clear CLI scripts for common workflows
6. **Professional Structure** - Follow Python packaging best practices

## Current Issues

### Documentation
- 8+ documentation files scattered across project
- Duplicate information in multiple README files
- Hard to find specific information
- No clear API reference

### Code Organization
- Tests mixed with production code in module folders
- Similar functionality split across multiple directories
- No clear separation between processors and generators
- Example scripts mixed with core code

### Configuration
- Hardcoded paths in every script
- Users must edit multiple files to configure system
- No centralized configuration management

### Entry Points
- No clear starting point for users
- Must know which specific script to run
- No command-line interface

## Proposed Structure

```
pdf-ocr-processor/
├── docs/                                    # Centralized documentation
│   ├── README.md                           # Main comprehensive guide
│   ├── SETUP_GUIDE.md                      # Quick setup instructions
│   ├── USER_GUIDE.md                       # Detailed usage examples
│   ├── TROUBLESHOOTING.md                  # Common issues and solutions
│   ├── CHANGELOG.md                        # Version history
│   ├── API_REFERENCE.md                    # Complete API documentation
│   ├── ARCHITECTURE.md                     # System design overview
│   └── MIGRATION_GUIDE.md                  # v1.x to v2.0 migration
│
├── src/                                     # Core application code
│   ├── __init__.py
│   ├── pdf_combiner/                       # PDF combination module
│   │   ├── __init__.py
│   │   └── combine_pdfs.ps1
│   │
│   ├── processors/                         # OCR processors
│   │   ├── __init__.py
│   │   ├── base_processor.py              # Abstract base class
│   │   ├── image_processor.py             # Image-specific base
│   │   ├── tesseract_processor.py         # Tesseract OCR
│   │   ├── kraken_processor.py            # Kraken OCR
│   │   └── aws_textract_processor.py      # AWS Textract OCR
│   │
│   ├── generators/                         # Review document generators
│   │   ├── __init__.py
│   │   ├── base_generator.py              # Abstract base class
│   │   ├── tesseract_generator.py         # Tesseract review docs
│   │   ├── kraken_generator.py            # Kraken review docs
│   │   └── aws_generator.py               # AWS review docs
│   │
│   └── utils/                              # Shared utilities
│       ├── __init__.py
│       ├── config.py                       # Configuration management
│       ├── validation.py                   # Input validation
│       ├── image_utils.py                  # Image processing helpers
│       └── logging_utils.py                # Logging configuration
│
├── tests/                                   # All tests
│   ├── __init__.py
│   ├── conftest.py                         # Pytest configuration
│   ├── README.md                           # Testing guide
│   ├── unit/                               # Unit tests
│   │   ├── test_base_processor.py
│   │   ├── test_image_processor.py
│   │   ├── test_tesseract_processor.py
│   │   ├── test_aws_processor.py
│   │   ├── test_generators.py
│   │   ├── test_rotation_detection.py
│   │   └── test_validation.py
│   │
│   ├── integration/                        # Integration tests
│   │   ├── test_pdf_workflow.py
│   │   ├── test_image_workflow.py
│   │   └── test_end_to_end.py
│   │
│   └── fixtures/                           # Test data and fixtures
│       ├── sample_images/
│       └── sample_pdfs/
│
├── examples/                                # Example scripts
│   ├── README.md                           # Examples guide
│   ├── basic_pdf_processing.py
│   ├── basic_image_processing.py
│   ├── aws_textract_example.py
│   ├── tesseract_example.py
│   ├── kraken_example.py
│   └── batch_processing.py
│
├── scripts/                                 # Utility scripts
│   ├── process_pdfs.py                    # Main PDF workflow entry point
│   ├── process_images.py                  # Main image workflow entry point
│   ├── setup_environment.py               # Environment setup
│   ├── validate_installation.py           # Dependency checker
│   ├── resize_images.py                   # Image utilities
│   └── cleanup_outputs.py                 # Clean test outputs
│
├── config/                                  # Configuration files
│   ├── default_config.yaml                # Default settings
│   ├── aws_config.yaml                    # AWS-specific config
│   └── tesseract_config.yaml              # Tesseract-specific config
│
├── test-data/                              # Test data
│   ├── sample_pdfs/                       # Sample PDF files
│   ├── sample_images/                     # Sample image files
│   └── expected_outputs/                  # Expected test results
│
├── .kiro/                                  # Kiro IDE configuration
│   └── specs/pdf-ocr-processor/
│       ├── requirements.md
│       ├── tasks.md
│       ├── reorganization-plan.md         # This document
│       └── architecture.md
│
├── .gitignore
├── requirements.txt                        # Production dependencies
├── requirements-dev.txt                    # Development dependencies
├── setup.py                                # Package installation
├── pyproject.toml                          # Modern Python packaging
├── VERSION                                 # Version number (2.0.0)
└── README.md                               # Quick start (links to docs/)
```

## File Migration Map

### Documentation Files

| Current Location | New Location | Action |
|-----------------|--------------|--------|
| `readme.md` | `docs/README.md` | Move |
| `SETUP_GUIDE.md` | `docs/SETUP_GUIDE.md` | Move |
| `EXAMPLES.md` | `docs/USER_GUIDE.md` | Move & Rename |
| `TROUBLESHOOTING.md` | `docs/TROUBLESHOOTING.md` | Move |
| `CHANGELOG.md` | `docs/CHANGELOG.md` | Move |
| `image_processor/README.md` | `docs/API_REFERENCE.md` | Merge |
| `image_processor/README_REVIEW_GENERATORS.md` | `docs/API_REFERENCE.md` | Merge |
| `image_processor/ROTATION_DETECTION.md` | `docs/API_REFERENCE.md` | Merge |
| `image_processor/TESSERACT_FEATURES.md` | `docs/API_REFERENCE.md` | Merge |
| `aws_processor/README_IMAGE_PROCESSOR.md` | `docs/API_REFERENCE.md` | Merge |
| N/A | `docs/ARCHITECTURE.md` | Create New |
| N/A | `docs/MIGRATION_GUIDE.md` | Create New |
| N/A | Root `README.md` | Create New (quick start) |

### Source Code Files

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `image_processor/base_image_processor.py` | `src/processors/image_processor.py` | Rename |
| `image_processor/tesseract_image_processor.py` | `src/processors/tesseract_processor.py` | Rename |
| `local_processor/process_recipes_kraken_python_only.py` | `src/processors/kraken_processor.py` | Rename |
| `aws_processor/kraken_alternative_aws.py` | `src/processors/aws_textract_processor.py` | Merge with aws_textract_image_processor.py |
| `aws_processor/aws_textract_image_processor.py` | `src/processors/aws_textract_processor.py` | Merge |
| `image_processor/tesseract_sidebyside_generator.py` | `src/generators/tesseract_generator.py` | Rename |
| `local_processor/kraken_sidebyside_generator.py` | `src/generators/kraken_generator.py` | Rename |
| `aws_processor/aws_textract_sidebyside_generator.py` | `src/generators/aws_generator.py` | Merge with image_processor version |
| `image_processor/aws_textract_image_sidebyside_generator.py` | `src/generators/aws_generator.py` | Merge |
| `image_combinor/combine_recipe_pdfs.ps1` | `src/pdf_combiner/combine_pdfs.ps1` | Move & Rename |

### Test Files

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `image_processor/test_base_processor.py` | `tests/unit/test_image_processor.py` | Move |
| `image_processor/test_tesseract_preprocessing.py` | `tests/unit/test_tesseract_processor.py` | Move |
| `image_processor/test_rotation_detection.py` | `tests/unit/test_rotation_detection.py` | Move |
| `image_processor/test_review_generators.py` | `tests/unit/test_generators.py` | Move |
| `aws_processor/test_aws_image_processor.py` | `tests/unit/test_aws_processor.py` | Move |
| `image_processor/test_comprehensive.py` | `tests/integration/test_comprehensive.py` | Move |
| `image_processor/test_image_integration.py` | `tests/integration/test_image_workflow.py` | Move & Rename |

### Example Files

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `image_processor/example_usage.py` | `examples/basic_image_processing.py` | Move & Rename |
| `image_processor/example_tesseract_usage.py` | `examples/tesseract_example.py` | Move & Rename |
| `image_processor/example_tesseract_review_usage.py` | `examples/tesseract_review_example.py` | Move & Rename |
| `image_processor/example_aws_review_usage.py` | `examples/aws_review_example.py` | Move & Rename |
| `aws_processor/example_aws_image_usage.py` | `examples/aws_textract_example.py` | Move & Rename |

### Utility Files

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `tools/resize_images.py` | `scripts/resize_images.py` | Move |
| `config_template.py` | `config/default_config.yaml` | Convert to YAML |

## Breaking Changes

### Import Paths

**Before (v1.x):**
```python
from image_processor.base_image_processor import ImageProcessor
from image_processor.tesseract_image_processor import TesseractImageProcessor
from aws_processor.aws_textract_image_processor import AWSTextractImageProcessor
```

**After (v2.0):**
```python
from src.processors.image_processor import ImageProcessor
from src.processors.tesseract_processor import TesseractProcessor
from src.processors.aws_textract_processor import AWSTextractProcessor
```

### Configuration

**Before (v1.x):**
```python
# Hardcoded in script
pdf_path = Path(r"C:\path\to\file.pdf")
output_dir = Path(r"C:\output")
```

**After (v2.0):**
```python
from src.utils.config import Config

config = Config()
pdf_path = config.get('pdf.input_file')
output_dir = config.get('pdf.output_folder')
```

### Entry Points

**Before (v1.x):**
```bash
# Edit script, then run
python aws_processor/kraken_alternative_aws.py
```

**After (v2.0):**
```bash
# Use CLI with config
python scripts/process_pdfs.py input.pdf -o output/ -m aws
```

## Implementation Phases

### Phase 1: Preparation (Tasks 20.0 - 20.1)
- Create new directory structure
- Move source code to src/ module
- No breaking changes yet (old structure still works)

### Phase 2: Tests & Documentation (Tasks 20.2 - 20.4)
- Reorganize tests into tests/ directory
- Consolidate documentation into docs/
- Reorganize examples into examples/
- Still no breaking changes

### Phase 3: Configuration (Tasks 20.5 - 20.6)
- Implement configuration management
- Remove hardcoded paths
- First breaking changes introduced

### Phase 4: Entry Points (Tasks 20.7 - 20.8)
- Create CLI scripts
- Create utility scripts
- Improve user experience

### Phase 5: Packaging (Tasks 20.9 - 20.11)
- Implement Python package structure
- Update all imports
- Reorganize test data

### Phase 6: Validation (Tasks 20.12 - 20.15)
- Test everything
- Create migration guide
- Update documentation
- Release v2.0.0

## Benefits

### For Users
- ✅ Clear entry points - know exactly what to run
- ✅ Configuration files - no more editing code
- ✅ Centralized documentation - find information easily
- ✅ Better examples - learn by example

### For Developers
- ✅ Clear module boundaries - easier to understand
- ✅ Organized tests - faster development
- ✅ Consistent structure - easier to extend
- ✅ Better maintainability - reduce technical debt

### For the Project
- ✅ Professional structure - looks mature
- ✅ Easier onboarding - new contributors can start quickly
- ✅ Better testing - comprehensive test coverage
- ✅ Scalability - easy to add new features

## Risk Mitigation

### Backward Compatibility
- Create migration guide with clear examples
- Document all breaking changes
- Provide import path mapping
- Version as 2.0.0 to signal major changes

### Testing
- Run full test suite after each phase
- Test package installation
- Verify all imports work
- Test all examples

### Documentation
- Update all documentation links
- Create architecture documentation
- Document new structure
- Provide migration examples

## Success Criteria

- [ ] All tests pass in new structure
- [ ] Package installs with pip
- [ ] All examples run successfully
- [ ] Documentation is complete and accurate
- [ ] No broken imports or references
- [ ] Configuration system works correctly
- [ ] CLI scripts provide good user experience
- [ ] Migration guide is clear and helpful

## Timeline Estimate

- **Phase 1-2**: 2-3 days (structure, move files, update imports)
- **Phase 3-4**: 2-3 days (configuration, CLI scripts)
- **Phase 5-6**: 2-3 days (packaging, testing, documentation)
- **Total**: 6-9 days for complete reorganization

## Related Requirements

This reorganization addresses **Requirement 10: Project Organization and Maintainability** with all 10 acceptance criteria.

## Related Tasks

Tasks 20.0 through 20.15 implement this reorganization plan.
