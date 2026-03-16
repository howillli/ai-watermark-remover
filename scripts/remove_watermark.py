#!/usr/bin/env python3
"""
Remove watermarks from AI-generated images using inpainting.
Usage: python remove_watermark.py input.jpg --position bottomright
"""

import sys
import argparse
from pathlib import Path
import cv2
import numpy as np

class WatermarkRemover:
    """Remove watermarks from images using various inpainting techniques."""
    
    def __init__(self, image_path):
        self.image_path = Path(image_path)
        self.image = cv2.imread(str(image_path))
        
        if self.image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        self.height, self.width = self.image.shape[:2]
        
    def get_position_area(self, position, padding=10, size='medium'):
        """Get watermark area based on position."""
        
        # Define watermark sizes
        sizes = {
            'small': (200, 60),
            'medium': (400, 100),
            'large': (600, 150)
        }
        
        w, h = sizes.get(size, sizes['medium'])
        
        positions = {
            'topleft': (padding, padding, w, h),
            'top': (self.width//2 - w//2, padding, w, h),
            'topright': (self.width - w - padding, padding, w, h),
            'left': (padding, self.height//2 - h//2, w, h),
            'center': (self.width//2 - w//2, self.height//2 - h//2, w, h),
            'right': (self.width - w - padding, self.height//2 - h//2, w, h),
            'bottomleft': (padding, self.height - h - padding, w, h),
            'bottom': (self.width//2 - w//2, self.height - h - padding, w, h),
            'bottomright': (self.width - w - padding, self.height - h - padding, w, h)
        }
        
        return positions.get(position.lower())
    
    def create_mask(self, area, padding=0):
        """Create mask for the watermark area."""
        x, y, w, h = area
        
        # Add padding
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(self.width - x, w + 2*padding)
        h = min(self.height - y, h + 2*padding)
        
        # Create mask
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        mask[y:y+h, x:x+w] = 255
        
        return mask
    
    def remove_watermark(self, area, method='inpaint', radius=5, padding=10):
        """Remove watermark using specified method."""
        
        # Create mask
        mask = self.create_mask(area, padding)
        
        # Apply inpainting
        if method == 'inpaint' or method == 'ns':
            result = cv2.inpaint(self.image, mask, radius, cv2.INPAINT_NS)
        elif method == 'telea':
            result = cv2.inpaint(self.image, mask, radius, cv2.INPAINT_TELEA)
        elif method == 'patch':
            # Use larger radius for patch-based method
            result = cv2.inpaint(self.image, mask, radius*2, cv2.INPAINT_TELEA)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return result
    
    def save(self, output_path, image=None, quality=95):
        """Save the processed image."""
        if image is None:
            image = self.image
        
        output_path = Path(output_path)
        
        # Set quality parameters
        if output_path.suffix.lower() in ['.jpg', '.jpeg']:
            params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        elif output_path.suffix.lower() == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, 9 - (quality // 11)]
        else:
            params = []
        
        success = cv2.imwrite(str(output_path), image, params)
        
        if not success:
            raise IOError(f"Failed to save image: {output_path}")
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Remove watermarks from AI-generated images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s image.jpg --position bottomright
  %(prog)s image.jpg --area 1500,50,400,100
  %(prog)s image.jpg --position bottomright --method telea --radius 10
  %(prog)s image.jpg --position center --size large --output clean.jpg

Positions:
  topleft, top, topright, left, center, right, bottomleft, bottom, bottomright

Methods:
  inpaint - Fast, good for text (default)
  telea   - Better for complex backgrounds
  patch   - Best quality, slower

Sizes:
  small  - 200x60px
  medium - 400x100px (default)
  large  - 600x150px
        '''
    )
    
    parser.add_argument('input', help='Input image file')
    parser.add_argument('--position', help='Watermark position')
    parser.add_argument('--area', help='Custom area (x,y,width,height)')
    parser.add_argument('--method', default='inpaint', 
                       choices=['inpaint', 'telea', 'patch'],
                       help='Inpainting method (default: inpaint)')
    parser.add_argument('--radius', type=int, default=5,
                       help='Inpainting radius (default: 5)')
    parser.add_argument('--padding', type=int, default=10,
                       help='Extra padding around watermark (default: 10)')
    parser.add_argument('--size', default='medium',
                       choices=['small', 'medium', 'large'],
                       help='Watermark size for position-based removal')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--quality', type=int, default=95,
                       help='Output quality 1-100 (default: 95)')
    parser.add_argument('--preview', action='store_true',
                       help='Show preview before saving')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.position and not args.area:
        parser.error("Either --position or --area must be specified")
    
    try:
        # Load image
        print(f"Loading image: {args.input}")
        remover = WatermarkRemover(args.input)
        print(f"Image size: {remover.width}x{remover.height}")
        
        # Get watermark area
        if args.area:
            # Parse custom area
            try:
                x, y, w, h = map(int, args.area.split(','))
                area = (x, y, w, h)
                print(f"Custom area: x={x}, y={y}, w={w}, h={h}")
            except:
                print("Error: Invalid area format. Use: x,y,width,height")
                sys.exit(1)
        else:
            # Use position
            area = remover.get_position_area(args.position, args.padding, args.size)
            if area is None:
                print(f"Error: Invalid position: {args.position}")
                sys.exit(1)
            x, y, w, h = area
            print(f"Position '{args.position}': x={x}, y={y}, w={w}, h={h}")
        
        # Remove watermark
        print(f"Removing watermark using {args.method} method...")
        result = remover.remove_watermark(area, args.method, args.radius, args.padding)
        
        # Preview
        if args.preview:
            print("Showing preview... (Press any key to continue, ESC to cancel)")
            
            # Create comparison
            comparison = np.hstack([remover.image, result])
            
            # Resize if too large
            max_width = 1600
            if comparison.shape[1] > max_width:
                scale = max_width / comparison.shape[1]
                new_width = int(comparison.shape[1] * scale)
                new_height = int(comparison.shape[0] * scale)
                comparison = cv2.resize(comparison, (new_width, new_height))
            
            cv2.imshow('Before (Left) | After (Right)', comparison)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            if key == 27:  # ESC
                print("Cancelled by user")
                sys.exit(0)
        
        # Save result
        if args.output:
            output_path = args.output
        else:
            input_path = Path(args.input)
            output_path = input_path.parent / f"{input_path.stem}_clean{input_path.suffix}"
        
        print(f"Saving result to: {output_path}")
        remover.save(output_path, result, args.quality)
        
        # Show file sizes
        input_size = Path(args.input).stat().st_size / 1024
        output_size = Path(output_path).stat().st_size / 1024
        print(f"✓ Watermark removed successfully!")
        print(f"  Input size: {input_size:.1f} KB")
        print(f"  Output size: {output_size:.1f} KB")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
