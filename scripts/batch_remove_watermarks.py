#!/usr/bin/env python3
"""
Batch remove watermarks from multiple images.
Usage: python batch_remove_watermarks.py /path/to/images --position bottomright
"""

import sys
import argparse
from pathlib import Path
import cv2
import numpy as np
from remove_watermark import WatermarkRemover

def batch_process(directory, position=None, area=None, method='inpaint', 
                 radius=5, padding=10, size='medium', formats=None, 
                 output_dir=None, quality=95):
    """Batch process images in directory."""
    
    directory = Path(directory)
    
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    
    # Default formats
    if formats is None:
        formats = ['jpg', 'jpeg', 'png', 'webp']
    else:
        formats = [f.lower().strip() for f in formats.split(',')]
    
    # Get all image files
    image_files = []
    for fmt in formats:
        image_files.extend(directory.glob(f'*.{fmt}'))
        image_files.extend(directory.glob(f'*.{fmt.upper()}'))
    
    if not image_files:
        print(f"No image files found in {directory}")
        return
    
    # Create output directory
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = directory / 'watermark_removed'
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"Processing {len(image_files)} images")
    print(f"Output directory: {output_dir}")
    print()
    
    # Parse custom area if provided
    if area:
        try:
            x, y, w, h = map(int, area.split(','))
            custom_area = (x, y, w, h)
            print(f"Using custom area: x={x}, y={y}, w={w}, h={h}")
        except:
            print("Error: Invalid area format. Use: x,y,width,height")
            sys.exit(1)
    else:
        custom_area = None
        print(f"Using position: {position}, size: {size}")
    
    print()
    
    success_count = 0
    fail_count = 0
    
    for i, image_file in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] Processing: {image_file.name}")
        
        try:
            # Load image
            remover = WatermarkRemover(image_file)
            
            # Get watermark area
            if custom_area:
                process_area = custom_area
            else:
                process_area = remover.get_position_area(position, padding, size)
                if process_area is None:
                    print(f"  ✗ Invalid position: {position}")
                    fail_count += 1
                    continue
            
            # Remove watermark
            result = remover.remove_watermark(process_area, method, radius, padding)
            
            # Save result
            output_file = output_dir / image_file.name
            remover.save(output_file, result, quality)
            
            # Show file sizes
            input_size = image_file.stat().st_size / 1024
            output_size = output_file.stat().st_size / 1024
            
            print(f"  ✓ Saved: {output_file.name} ({input_size:.1f}KB -> {output_size:.1f}KB)")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            fail_count += 1
        
        print()
    
    print("=" * 60)
    print(f"Batch processing complete!")
    print(f"Success: {success_count}, Failed: {fail_count}")
    print(f"Output directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='Batch remove watermarks from images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s /path/to/images --position bottomright
  %(prog)s /path/to/images --area 1500,50,400,100
  %(prog)s /path/to/images --position bottomright --method telea
  %(prog)s /path/to/images --position bottomright --output-dir ./cleaned
        '''
    )
    
    parser.add_argument('directory', help='Directory containing images')
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
    parser.add_argument('--formats', default='jpg,png,webp',
                       help='File formats to process (default: jpg,png,webp)')
    parser.add_argument('--output-dir', help='Output directory')
    parser.add_argument('--quality', type=int, default=95,
                       help='Output quality 1-100 (default: 95)')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.position and not args.area:
        parser.error("Either --position or --area must be specified")
    
    try:
        batch_process(
            args.directory,
            position=args.position,
            area=args.area,
            method=args.method,
            radius=args.radius,
            padding=args.padding,
            size=args.size,
            formats=args.formats,
            output_dir=args.output_dir,
            quality=args.quality
        )
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
