/**
 * Base64Plus - Transform images into AI-ready data with embedded text and positions.
 * 
 * This library processes images by extracting text and positional metadata,
 * then encodes both the image and extracted metadata into an AI-ready Base64+ format.
 */

const fs = require('fs');
const path = require('path');
const { createCanvas, loadImage } = require('canvas');

// Check if Tesseract.js is available
let Tesseract;
try {
  Tesseract = require('tesseract.js');
  TESSERACT_AVAILABLE = true;
} catch (error) {
  TESSERACT_AVAILABLE = false;
}

// Check if Sharp is available (optional for better image processing)
let sharp;
try {
  sharp = require('sharp');
  SHARP_AVAILABLE = true;
} catch (error) {
  SHARP_AVAILABLE = false;
}

/**
 * Base class for Base64Plus errors
 */
class Base64PlusError extends Error {
  constructor(message) {
    super(message);
    this.name = 'Base64PlusError';
  }
}

/**
 * Error thrown when a required dependency is missing
 */
class DependencyError extends Base64PlusError {
  constructor(message) {
    super(message);
    this.name = 'DependencyError';
  }
}

/**
 * Check if required dependencies are installed
 * @private
 */
function _checkDependencies() {
  if (!TESSERACT_AVAILABLE) {
    throw new DependencyError(
      "Tesseract.js is required. Install it with 'npm install tesseract.js'."
    );
  }
}

/**
 * Extract text and positions from an image using Tesseract.js
 * @private
 * @param {Buffer|string} imageData - Image data buffer or path
 * @returns {Promise<Array>} Array of text data objects
 */
async function _extractTextTesseract(imageData) {
  if (!TESSERACT_AVAILABLE) {
    throw new DependencyError("Tesseract.js is not installed.");
  }

  // Create worker
  const worker = await Tesseract.createWorker('eng');
  
  try {
    // Recognize text (with bounding boxes)
    const { data } = await worker.recognize(imageData);
    
    // Process results
    const textData = [];
    
    // Process words with positions
    for (const word of data.words) {
      // Skip words with low confidence
      if (word.confidence < 10) continue;
      
      const { text, bbox } = word;
      
      textData.push({
        text,
        x: Math.round(bbox.x0),
        y: Math.round(bbox.y0),
        width: Math.round(bbox.x1 - bbox.x0),
        height: Math.round(bbox.y1 - bbox.y0),
        confidence: word.confidence / 100 // Normalize to 0-1
      });
    }
    
    return textData;
  } finally {
    // Always terminate the worker
    await worker.terminate();
  }
}

/**
 * Encode an image into Base64Plus format with text and position metadata
 * @param {string|Buffer} imagePath - Path to the image file or image buffer
 * @param {Object} options - Encoding options
 * @param {boolean} [options.includeConfidence=true] - Whether to include confidence scores
 * @param {string} [options.imageFormat=null] - Output image format (default: same as input or 'png')
 * @returns {Promise<string>} A JSON string containing the Base64-encoded image and text metadata
 */
