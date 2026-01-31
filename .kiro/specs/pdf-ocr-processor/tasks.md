# Implementation Plan: PDF OCR Processor

## Overview

This implementation plan converts the PDF OCR processor design into discrete coding tasks. The system has four main components for PDF processing: PDF combination (PowerShell), local OCR processing (Python/Kraken), AWS OCR processing (Python/Textract), and review document generation (Python/Word). Additionally, the system supports direct image folder processing with Tesseract (local) and AWS Textract (cloud) for OCR, with automatic text orientation detection and rotation correction, generating similar side-by-side review documents. Tasks focus on improving existing code, adding comprehensive testing, and ensuring robust error handling.

## Tasks

- [x] A. Validate existing code functionality and setup
  - Test the PowerShell PDF combiner script with sample SCN_*.pdf files
  - Verify PSWritePDF module is installed and working
  - Test the local Kraken OCR processor with a sample combined PDF
  - Verify Kraken installation and model availability in WSL
  - Test the AWS OCR processor with proper AWS credentials
  - Verify boto3 and AWS Textract access is working
  - Test the side-by-side review generator with existing OCR output
  - Verify python-docx and Word document generation works
  - Document any setup issues or missing dependencies
  - _Requirements: Baseline functionality validation_

- [x] 1. Enhance PDF Combiner with robust error handling and validation
  - Improve the PowerShell script with comprehensive input validation
  - Add better error messages for missing dependencies (PSWritePDF module)
  - Implement file corruption detection before processing
  - Add disk space validation before combining PDFs
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.3, 5.5_

- [ ]* 1.1 Write property test for PDF combination ordering
  - **Property 1: PDF Combination Preserves Order and Completeness**
  - **Validates: Requirements 1.1, 1.2, 1.3**

- [ ]* 1.2 Write unit tests for PDF combiner error handling
  - Test missing files, corrupted files, permission issues
  - Test dry-run mode functionality
  - _Requirements: 1.4, 5.2, 5.3_

- [ ] 2. Refactor and enhance Local OCR Processor
  - Improve error handling in KrakenProcessorPythonOnly class
  - Add input validation for PDF files and output directories
  - Enhance progress reporting during processing
  - Add configuration validation for Kraken models
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 5.1, 5.4_

- [ ]* 2.1 Write property test for local OCR completeness
  - **Property 2: OCR Processing Produces Complete Results**
  - **Validates: Requirements 2.1, 2.3**

- [ ]* 2.2 Write property test for Kraken model usage
  - **Property 6: Processing Models and APIs Are Used Correctly**
  - **Validates: Requirements 2.2**

- [ ]* 2.3 Write unit tests for local OCR error handling
  - Test missing dependencies, invalid inputs, processing failures
  - Test partial processing and recovery scenarios
  - _Requirements: 2.4, 5.1, 5.4_

- [ ] 3. Enhance AWS OCR Processor with better error handling
  - Improve error handling in AWSTextractOCR class
  - Add retry logic for AWS service failures
  - Enhance confidence score analysis and flagging
  - Add AWS credentials validation
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 5.1_

- [ ]* 3.1 Write property test for AWS OCR completeness
  - **Property 2: OCR Processing Produces Complete Results**
  - **Validates: Requirements 3.1, 3.3**

- [ ]* 3.2 Write property test for confidence score flagging
  - **Property 4: Confidence Scoring Flags Low-Quality Results**
  - **Validates: Requirements 3.4**

- [ ]* 3.3 Write unit tests for AWS OCR error handling
  - Test AWS service errors, credential issues, API failures
  - Test confidence threshold configuration
  - _Requirements: 3.5, 5.1, 6.3_

- [x] 3.5 Create AWS OCR Review Generator
  - Create AWSTextractSideBySideGenerator class similar to KrakenSideBySideGenerator
  - Support AWS Textract output format with confidence scores
  - Generate Word documents with original images and AWS OCR text
  - Include confidence score highlighting for low-confidence words
  - Handle AWS-specific metadata and processing statistics
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.1, 8.2, 8.3_

