#!/usr/bin/env python3
"""
Interactive watermark removal with visual selection.
Usage: python remove_watermark_interactive.py input.jpg
"""

import sys
import argparse
from pathlib import Path
import cv2
import numpy as np
from remove_watermark import WatermarkRemover

class InteractiveSelector:
    """Interactive watermark area selector."""
    
    def __init__(self, image_path):
        self.image_path = Path(image_path)
        self.image = cv2.imread(str(image_path))
        
        if self.image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        self.display_image = self.image.copy()
        self.original_image = self.image.copy()
        
        # Selection state
        self.selecting = False
        self.start_point = None
        self.end_point = None
        self.selected_area = None
        
        # Window name
        self.window_name = 'Select Watermark Area'
        
        # Scale for display
        self.scale = 1.0
        max_display_width = 1400
        if self.image.shape[1] > max_display_width:
            self.scale = max_display_width / self.image.shape[1]
            new_width = int(self.image.shape[1] * self.scale)
            new_height = int(self.image.shape[0] * self.scale)
            self.display_image = cv2.resize(self.image, (new_width, new_height))
            self.original_image = self.display_image.copy()
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events."""
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.start_point = (x, y)
            self.end_point = (x, y)
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.selecting:
                self.end_point = (x, y)
                self.draw_selection()
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.selecting = False
            self.end_point = (x, y)
            self.draw_selection()
            
            # Calculate selected area
            if self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                
                # Ensure x1 < x2 and y1 < y2
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                
                # Convert to original image coordinates
                x1 = int(x1 / self.scale)
                y1 = int(y1 / self.scale)
                x2 = int(x2 / self.scale)
                y2 = int(y2 / self.scale)
                
                width = x2 - x1
                height = y2 - y1
                
                self.selected_area = (x1, y1, width, height)
    
    def draw_selection(self):
        """Draw selection rectangle."""
        self.display_image = self.original_image.copy()
        
        if self.start_point and self.end_point:
            cv2.rectangle(
                self.display_image,
                self.start_point,
                self.end_point,
                (0, 255, 0),
                2
            )
            
            # Show dimensions
            x1, y1 = self.start_point
            x2, y2 = self.end_point
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            # Convert to original coordinates
            orig_width = int(width / self.scale)
            orig_height = int(height / self.scale)
            
            text = f"{orig_width}x{orig_height}"
            cv2.putText(
                self.display_image,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        cv2.imshow(self.window_name, self.display_image)
    
    def select(self):
        """Run interactive selection."""
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        # Instructions
        instructions = [
            "Instructions:",
            "1. Click and drag to select watermark area",
            "2. Press ENTER to confirm selection",
            "3. Press R to reset selection",
            "4. Press ESC to cancel"
        ]
        
        print("\n".join(instructions))
        print()
        
        cv2.imshow(self.window_name, self.display_image)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            if key == 13:  # ENTER
                if self.selected_area:
                    cv2.destroyAllWindows()
                    return self.selected_area
                else:
                    print("No area selected. Please select an area first.")
            
            elif key == 27:  # ESC
                cv2.destroyAllWindows()
                return None
            
            elif key == ord('r') or key == ord('R'):
                # Reset selection
                self.start_point = None
                self.end_point = None
                self.selected_area = None
                self.display_image = self.original_image.copy()
                cv2.imshow(self.window_name, self.display_image)
                print("Selection reset")

def main():
    parser = argparse.ArgumentParser(
        description='Interactive watermark removal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Instructions:
  1. Click and drag to select watermark area
  2. Press ENTER to confirm selection
  3. Press R to reset selection
  4. Press ESC to cancel

Example:
  %(prog)s image.jpg
  %(prog)s image.jpg --method telea --output clean.jpg
        '''
    )
    
    parser.add_argument('input', help='Input image file')
    parser.add_argument('--method', default='inpaint',
                       choices=['inpaint', 'telea', 'patch'],
                       help='Inpainting method (default: inpaint)')
    parser.add_argument('--radius', type=int, default=5,
                       help='Inpainting radius (default: 5)')
    parser.add_argument('--padding', type=int, default=10,
                       help='Extra padding around watermark (default: 10)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--quality', type=int, default=95,
                       help='Output quality 1-100 (default: 95)')
    
    args = parser.parse_args()
    
    try:
        # Interactive selection
        print(f"Loading image: {args.input}")
        selector = InteractiveSelector(args.input)
        
        area = selector.select()
        
        if area is None:
            print("Cancelled by user")
            sys.exit(0)
        
        x, y, w, h = area
        print(f"\nSelected area: x={x}, y={y}, width={w}, height={h}")
        print(f"Command for batch processing:")
        print(f"  python batch_remove_watermarks.py <directory> --area {x},{y},{w},{h}")
        print()
        
        # Remove watermark
        print(f"Removing watermark using {args.method} method...")
        remover = WatermarkRemover(args.input)
        result = remover.remove_watermark(area, args.method, args.radius, args.padding)
        
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
