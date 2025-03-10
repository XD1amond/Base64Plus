/**
 * Basic usage example for Base64Plus JavaScript library.
 */

const fs = require('fs');
const path = require('path');
const { 
  encodeBase64Plus, 
  decodeBase64Plus, 
  renderWithBoundingBoxes 
} = require('../index');

async function main() {
  // Get the current directory
  const currentDir = __dirname;
  
  // Check if sample image exists, otherwise provide instructions
  const sampleImagePath = path.join(currentDir, 'sample_image.jpg');
  if (!fs.existsSync(sampleImagePath)) {
    console.log(`Please place a sample image at ${sampleImagePath}`);
    console.log('You can use any image with text in it.');
    return;
  }
  
  console.log(`Processing image: ${sampleImagePath}`);
  
  try {
    // Encode the image to Base64Plus format
    console.log('Encoding image to Base64Plus format...');
    const base64PlusData = await encodeBase64Plus(sampleImagePath, {
      includeConfidence: true
    });
    
    // Save the Base64Plus data to a file
    const outputFile = path.join(currentDir, 'output.b64p');
    fs.writeFileSync(outputFile, base64PlusData);
    console.log(`Base64Plus data saved to: ${outputFile}`);
    
    // Parse and display some information about the encoded data
    const data = JSON.parse(base64PlusData);
    console.log(`Image format: ${data.format || 'unknown'}`);
    console.log(`Number of text elements detected: ${data.text_data.length}`);
    
    // Print the first few text elements
    console.log('\nDetected text elements:');
    const elementsToShow = Math.min(5, data.text_data.length);
    for (let i = 0; i < elementsToShow; i++) {
      const item = data.text_data[i];
      console.log(`${i+1}. Text: ${item.text}`);
      console.log(`   Position: x=${item.x}, y=${item.y}, width=${item.width}, height=${item.height}`);
      if (item.confidence !== undefined) {
        console.log(`   Confidence: ${item.confidence.toFixed(2)}`);
      }
    }
    
    if (data.text_data.length > 5) {
      console.log(`... and ${data.text_data.length - 5} more elements`);
    }
    
    // Decode the Base64Plus data
    console.log('\nDecoding the Base64Plus data...');
    const decoded = await decodeBase64Plus(base64PlusData);
    
    // Save the decoded image
    const decodedImagePath = path.join(currentDir, 'decoded_image.png');
    fs.writeFileSync(decodedImagePath, decoded.imageBuffer);
    console.log(`Decoded image saved to: ${decodedImagePath}`);
    
    // Create a visualization with bounding boxes
    console.log('\nCreating visualization with bounding boxes...');
    const visualizationPath = path.join(currentDir, 'visualization.png');
    await renderWithBoundingBoxes(decoded, visualizationPath);
    console.log(`Visualization saved to: ${visualizationPath}`);
    
    console.log('\nBase64Plus encoding and decoding completed successfully!');
    
  } catch (error) {
    console.error(`Error: ${error.message}`);
    console.log('\nTroubleshooting tips:');
    console.log('1. Make sure you have installed the required dependencies:');
    console.log('   - npm install tesseract.js canvas');
    console.log('   - For better image processing: npm install sharp');
    console.log('2. Check that your image contains readable text');
    console.log('3. If you\'re on Linux, you might need additional dependencies for canvas:');
    console.log('   - Ubuntu/Debian: sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev');
  }
}

// Run the example
main().catch(console.error);