- [ ]* 3.6 Write unit tests for AWS review generator
  - Test document creation with AWS OCR results
  - Test confidence score highlighting and formatting
  - Test handling of missing images and failed pages
  - _Requirements: 4.3, 4.4, 8.1, 8.2_

- [x] 4.1 Cleanup and prepare MVP environment
  - Create cleanup script to remove test files and validation output
  - List files to be cleaned up for user confirmation before removal
  - Clean up validation_output directory contents
  - Remove create_mock_results.py and test_*.py files
  - Preserve test-data folder and its contents
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: System cleanup and preparation_

- [x] 4.2 MVP Checkpoint - Create initial documentation
  - Create comprehensive README with setup and usage instructions
  - Create a requirements file, 1 for the use of local (kraken), and 1 for AWS
  - Document configuration options and troubleshooting guide
  - Document both local (Kraken) and AWS (Textract) processing workflows
  - Include examples of running each component
  - Document review document generation process
  - _Requirements: MVP documentation and user guidance_

- [ ] 5. Enhance Review Generator with comprehensive formatting
  - Improve KrakenSideBySideGenerator class error handling
  - Add support for AWS OCR results in addition to Kraken results
  - Enhance document formatting and image quality preservation
  - Add metadata and processing statistics to documents
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.1, 8.2, 8.3_

- [ ]* 5.1 Write property test for review document structure
  - **Property 5: Review Document Generation Maintains Structure**
  - **Validates: Requirements 4.1, 4.2, 4.5**

- [ ]* 5.2 Write unit tests for review generator formatting
  - Test document layout, image insertion, text formatting
  - Test handling of missing images and failed pages
  - _Requirements: 4.3, 4.4, 8.1, 8.2_

- [ ] 6. Implement comprehensive error handling and logging
  - Create centralized logging system across all components
  - Add input validation utilities for file paths and configurations
  - Implement graceful degradation for missing dependencies
  - Add progress tracking and resumption capabilities
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 7.3, 7.4_

- [ ]* 6.1 Write property test for error handling resilience
  - **Property 3: Error Handling Preserves System Stability**
  - **Validates: Requirements 5.1, 5.2, 5.3**

- [ ]* 6.2 Write property test for processing resilience
  - **Property 8: Processing Resilience Preserves Partial Work**
  - **Validates: Requirements 5.4, 7.4**

- [ ] 7. Add configuration management system
  - Create configuration classes for all processing options
  - Add support for configuration files (JSON/YAML)
  - Implement configuration validation and defaults
  - Add support for different output directories and naming schemes
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 7.1 Write property test for configuration validation
  - **Property 7: Configuration Options Control System Behavior**
  - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [ ]* 7.2 Write unit tests for configuration management
  - Test configuration loading, validation, and defaults
  - Test dry-run mode functionality
  - _Requirements: 6.5_

- [ ] 8. Implement performance optimizations
  - Add image resolution validation and optimization
  - Implement sequential processing with memory management
  - Add progress indicators and status reporting
  - Optimize file I/O operations
  - _Requirements: 7.1, 7.2, 7.3_

- [ ]* 8.1 Write property test for image resolution requirements
  - **Property 9: Image Resolution Meets OCR Requirements**
  - **Validates: Requirements 7.1**

- [ ]* 8.2 Write unit tests for performance optimizations
  - Test memory usage during large file processing
  - Test progress reporting functionality
  - _Requirements: 7.2, 7.3_

- [ ] 9. Add summary statistics and reporting
  - Implement comprehensive statistics collection
  - Add accuracy and completeness reporting
  - Create processing reports with detailed metrics
  - Add comparison capabilities between processing methods
  - _Requirements: 8.5, 2.5_

- [ ]* 9.1 Write property test for summary statistics accuracy
  - **Property 10: Summary Statistics Reflect Actual Results**
  - **Validates: Requirements 2.5, 8.5**

