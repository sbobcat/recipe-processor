#!/usr/bin/env python3
"""
Image resizer script to resize images in the assets folder to 400px width
while maintaining aspect ratio.
"""

import os
from PIL import Image
import sys

def resize_image(input_path, output_path, target_width=400):
    """
    Resize an image to target width while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the resized image
        target_width (int): Target width in pixels (default: 400)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Get original dimensions
            original_width, original_height = img.size
            
            # Calculate new height to maintain aspect ratio
            aspect_ratio = original_height / original_width
            target_height = int(target_width * aspect_ratio)
            
            # Resize the image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Save the resized image
            resized_img.save(output_path, optimize=True, quality=95)
            
            print(f"✓ Resized {os.path.basename(input_path)}: {original_width}x{original_height} → {target_width}x{target_height}")
            
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False
    
    return True

def main():
    """Main function to process all images in the assets folder."""
    assets_folder = "assets"
    target_width = 400
    
    # Check if assets folder exists
    if not os.path.exists(assets_folder):
        print(f"Error: {assets_folder} folder not found!")
        sys.exit(1)
    
    # Get list of image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
    image_files = []
    
    for filename in os.listdir(assets_folder):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            image_files.append(filename)
    
    if not image_files:
        print(f"No image files found in {assets_folder} folder!")
        sys.exit(1)
    
    print(f"Found {len(image_files)} image(s) to resize:")
    for img in image_files:
        print(f"  - {img}")
    
    print(f"\nResizing images to {target_width}px width...")
    
    success_count = 0
    for filename in image_files:
        input_path = os.path.join(assets_folder, filename)
        output_path = input_path  # Overwrite original files
        
        if resize_image(input_path, output_path, target_width):
            success_count += 1
    
    print(f"\nCompleted! Successfully resized {success_count}/{len(image_files)} images.")

if __name__ == "__main__":
    main()