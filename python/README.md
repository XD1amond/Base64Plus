# Base64Plus (Python)

Transform images into AI-ready data with embedded text and positions.

Base64Plus is a Python library that processes images by extracting text and positional metadata, then encodes both the image and extracted metadata into an AI-ready Base64+ format.

## Installation

```bash
# Basic installation
pip install base64plus

# With EasyOCR support (recommended)
pip install base64plus[easyocr]

# With Tesseract support
pip install base64plus[tesseract]

# With all OCR engines
pip install base64plus[all]
```

If using Tesseract, you'll also need to install the Tesseract executable:
- On Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- On macOS: `brew install tesseract`
- On Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Basic Usage

```python
from base64plus import encode_base64plus, decode_base64plus

# Encode an image to Base64Plus format
base64plus_data = encode_base64plus('path/to/your/image.jpg')

# Save the Base64Plus data to a file
with open('output.b64p', 'w') as f:
    f.write(base64plus_data)

# Later, decode the Base64Plus data
with open('output.b64p', 'r') as f:
    base64plus_string = f.read()
    
image, text_data = decode_base64plus(base64plus_string)

# Display the image
image.show()

# Print the extracted text data
for item in text_data:
    print(f"Text: {item['text']}")
    print(f"Position: x={item['x']}, y={item['y']}, width={item['width']}, height={item['height']}")
    if 'confidence' in item:
        print(f"Confidence: {item['confidence']}")
    print("---")
```

### Advanced Usage

```python
# Specify OCR engine
base64plus_data = encode_base64plus(
    'path/to/your/image.jpg',
    ocr_engine='easyocr',  # or 'tesseract' or 'auto'
    include_confidence=True,
    image_format='PNG'  # Force output format
)

# Parse the JSON directly if needed
import json
data = json.loads(base64plus_data)
print(f"Number of text elements: {len(data['text_data'])}")
```

## Output Format

The Base64Plus format is a JSON structure containing:

```json
{
  "image": "<base64_encoded_image>",
  "text_data": [
    {"text": "Hello", "x": 100, "y": 50, "width": 80, "height": 20, "confidence": 0.95},
    {"text": "World", "x": 200, "y": 50, "width": 90, "height": 20, "confidence": 0.98}
  ],
  "format": "png"
}
```

## License

MIT