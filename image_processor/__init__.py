"""
Image Processor Module
Provides base classes and utilities for OCR processing of image folders
"""

from .base_image_processor import ImageProcessor, ImageValidationError

__all__ = ['ImageProcessor', 'ImageValidationError']
