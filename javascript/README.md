# Base64Plus (JavaScript)

Transform images into AI-ready data with embedded text and positions.

Base64Plus is a JavaScript library that processes images by extracting text and positional metadata, then encodes both the image and extracted metadata into an AI-ready Base64+ format.

## Installation

```bash
# Using npm
npm install base64plus

# Using yarn
yarn add base64plus
```

### Dependencies

Base64Plus requires the following dependencies:

- **Required**: 
  - `tesseract.js`: For OCR text extraction
  - `canvas`: For image processing and visualization

- **Optional**:
  - `sharp`: For better image processing (recommended)

These dependencies will be installed automatically when you install Base64Plus.

## Usage

### Basic Usage

```javascript
const { encodeBase64Plus, decodeBase64Plus } = require('base64plus');
const fs = require('fs');

// Encode an image to Base64Plus format
async function encodeExample() {
  try {
    const base64PlusData = await encodeBase64Plus('path/to/your/image.jpg');
    
    // Save the Base64Plus data to a file
    fs.writeFileSync('output.b64p', base64PlusData);
    console.log('Base64Plus data saved to output.b64p');
  } catch (error) {
    console.error('Encoding error:', error);
  }
}

// Decode Base64Plus data
async function decodeExample() {
  try {
    const base64PlusString = fs.readFileSync('output.b64p', 'utf8');
    const { imageBuffer, textData } = await decodeBase64Plus(base64PlusString);
    
    // Save the decoded image
    fs.writeFileSync('decoded_image.png', imageBuffer);
    console.log('Decoded image saved to decoded_image.png');
    
    // Print the extracted text data
    textData.forEach((item, index) => {
      console.log(`Text ${index + 1}: ${item.text}`);
      console.log(`Position: x=${item.x}, y=${item.y}, width=${item.width}, height=${item.height}`);
      if (item.confidence !== undefined) {
        console.log(`Confidence: ${item.confidence.toFixed(2)}`);
      }
      console.log('---');
    });
  } catch (error) {
    console.error('Decoding error:', error);
  }
}

// Run the examples
encodeExample().then(() => decodeExample());
```

### Advanced Usage

```javascript
const { 
  encodeBase64Plus, 
  decodeBase64Plus, 
  renderWithBoundingBoxes 
} = require('base64plus');
const fs = require('fs');

async function advancedExample() {
  try {
    // Encode with options
    const base64PlusData = await encodeBase64Plus('path/to/your/image.jpg', {
      includeConfidence: true,
      imageFormat: 'png'  // Force output format
    });
    
    // Parse the JSON directly if needed
    const data = JSON.parse(base64PlusData);
    console.log(`Number of text elements: ${data.text_data.length}`);
    
    // Decode the data
    const decoded = await decodeBase64Plus(base64PlusData);
    
    // Render the image with bounding boxes around text
    await renderWithBoundingBoxes(decoded, 'visualization.png');
    console.log('Visualization with bounding boxes saved to visualization.png');
    
    // You can also work with image buffers directly
    const imageBuffer = fs.readFileSync('path/to/your/image.jpg');
    const bufferEncoded = await encodeBase64Plus(imageBuffer, {
      imageFormat: 'jpeg'
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

advancedExample();
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

## API Reference

### encodeBase64Plus(imagePath, options)

Encodes an image into Base64Plus format with text and position metadata.

- **Parameters**:
  - `imagePath`: String (file path) or Buffer (image data)
  - `options`: Object (optional)
    - `includeConfidence`: Boolean (default: true) - Whether to include confidence scores
    - `imageFormat`: String (default: auto-detected) - Output image format ('jpeg' or 'png')
  
- **Returns**: Promise resolving to a JSON string

### decodeBase64Plus(base64PlusString)

Decodes a Base64Plus string back into an image and text metadata.

- **Parameters**:
  - `base64PlusString`: String - The Base64Plus JSON string
  
- **Returns**: Promise resolving to an object with:
  - `imageBuffer`: Buffer - The decoded image data
  - `textData`: Array - The text metadata
  - `format`: String - The image format

### saveDecodedImage(decodedData, outputPath)

Saves the decoded image to a file.

- **Parameters**:
  - `decodedData`: Object - Data returned from decodeBase64Plus
  - `outputPath`: String - Path to save the image
  
- **Returns**: Promise resolving when the file is saved

### renderWithBoundingBoxes(decodedData, outputPath)

Renders the decoded image with bounding boxes around text.

- **Parameters**:
  - `decodedData`: Object - Data returned from decodeBase64Plus
  - `outputPath`: String - Path to save the rendered image
  
- **Returns**: Promise resolving when the file is saved

## License

MIT