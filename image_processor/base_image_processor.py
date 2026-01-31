#!/usr/bin/env python3
"""
Base Image Processor for OCR Processing
Provides common functionality for processing image folders with OCR
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import logging

try:
    from PIL import Image
except ImportError:
    print("Missing Pillow. Install with: pip install Pillow")
    raise

try:
    import pytesseract
except ImportError:
    pytesseract = None  # Optional dependency for rotation detection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class ImageValidationError(Exception):
    """Raised when image validation fails."""
    pass


class ImageProcessor(ABC):
    """
    Abstract base class for image folder OCR processors.
    Provides common functionality for image discovery, validation, and batch processing.
    """
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    # Minimum resolution for OCR (width x height in pixels)
    MIN_RESOLUTION = (300, 300)  # Minimum 300x300 pixels
    
    # Recommended DPI for OCR
    RECOMMENDED_DPI = 300
    
    # Rotation angles
    ROTATION_ANGLES = {
        0: 0,      # Correct orientation
        90: 270,   # Rotated 90° clockwise -> rotate 270° to correct
        180: 180,  # Upside down -> rotate 180° to correct
        270: 90    # Rotated 270° clockwise -> rotate 90° to correct
    }
    
    def __init__(self, image_folder: str, output_dir: str, auto_rotate: bool = True):
        """
        Initialize image processor.
        
        Args:
            image_folder: Path to folder containing images
            output_dir: Path to output directory for results
            auto_rotate: Enable automatic rotation detection and correction (default: True)
        """
        self.image_folder = Path(image_folder)
        self.output_dir = Path(output_dir)
        self.auto_rotate = auto_rotate
        
        # Create rotated images directory if auto-rotation is enabled
        if self.auto_rotate:
            self.rotated_dir = self.output_dir / 'rotated_images'
            self.rotated_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.rotated_dir = None
        
        # Validate inputs
        if not self.image_folder.exists():
            raise FileNotFoundError(
                f"Image folder not found: {self.image_folder}"
            )
        
        if not self.image_folder.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {self.image_folder}"
            )
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Progress tracking
        self.total_images = 0
        self.processed_images = 0
        self.failed_images = 0
    
    def discover_images(self) -> List[Path]:
        """
        Discover and sort image files in the folder using natural sorting.
        
        Natural sorting ensures: IMG_1.jpg, IMG_2.jpg, IMG_10.jpg, IMG_20.jpg
        instead of: IMG_1.jpg, IMG_10.jpg, IMG_2.jpg, IMG_20.jpg
        
        Returns:
            List of image file paths sorted naturally by filename
        """
        logger.info(f"Discovering images in: {self.image_folder}")
        
        # Find all image files
        image_files = []
        for file_path in self.image_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                image_files.append(file_path)
        
        # Natural sort by filename
        sorted_images = self._natural_sort(image_files)
        
        logger.info(f"Found {len(sorted_images)} image files")
        return sorted_images
    
    def _natural_sort(self, file_paths: List[Path]) -> List[Path]:
        """
        Sort file paths using natural sorting algorithm.
        
        Natural sorting treats numbers as integers rather than strings,
        so IMG_2.jpg comes before IMG_10.jpg.
        
        Args:
            file_paths: List of file paths to sort
            
        Returns:
            Naturally sorted list of file paths
        """
        def natural_key(path: Path) -> List:
            """Generate natural sort key for a file path."""
            # Extract filename without extension
            filename = path.stem
            
            # Split into text and number parts
            parts = re.split(r'(\d+)', filename)
            
            # Convert number strings to integers for proper sorting
            return [int(part) if part.isdigit() else part.lower() for part in parts]
        
        return sorted(file_paths, key=natural_key)
    
    def validate_image_format(self, image_path: Path) -> bool:
        """
        Validate that image file format is supported.
        
        Args:
            image_path: Path to image file
            
        Returns:
            True if format is supported, False otherwise
        """
        suffix = image_path.suffix.lower()
        
        if suffix not in self.SUPPORTED_FORMATS:
            logger.warning(
                f"Unsupported format '{suffix}' for file: {image_path.name}"
            )
            return False
        
        return True
    
    def validate_image_quality(self, image_path: Path) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate image resolution and quality for OCR processing.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (is_valid, metadata_dict)
            metadata_dict contains: width, height, dpi, format, mode
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                dpi = img.info.get('dpi', (72, 72))
                
                # Handle DPI as tuple or single value
                if isinstance(dpi, tuple):
                    dpi_x, dpi_y = dpi
                else:
                    dpi_x = dpi_y = dpi
                
                metadata = {
                    'width': width,
                    'height': height,
                    'dpi': (dpi_x, dpi_y),
                    'format': img.format,
                    'mode': img.mode
                }
                
                # Check minimum resolution
                if width < self.MIN_RESOLUTION[0] or height < self.MIN_RESOLUTION[1]:
                    logger.warning(
                        f"Image resolution too low: {width}x{height} "
                        f"(minimum: {self.MIN_RESOLUTION[0]}x{self.MIN_RESOLUTION[1]}) "
                        f"for file: {image_path.name}"
                    )
                    return False, metadata
                
                # Check DPI (warning only, not a hard failure)
                if dpi_x < self.RECOMMENDED_DPI or dpi_y < self.RECOMMENDED_DPI:
                    logger.warning(
                        f"Image DPI below recommended: {dpi_x}x{dpi_y} "
                        f"(recommended: {self.RECOMMENDED_DPI}) "
                        f"for file: {image_path.name}"
                    )
                
                return True, metadata
                
        except Exception as e:
            logger.error(f"Error validating image {image_path.name}: {e}")
            return False, {'error': str(e)}
    
    def validate_all_images(self, image_paths: List[Path]) -> Tuple[List[Path], List[Dict[str, Any]]]:
        """
        Validate all discovered images for format and quality.
        
        Args:
            image_paths: List of image paths to validate
            
        Returns:
            Tuple of (valid_images, validation_errors)
            validation_errors is a list of dicts with 'path' and 'reason' keys
        """
        logger.info("Validating images...")
        
        valid_images = []
        validation_errors = []
        
        for image_path in image_paths:
            # Check format
            if not self.validate_image_format(image_path):
                validation_errors.append({
                    'path': str(image_path),
                    'reason': f"Unsupported format: {image_path.suffix}"
                })
                continue
            
            # Check quality
            is_valid, metadata = self.validate_image_quality(image_path)
            if not is_valid:
                error_msg = metadata.get('error', 'Resolution too low')
                validation_errors.append({
                    'path': str(image_path),
                    'reason': error_msg
                })
                continue
            
            valid_images.append(image_path)
        
        logger.info(
            f"Validation complete: {len(valid_images)} valid, "
            f"{len(validation_errors)} invalid"
        )
        
        return valid_images, validation_errors
    
    def detect_text_orientation(self, image_path: Path) -> Tuple[int, float]:
        """
        Detect text orientation in an image using Tesseract OSD.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (detected_angle, confidence)
            detected_angle: 0, 90, 180, or 270 degrees
            confidence: Detection confidence (0-100)
        """
        if pytesseract is None:
            logger.warning(
                "Tesseract not available for rotation detection. "
                "Install with: pip install pytesseract"
            )
            return 0, 0.0
        
        try:
            with Image.open(image_path) as img:
                # Use Tesseract OSD (Orientation and Script Detection)
                osd_data = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
                
                # Extract orientation information
                detected_angle = osd_data.get('orientation', 0)
                confidence = osd_data.get('orientation_conf', 0.0)
                
                logger.debug(
                    f"Detected orientation for {image_path.name}: "
                    f"{detected_angle}° (confidence: {confidence:.1f}%)"
                )
                
                return detected_angle, confidence
                
        except pytesseract.TesseractError as e:
            # OSD failed - likely no text detected or image quality too low
            logger.warning(
                f"Could not detect orientation for {image_path.name}: {e}"
            )
            return 0, 0.0
        except Exception as e:
            logger.error(
                f"Error detecting orientation for {image_path.name}: {e}"
            )
            return 0, 0.0
    
    def rotate_image(
        self,
        image_path: Path,
        angle: int,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Rotate an image by the specified angle.
        
        Args:
            image_path: Path to original image file
            angle: Rotation angle (0, 90, 180, 270 degrees)
            output_path: Path to save rotated image (optional)
            
        Returns:
            Path to rotated image file, or None if rotation failed
        """
        if angle == 0:
            # No rotation needed
            return image_path
        
        try:
            with Image.open(image_path) as img:
                # Rotate image (PIL rotates counter-clockwise)
                rotated_img = img.rotate(-angle, expand=True)
                
                # Determine output path
                if output_path is None:
                    if self.rotated_dir:
                        output_path = self.rotated_dir / f"rotated_{image_path.name}"
                    else:
                        output_path = image_path.parent / f"rotated_{image_path.name}"
                
                # Save rotated image
                rotated_img.save(output_path)
                
                logger.info(
                    f"Rotated {image_path.name} by {angle}° -> {output_path.name}"
                )
                
                return output_path
                
        except Exception as e:
            logger.error(f"Failed to rotate image {image_path.name}: {e}")
            return None
    
    def detect_and_correct_rotation(
        self,
        image_path: Path,
        min_confidence: float = 1.5
    ) -> Tuple[Path, Dict[str, Any]]:
        """
        Detect text orientation and automatically correct rotation if needed.
        
        Args:
            image_path: Path to image file
            min_confidence: Minimum confidence threshold for rotation (default: 1.5)
            
        Returns:
            Tuple of (corrected_image_path, rotation_metadata)
            corrected_image_path: Path to corrected image (original if no rotation needed)
            rotation_metadata: Dict with rotation information
        """
        metadata = {
            'original_path': str(image_path),
            'detected_angle': 0,
            'confidence': 0.0,
            'correction_applied': False,
            'corrected_path': str(image_path)
        }
        
        # Skip if auto-rotation is disabled
        if not self.auto_rotate:
            return image_path, metadata
        
        # Detect orientation
        detected_angle, confidence = self.detect_text_orientation(image_path)
        
        metadata['detected_angle'] = detected_angle
        metadata['confidence'] = confidence
        
        # Check if rotation is needed
        if detected_angle == 0:
            # Image is correctly oriented
            logger.debug(f"Image {image_path.name} is correctly oriented")
            return image_path, metadata
        
        # Check confidence threshold
        if confidence < min_confidence:
            logger.warning(
                f"Low confidence ({confidence:.1f}%) for rotation detection "
                f"on {image_path.name}. Skipping rotation."
            )
            return image_path, metadata
        
        # Calculate correction angle
        correction_angle = self.ROTATION_ANGLES.get(detected_angle, 0)
        
        if correction_angle == 0:
            return image_path, metadata
        
        # Rotate image
        corrected_path = self.rotate_image(image_path, correction_angle)
        
        if corrected_path:
            metadata['correction_applied'] = True
            metadata['correction_angle'] = correction_angle
            metadata['corrected_path'] = str(corrected_path)
            
            logger.info(
                f"Corrected orientation for {image_path.name}: "
                f"detected {detected_angle}°, applied {correction_angle}° rotation"
            )
            
            return corrected_path, metadata
        else:
            # Rotation failed, use original
            logger.warning(
                f"Failed to rotate {image_path.name}, using original"
            )
            return image_path, metadata
    
    def update_progress(self, page_num: int, total: int, status: str = "processing"):
        """
        Update and display progress for batch processing.
        
        Args:
            page_num: Current page/image number
            total: Total number of images
            status: Status message (e.g., "processing", "complete", "failed")
        """
        self.processed_images = page_num
        self.total_images = total
        
        percentage = (page_num / total * 100) if total > 0 else 0
        
        logger.info(
            f"Progress: {page_num}/{total} ({percentage:.1f}%) - {status}"
        )
    
    @abstractmethod
    def process_single_image(self, image_path: Path, output_dir: Path, image_num: int) -> Dict[str, Any]:
        """
        Process a single image with OCR.
        
        Must be implemented by subclasses for specific OCR engines.
        
        Args:
            image_path: Path to image file
            output_dir: Directory for output files
            image_num: Image number in sequence
            
        Returns:
            Dictionary with processing results:
            {
                'image_number': int,
                'image_file': str,
                'text_file': str,
                'text': str,
                'success': bool,
                'confidence': float (optional),
                'error': str (if success=False)
            }
        """
        pass
    
    @abstractmethod
    def process_image_folder(self) -> Dict[str, Any]:
        """
        Process all images in the folder.
        
        Must be implemented by subclasses for specific OCR engines.
        
        Returns:
            Dictionary with overall processing results:
            {
                'folder_name': str,
                'total_images': int,
                'successful_images': int,
                'failed_images': int,
                'images': List[Dict] (individual image results)
            }
        """
        pass
    
    def create_processing_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create summary of processing results.
        
        Args:
            results: List of individual image processing results
            
        Returns:
            Summary dictionary with statistics
        """
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        summary = {
            'folder_name': str(self.image_folder),
            'total_images': len(results),
            'successful_images': len(successful),
            'failed_images': len(failed),
            'success_rate': (len(successful) / len(results) * 100) if results else 0,
            'images': results
        }
        
        return summary
