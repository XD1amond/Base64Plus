"""
Core implementation of Base64Plus encoding and decoding functionality.
"""

import base64
import json
import os
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    from pytesseract import Output
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Base64PlusError(Exception):
    """Base exception for Base64Plus errors."""
    pass


class DependencyError(Base64PlusError):
    """Raised when a required dependency is not available."""
    pass


def _check_dependencies():
    """Check if required dependencies are installed."""
    if not PIL_AVAILABLE:
        raise DependencyError(
            "Pillow is required. Install it with 'pip install Pillow'."
        )
    
    if not (EASYOCR_AVAILABLE or TESSERACT_AVAILABLE):
        raise DependencyError(
            "Either EasyOCR or Tesseract is required. "
            "Install EasyOCR with 'pip install easyocr' or "
            "Tesseract with 'pip install pytesseract' (and the Tesseract executable)."
        )


def _extract_text_easyocr(image: Image.Image) -> List[Dict]:
    """Extract text and positions using EasyOCR."""
    if not EASYOCR_AVAILABLE:
        raise DependencyError("EasyOCR is not installed.")
    
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])  # Initialize for English
    
    # Detect text
    results = reader.readtext(img_array)
    
    text_data = []
    for result in results:
        # EasyOCR returns: (bbox, text, prob)
        bbox, text, confidence = result
        
        # Calculate bounding box coordinates
        top_left, top_right, bottom_right, bottom_left = bbox
        x = int(top_left[0])
        y = int(top_left[1])
        width = int(bottom_right[0] - top_left[0])
        height = int(bottom_right[1] - top_left[1])
        
        text_data.append({
            "text": text,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "confidence": float(confidence)
        })
    
    return text_data


def _extract_text_tesseract(image: Image.Image) -> List[Dict]:
    """Extract text and positions using Tesseract OCR."""
    if not TESSERACT_AVAILABLE:
        raise DependencyError("Tesseract is not installed.")
    
    # Get text and bounding box data
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    
    text_data = []
    n_boxes = len(data['text'])
    
    for i in range(n_boxes):
        # Skip empty text
        if int(data['conf'][i]) < 0 or not data['text'][i].strip():
            continue
        
        text_data.append({
            "text": data['text'][i],
            "x": data['left'][i],
            "y": data['top'][i],
            "width": data['width'][i],
            "height": data['height'][i],
            "confidence": float(data['conf'][i]) / 100.0  # Normalize to 0-1
        })
    
    return text_data


def encode_base64plus(
    image_path: str, 
    ocr_engine: str = 'auto',
    include_confidence: bool = True,
    image_format: str = None
) -> str:
    """
    Encode an image into Base64Plus format with text and position metadata.
    
    Args:
        image_path: Path to the image file
        ocr_engine: OCR engine to use ('easyocr', 'tesseract', or 'auto')
        include_confidence: Whether to include confidence scores in the output
        image_format: Output image format (default: same as input)
    
    Returns:
        A JSON string containing the Base64-encoded image and text metadata
    """
    _check_dependencies()
    
    # Open the image
    image = Image.open(image_path)
    
    # Determine image format if not specified
    if image_format is None:
        image_format = os.path.splitext(image_path)[1].lstrip('.').upper()
        if image_format.lower() not in ('jpeg', 'jpg', 'png'):
            image_format = 'PNG'  # Default to PNG
        # Normalize JPG to JPEG for PIL
        if image_format.upper() == 'JPG':
            image_format = 'JPEG'
    
    # Extract text based on the specified OCR engine
    if ocr_engine == 'easyocr' or (ocr_engine == 'auto' and EASYOCR_AVAILABLE):
        text_data = _extract_text_easyocr(image)
    elif ocr_engine == 'tesseract' or (ocr_engine == 'auto' and TESSERACT_AVAILABLE):
        text_data = _extract_text_tesseract(image)
    else:
        raise ValueError(f"Unsupported OCR engine: {ocr_engine}")
    
    # Remove confidence if not requested
    if not include_confidence:
        for item in text_data:
            if 'confidence' in item:
                del item['confidence']
    
    # Encode the image to base64
    buffered = BytesIO()
    image.save(buffered, format=image_format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Create the Base64Plus data structure
    base64plus_data = {
        "image": img_str,
        "text_data": text_data,
        "format": image_format.lower()
    }
    
    # Return as JSON string
    return json.dumps(base64plus_data)


def decode_base64plus(base64plus_string: str) -> Tuple[Image.Image, List[Dict]]:
    """
    Decode a Base64Plus string back into an image and text metadata.
    
    Args:
        base64plus_string: The Base64Plus JSON string
    
    Returns:
        A tuple containing (PIL Image, text data list)
    """
    _check_dependencies()
    
    # Parse the JSON data
    try:
        data = json.loads(base64plus_string)
    except json.JSONDecodeError:
        raise ValueError("Invalid Base64Plus string: not valid JSON")
    
    # Check required fields
    if 'image' not in data or 'text_data' not in data:
        raise ValueError("Invalid Base64Plus string: missing required fields")
    
    # Decode the base64 image
    image_format = data.get('format', 'png')
    image_data = base64.b64decode(data['image'])
    image = Image.open(BytesIO(image_data))
    
    return image, data['text_data']


# Add numpy import at the top if EasyOCR is available
if EASYOCR_AVAILABLE:
    import numpy as np