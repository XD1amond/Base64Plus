# Base64Plus

Transform images into AI-ready data with embedded text and positions.

Base64Plus is a cross-platform library that processes images by extracting text and positional metadata, then encodes both the image and extracted metadata into an AI-ready Base64+ format. This makes it easy to feed images with text into AI models while preserving the text content and its spatial information.

## Available Implementations

Base64Plus is available in multiple programming languages:

- [Python](./python/): A Python library with support for both EasyOCR and Tesseract
- [JavaScript](./javascript/): A Node.js library using Tesseract.js

## What is Base64Plus?

Base64Plus extends the standard Base64 encoding by adding structured metadata about text content found in the image. The format is a JSON structure containing:

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

This format makes it easy to:

1. Transmit images with text content in a single string
2. Preserve text information for AI processing
3. Maintain the spatial relationship between text elements
4. Reconstruct the original image when needed

## Use Cases

- **AI Training Data**: Create datasets that include both images and text positions
- **Document Processing**: Extract and preserve text layout from scanned documents
- **Image Annotation**: Store text annotations directly with images
- **OCR Preprocessing**: Pre-extract text to speed up AI processing pipelines
- **Cross-Platform Applications**: Use the same format across different programming languages

## Getting Started

### Python

```bash
# Install the Python package
pip install base64plus[easyocr]  # With EasyOCR support (recommended)
# or
pip install base64plus[tesseract]  # With Tesseract support
```

```python
from base64plus import encode_base64plus, decode_base64plus

# Encode an image
base64plus_data = encode_base64plus('path/to/image.jpg')

# Decode back to image and text data
image, text_data = decode_base64plus(base64plus_data)
```

See the [Python README](./python/README.md) for more details.

### JavaScript

```bash
# Install the JavaScript package
npm install base64plus
```

```javascript
const { encodeBase64Plus, decodeBase64Plus } = require('base64plus');

// Encode an image
async function example() {
  const base64PlusData = await encodeBase64Plus('path/to/image.jpg');
  
  // Decode back to image buffer and text data
  const { imageBuffer, textData } = await decodeBase64Plus(base64PlusData);
}
```

See the [JavaScript README](./javascript/README.md) for more details.

## License

MIT
