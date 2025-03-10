"""
Unit tests for the Base64Plus Python package.
"""

import os
import json
import unittest
from io import BytesIO
from PIL import Image

# Try to import the package
try:
    from base64plus import encode_base64plus, decode_base64plus
    PACKAGE_INSTALLED = True
except ImportError:
    # If package is not installed, try to import from local path
    import sys
    import os.path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from base64plus import encode_base64plus, decode_base64plus
        PACKAGE_INSTALLED = True
    except ImportError:
        PACKAGE_INSTALLED = False


class TestBase64Plus(unittest.TestCase):
    """Test cases for Base64Plus functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Create a simple test image
        cls.test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
        
        # Create a simple image with text
        img = Image.new('RGB', (300, 100), color=(255, 255, 255))
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Try to use a font that's likely to be available
        try:
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
                '/Library/Fonts/Arial.ttf',  # macOS
                'C:\\Windows\\Fonts\\arial.ttf',  # Windows
                '/System/Library/Fonts/Helvetica.ttc'  # macOS alternative
            ]
            
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 24)
                    break
            
            if font is None:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Draw text
        draw.text((10, 10), "Base64Plus Test", fill=(0, 0, 0), font=font)
        draw.text((10, 50), "Testing 123", fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(cls.test_image_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        # Remove the test image
        if os.path.exists(cls.test_image_path):
            os.remove(cls.test_image_path)
    
    def test_package_installed(self):
        """Test that the package is installed."""
        self.assertTrue(PACKAGE_INSTALLED, "Base64Plus package is not installed")
    
    def test_encode_decode_roundtrip(self):
        """Test encoding and decoding an image."""
        if not PACKAGE_INSTALLED:
            self.skipTest("Base64Plus package is not installed")
        
        # Skip if OCR engines are not available
        try:
            # Encode the test image
            base64plus_data = encode_base64plus(self.test_image_path)
            
            # Check that the result is valid JSON
            data = json.loads(base64plus_data)
            
            # Check that the required fields are present
            self.assertIn('image', data, "Encoded data missing 'image' field")
            self.assertIn('text_data', data, "Encoded data missing 'text_data' field")
            self.assertIn('format', data, "Encoded data missing 'format' field")
            
            # Decode the data
            image, text_data = decode_base64plus(base64plus_data)
            
            # Check that the image is a PIL Image
            self.assertIsInstance(image, Image.Image, "Decoded image is not a PIL Image")
            
            # Check that text_data is a list
            self.assertIsInstance(text_data, list, "Decoded text_data is not a list")
            
            # If OCR worked, there should be some text data
            # But we can't guarantee this, so we don't assert on the content
            
        except Exception as e:
            if "No OCR engine available" in str(e):
                self.skipTest("No OCR engine available")
            else:
                raise
    
    def test_encode_with_options(self):
        """Test encoding with various options."""
        if not PACKAGE_INSTALLED:
            self.skipTest("Base64Plus package is not installed")
        
        # Skip if OCR engines are not available
        try:
            # Test with different options
            options_to_test = [
                {'include_confidence': True, 'image_format': 'PNG'},
                {'include_confidence': False, 'image_format': 'JPEG'},
            ]
            
            for options in options_to_test:
                # Encode with options
                base64plus_data = encode_base64plus(
                    self.test_image_path,
                    include_confidence=options['include_confidence'],
                    image_format=options['image_format']
                )
                
                # Check that the result is valid JSON
                data = json.loads(base64plus_data)
                
                # Check format
                self.assertEqual(
                    data['format'].lower(), 
                    options['image_format'].lower(),
                    f"Incorrect format: expected {options['image_format'].lower()}, got {data['format'].lower()}"
                )
                
                # Check confidence
                if not options['include_confidence'] and len(data['text_data']) > 0:
                    # If confidence should be excluded and we have text data,
                    # check that no item has a confidence field
                    for item in data['text_data']:
                        self.assertNotIn(
                            'confidence', item,
                            "Confidence field present when include_confidence=False"
                        )
        
        except Exception as e:
            if "No OCR engine available" in str(e):
                self.skipTest("No OCR engine available")
            else:
                raise


if __name__ == '__main__':
    unittest.main()