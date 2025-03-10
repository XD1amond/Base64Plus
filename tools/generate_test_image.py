"""
Generate a test image with text for Base64Plus examples.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def generate_test_image(output_path, width=800, height=600, bg_color=(255, 255, 255)):
    """Generate a test image with text."""
    # Create a blank image
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not available
    try:
        # Try to find a font that's likely to be on the system
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            '/Library/Fonts/Arial.ttf',  # macOS
            'C:\\Windows\\Fonts\\arial.ttf',  # Windows
            '/System/Library/Fonts/Helvetica.ttc'  # macOS alternative
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 36)
                break
        
        if font is None:
            # Fall back to default font
            font = ImageFont.load_default()
            print("Warning: Using default font. Text may not be ideal for OCR testing.")
    except Exception as e:
        print(f"Warning: Could not load font: {e}")
        font = ImageFont.load_default()
    
    # Draw some text
    texts = [
        ("Base64Plus Test Image", (100, 100)),
        ("Hello World!", (150, 200)),
        ("OCR Example", (200, 300)),
        ("1234567890", (250, 400)),
        ("Text with positions", (300, 500))
    ]
    
    for text, position in texts:
        # Draw text with a slight shadow for better contrast
        draw.text((position[0]+2, position[1]+2), text, font=font, fill=(200, 200, 200))
        draw.text(position, text, font=font, fill=(0, 0, 0))
    
    # Save the image
    image.save(output_path)
    print(f"Test image generated: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output paths for both Python and JavaScript examples
    output_paths = [
        os.path.join(script_dir, '..', 'python', 'examples', 'sample_image.jpg'),
        os.path.join(script_dir, '..', 'javascript', 'examples', 'sample_image.jpg')
    ]
    
    # Generate images
    for path in output_paths:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        generate_test_image(path)
        
    print("\nTest images have been generated for both Python and JavaScript examples.")
    print("You can now run the example scripts to test the Base64Plus library.")