- [ ] 10. Create integration and end-to-end tests
  - Create test data sets with known expected results
  - Implement full pipeline testing from PDF input to review document
  - Add cross-platform testing for Windows/WSL integration
  - Test AWS integration with proper mocking
  - _Requirements: All requirements integration_

- [ ]* 10.1 Write integration tests for complete workflows
  - Test PDF combination → OCR processing → review generation pipeline
  - Test both local and AWS processing paths
  - _Requirements: Complete workflow validation_

- [ ] 11. Final checkpoint and documentation
  - Ensure all tests pass and system works end-to-end
  - Create comprehensive README with setup and usage instructions
  - Document configuration options and troubleshooting guide
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 12. Create AWS Textract monitoring infrastructure
  - Create CloudFormation template for CloudWatch dashboard
  - Monitor key Textract metrics (API calls, errors, throttling, processing time)
  - Add service quota monitoring for Textract limits
  - Create CloudTrail insights queries for Textract activity investigation
  - Include cost monitoring and usage analytics
  - Add alerting for quota approaching and error rate thresholds
  - _Requirements: AWS monitoring and operational visibility_

- [ ]* 12.1 Design CloudWatch dashboard for Textract metrics
  - Create dashboard with API call volume, success/error rates
  - Add processing time and throttling metrics
  - Include service quota utilization widgets
  - Add cost analysis and usage trends
  - _Requirements: Real-time monitoring visibility_

- [ ]* 12.2 Implement CloudTrail queries for investigation
  - Create pre-built queries for Textract API activity
  - Add queries for error investigation and troubleshooting
  - Include user activity and access pattern analysis
  - Create queries for cost optimization insights
  - _Requirements: Operational troubleshooting and audit capabilities_

- [ ]* 12.3 Set up automated alerting and notifications
  - Configure CloudWatch alarms for error rate thresholds
  - Add quota utilization alerts (80%, 90% thresholds)
  - Create cost anomaly detection for unexpected usage
  - Set up SNS notifications for critical alerts
  - _Requirements: Proactive monitoring and incident response_

- [x] 13. Create Image Folder Processor Base Class
  - Implement image file discovery with natural sorting (IMG_001.jpg, IMG_002.jpg, etc.)
  - Add image format validation (JPEG, PNG, BMP, TIFF support)
  - Create resolution and quality validation before OCR processing
  - Add text orientation detection and automatic rotation correction
  - Implement base ImageProcessor interface similar to PDF processors
  - Add progress tracking for batch image processing
  - _Requirements: 9.1, 9.2, 9.3, 9.7, 9.9, 7.1_

- [ ]* 13.1 Write property test for image discovery and sorting
  - **Property 11: Image Discovery Maintains Order and Completeness**
  - **Validates: Requirements 9.1**

- [ ]* 13.2 Write unit tests for image validation
  - Test format validation for supported/unsupported formats
  - Test resolution and quality checks
  - Test error handling for corrupted images
  - _Requirements: 9.2, 9.3, 9.8_

- [x] 14. Implement Tesseract Local Image Processor
  - Create TesseractImageProcessor class (parallel to KrakenProcessorPythonOnly)
  - Support configurable language models (eng, fra, deu, etc.)
  - Utilize base class rotation detection before OCR processing
  - Implement batch image processing with memory management
  - Generate text output files per image with confidence scores
  - Add preprocessing options (deskew, denoise, contrast enhancement)
  - Create processing summary with success rates and statistics
  - _Requirements: 9.4, 9.7, 9.8, 9.9, 9.10_

- [ ]* 14.1 Write property test for Tesseract processing completeness
  - **Property 12: Image OCR Processing Produces Complete Results**
  - **Validates: Requirements 9.4, 9.7**

- [ ]* 14.2 Write property test for Tesseract language model usage
  - **Property 13: Tesseract Language Models Are Applied Correctly**
  - **Validates: Requirements 9.4**

- [ ]* 14.3 Write unit tests for Tesseract error handling
  - Test missing dependencies and installation validation
  - Test invalid image inputs and processing failures
  - Test partial processing and recovery scenarios
  - _Requirements: 9.8, 5.1, 5.2_

