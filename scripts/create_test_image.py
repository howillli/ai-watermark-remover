#!/usr/bin/env python3
"""
Create a test image with watermark for demonstration.
"""

import numpy as np
import cv2
from pathlib import Path

def create_test_image():
    """Create a test image with AI watermark."""
    
    # Create a colorful test image (800x600)
    width, height = 800, 600
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create gradient background
    for y in range(height):
        for x in range(width):
            image[y, x] = [
                int(255 * x / width),
                int(255 * y / height),
                int(128 + 127 * np.sin(x / 50))
            ]
    
    # Add some shapes
    cv2.circle(image, (200, 200), 80, (255, 255, 0), -1)
    cv2.rectangle(image, (400, 300), (600, 500), (0, 255, 255), -1)
    
    # Add "AI Generated" watermark in bottom right
    watermark_text = "AI Generated"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    thickness = 2
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(
        watermark_text, font, font_scale, thickness
    )
    
    # Position in bottom right
    x = width - text_width - 20
    y = height - 20
    
    # Add semi-transparent background
    overlay = image.copy()
    cv2.rectangle(
        overlay,
        (x - 10, y - text_height - 10),
        (x + text_width + 10, y + 10),
        (0, 0, 0),
        -1
    )
    image = cv2.addWeighted(overlay, 0.3, image, 0.7, 0)
    
    # Add text
    cv2.putText(
        image,
        watermark_text,
        (x, y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA
    )
    
    return image

def main():
    # Create test image
    image = create_test_image()
    
    # Save to Desktop
    output_path = Path.home() / "Desktop" / "test_ai_watermark.jpg"
    cv2.imwrite(str(output_path), image)
    
    print(f"✓ Test image created: {output_path}")
    print(f"  Image size: 800x600")
    print(f"  Watermark: 'AI Generated' in bottom right corner")
    print()
    print("To remove watermark:")
    print(f"  python3 scripts/remove_watermark.py {output_path} --position bottomright")

if __name__ == '__main__':
    main()