async function encodeBase64Plus(imagePath, options = {}) {
  _checkDependencies();
  
  const {
    includeConfidence = true,
    imageFormat = null
  } = options;
  
  let imageBuffer;
  let format;
  
  // Handle different input types
  if (typeof imagePath === 'string') {
    // It's a file path
    imageBuffer = fs.readFileSync(imagePath);
    
    // Determine format from file extension if not specified
    if (!imageFormat) {
      const ext = path.extname(imagePath).toLowerCase().substring(1);
      format = ['jpg', 'jpeg', 'png'].includes(ext) ? ext : 'png';
      // Normalize jpg to jpeg for consistency
      if (format === 'jpg') format = 'jpeg';
    } else {
      format = imageFormat.toLowerCase();
    }
  } else if (Buffer.isBuffer(imagePath)) {
    // It's already a buffer
    imageBuffer = imagePath;
    format = imageFormat ? imageFormat.toLowerCase() : 'png';
  } else {
    throw new TypeError('Image input must be a file path (string) or Buffer');
  }
  
  // Use sharp for image processing if available
  if (SHARP_AVAILABLE) {
    const sharpImage = sharp(imageBuffer);
    const metadata = await sharpImage.metadata();
    
    // If format wasn't determined from file extension, get it from the image metadata
    if (!format && metadata.format) {
      format = metadata.format.toLowerCase();
    }
    
    // Ensure format is valid
    if (!['jpeg', 'png'].includes(format)) {
      format = 'png';
    }
    
    // Convert to specified format
    if (format === 'jpeg') {
      imageBuffer = await sharpImage.jpeg().toBuffer();
    } else {
      imageBuffer = await sharpImage.png().toBuffer();
    }
  }
  
  // Extract text using Tesseract
  const textData = await _extractTextTesseract(imageBuffer);
  
  // Remove confidence if not requested
  if (!includeConfidence) {
    for (const item of textData) {
      delete item.confidence;
    }
  }
  
  // Encode the image to base64
  const base64Image = imageBuffer.toString('base64');
  
  // Create the Base64Plus data structure
  const base64PlusData = {
    image: base64Image,
    text_data: textData,
    format: format
  };
  
  // Return as JSON string
  return JSON.stringify(base64PlusData);
}

/**
 * Decode a Base64Plus string back into an image and text metadata
 * @param {string} base64PlusString - The Base64Plus JSON string
 * @returns {Promise<Object>} Object containing { imageBuffer, textData, format }
 */
async function decodeBase64Plus(base64PlusString) {
  // Parse the JSON data
  let data;
  try {
    data = JSON.parse(base64PlusString);
  } catch (error) {
    throw new Error("Invalid Base64Plus string: not valid JSON");
  }
  
  // Check required fields
  if (!data.image || !data.text_data) {
    throw new Error("Invalid Base64Plus string: missing required fields");
  }
  
  // Decode the base64 image
  const imageBuffer = Buffer.from(data.image, 'base64');
  const format = data.format || 'png';
  
  return {
    imageBuffer,
    textData: data.text_data,
    format
  };
}

/**
 * Save the decoded image to a file
 * @param {Object} decodedData - Data returned from decodeBase64Plus
 * @param {string} outputPath - Path to save the image
 * @returns {Promise<void>}
 */
async function saveDecodedImage(decodedData, outputPath) {
  fs.writeFileSync(outputPath, decodedData.imageBuffer);
}

/**
 * Render the decoded image with bounding boxes around text
 * @param {Object} decodedData - Data returned from decodeBase64Plus
 * @param {string} outputPath - Path to save the rendered image
 * @returns {Promise<void>}
 */
async function renderWithBoundingBoxes(decodedData, outputPath) {
  const { imageBuffer, textData } = decodedData;
  
  // Load the image
  const image = await loadImage(imageBuffer);
  
  // Create a canvas with the same dimensions
  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext('2d');
  
  // Draw the original image
  ctx.drawImage(image, 0, 0);
  
  // Draw bounding boxes
  ctx.strokeStyle = 'red';
  ctx.lineWidth = 2;
  ctx.fillStyle = 'rgba(255, 0, 0, 0.2)';
  
  for (const item of textData) {
    ctx.strokeRect(item.x, item.y, item.width, item.height);
    ctx.fillRect(item.x, item.y, item.width, item.height);
  }
  
  // Save the image
  const out = fs.createWriteStream(outputPath);
  const stream = canvas.createPNGStream();
  stream.pipe(out);
  
  return new Promise((resolve, reject) => {
    out.on('finish', resolve);
    out.on('error', reject);
  });
}

module.exports = {
  encodeBase64Plus,
  decodeBase64Plus,
  saveDecodedImage,
  renderWithBoundingBoxes,
  Base64PlusError,
  DependencyError
};