- [x] 15. Implement AWS Textract Image Processor
  - Create AWSTextractImageProcessor class (extends existing AWSTextractOCR)
  - Process images directly without PDF conversion step
  - Utilize base class rotation detection before OCR processing
  - Reuse confidence scoring and low-confidence word flagging logic
  - Support batch processing with AWS API rate limiting
  - Add retry logic for AWS service failures
  - Generate per-image results with confidence scores
  - _Requirements: 9.5, 9.7, 9.8, 9.10_

- [ ]* 15.1 Write property test for AWS image processing completeness
  - **Property 14: AWS Image OCR Processing Produces Complete Results**
  - **Validates: Requirements 9.5, 9.7**

- [ ]* 15.2 Write unit tests for AWS image processor
  - Test direct image processing without PDF conversion
  - Test AWS API error handling and retry logic
  - Test confidence score analysis for images
  - _Requirements: 9.5, 9.8, 3.5_

- [x] 16. Create Image Review Generators
  - Create TesseractSideBySideGenerator for local processing results
  - Create AWSTextractImageSideBySideGenerator for AWS processing results
  - Generate Word documents with side-by-side image and text layout
  - Maintain image quality and aspect ratios in output documents
  - Highlight low-confidence words in review documents
  - Include processing metadata and statistics in documents
  - _Requirements: 9.6, 9.10, 4.1, 4.2, 4.3, 8.1, 8.2_

- [ ]* 16.1 Write property test for image review document structure
  - **Property 15: Image Review Documents Maintain Structure**
  - **Validates: Requirements 9.6, 4.1, 4.2_

- [ ]* 16.2 Write unit tests for image review generators
  - Test document layout with various image sizes
  - Test confidence score highlighting
  - Test handling of missing or failed images
  - _Requirements: 9.6, 4.3, 8.1, 8.2_

- [x] 17. Add Image Processing Integration Tests
  - Create test image datasets with known expected results
  - Test full pipeline: Image Folder → Tesseract → Review Document
  - Test full pipeline: Image Folder → AWS Textract → Review Document
  - Test mixed format image folders (JPEG + PNG)
  - Test error recovery and partial processing scenarios
  - _Requirements: 9.1-9.10 integration validation_

- [ ]* 17.1 Write end-to-end tests for image workflows
  - Test complete Tesseract workflow with sample images
  - Test complete AWS Textract workflow with sample images
  - Test comparison between Tesseract and AWS results
  - _Requirements: Complete image workflow validation_

- [x] 18. Update documentation for image processing
  - Add image processing section to README
  - Document Tesseract installation and configuration
  - Document supported image formats and requirements
  - Add examples of processing image folders
  - Document differences between PDF and image workflows
  - _Requirements: Image processing user guidance_

- [x] 19. Add automatic image rotation detection and correction
  - Implement text orientation detection in base_image_processor.py
  - Detect if text is vertical (90° or 270°), upside down (180°), or correct (0°)
  - Automatically rotate images before OCR processing
  - Add configuration option to enable/disable auto-rotation
  - Preserve original images and save rotated versions separately
  - Update processing metadata to track rotation corrections
  - _Requirements: 9.2, 9.3, 9.7, 7.1 (image quality optimization)_

- [ ]* 19.1 Write property test for rotation detection accuracy
  - **Property 16: Rotation Detection Identifies Text Orientation Correctly**
  - **Validates: Requirements 9.2, 9.3**

- [ ]* 19.2 Write unit tests for rotation correction
  - Test detection of 0°, 90°, 180°, 270° orientations
  - Test rotation correction for each orientation
  - Test handling of images with no detectable text
  - Test configuration option to disable auto-rotation
  - _Requirements: 9.2, 9.3, 6.1, 6.2_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The existing Kraken command structure should not be modified
- AWS Textract integration should use existing boto3 patterns
- PowerShell components should maintain Windows compatibility