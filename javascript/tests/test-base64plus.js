/**
 * Unit tests for the Base64Plus JavaScript package.
 * 
 * To run these tests:
 * 1. Make sure you have installed the package dependencies
 * 2. Run: node tests/test-base64plus.js
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { createCanvas, loadImage } = require('canvas');

// Import the Base64Plus library
let base64plus;
try {
  base64plus = require('../index');
  console.log('✓ Successfully imported Base64Plus library');
} catch (error) {
  console.error('✗ Failed to import Base64Plus library:', error.message);
  process.exit(1);
}

// Test image path
const TEST_IMAGE_PATH = path.join(__dirname, 'test_image.png');

/**
 * Create a simple test image with text
 */
async function createTestImage() {
  // Create a canvas
  const canvas = createCanvas(300, 100);
  const ctx = canvas.getContext('2d');
  
  // Fill with white background
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, 300, 100);
  
  // Add some text
  ctx.fillStyle = 'black';
  ctx.font = '24px Arial';
  ctx.fillText('Base64Plus Test', 10, 30);
  ctx.fillText('Testing 123', 10, 70);
  
  // Save to file
  const out = fs.createWriteStream(TEST_IMAGE_PATH);
  const stream = canvas.createPNGStream();
  stream.pipe(out);
  
  return new Promise((resolve, reject) => {
    out.on('finish', resolve);
    out.on('error', reject);
  });
}

/**
 * Clean up test files
 */
function cleanup() {
  if (fs.existsSync(TEST_IMAGE_PATH)) {
    fs.unlinkSync(TEST_IMAGE_PATH);
    console.log('✓ Cleaned up test image');
  }
}

/**
 * Run all tests
 */
async function runTests() {
  console.log('Running Base64Plus JavaScript tests...\n');
  
  try {
    // Create test image
    console.log('Creating test image...');
    await createTestImage();
    console.log('✓ Test image created');
    
    // Test 1: Encode and decode roundtrip
    console.log('\nTest 1: Encode and decode roundtrip');
    try {
      // Encode the test image
      const base64PlusData = await base64plus.encodeBase64Plus(TEST_IMAGE_PATH);
      console.log('✓ Successfully encoded image');
      
      // Check that the result is valid JSON
      const data = JSON.parse(base64PlusData);
      console.log('✓ Encoded data is valid JSON');
      
      // Check that the required fields are present
      assert(data.image, "Encoded data missing 'image' field");
      assert(data.text_data, "Encoded data missing 'text_data' field");
      assert(data.format, "Encoded data missing 'format' field");
      console.log('✓ Encoded data has all required fields');
      
      // Decode the data
      const decoded = await base64plus.decodeBase64Plus(base64PlusData);
      console.log('✓ Successfully decoded data');
      
      // Check that the image buffer exists
      assert(Buffer.isBuffer(decoded.imageBuffer), "Decoded image is not a Buffer");
      console.log('✓ Decoded image is a valid Buffer');
      
      // Check that text_data is an array
      assert(Array.isArray(decoded.textData), "Decoded text_data is not an array");
      console.log('✓ Decoded text_data is an array');
      
      // If OCR worked, there should be some text data
      if (decoded.textData.length > 0) {
        console.log(`✓ OCR detected ${decoded.textData.length} text elements`);
        
        // Log the first text element
        const firstText = decoded.textData[0];
        console.log(`  First text: "${firstText.text}" at (${firstText.x}, ${firstText.y})`);
      } else {
        console.log('⚠ OCR did not detect any text (this might be normal depending on OCR quality)');
      }
      
      console.log('✓ Test 1 passed');
    } catch (error) {
      console.error('✗ Test 1 failed:', error.message);
      throw error;
    }
    
    // Test 2: Encode with options
    console.log('\nTest 2: Encode with options');
    try {
      // Test with different options
      const options = { includeConfidence: false, imageFormat: 'jpeg' };
      
      // Encode with options
      const base64PlusData = await base64plus.encodeBase64Plus(TEST_IMAGE_PATH, options);
      console.log('✓ Successfully encoded image with options');
      
      // Check that the result is valid JSON
      const data = JSON.parse(base64PlusData);
      console.log('✓ Encoded data is valid JSON');
      
      // Check format
      assert.equal(
        data.format.toLowerCase(),
        options.imageFormat.toLowerCase(),
        `Incorrect format: expected ${options.imageFormat.toLowerCase()}, got ${data.format.toLowerCase()}`
      );
      console.log(`✓ Image format is correct: ${data.format}`);
      
      // Check confidence
      if (!options.includeConfidence && data.text_data.length > 0) {
        // If confidence should be excluded and we have text data,
        // check that no item has a confidence field
        for (const item of data.text_data) {
          assert(!item.hasOwnProperty('confidence'), "Confidence field present when includeConfidence=false");
        }
        console.log('✓ Confidence field correctly excluded');
      }
      
      console.log('✓ Test 2 passed');
    } catch (error) {
      console.error('✗ Test 2 failed:', error.message);
      throw error;
    }
    
    // Test 3: Render with bounding boxes
    console.log('\nTest 3: Render with bounding boxes');
    try {
      // Encode the test image
      const base64PlusData = await base64plus.encodeBase64Plus(TEST_IMAGE_PATH);
      
      // Decode the data
      const decoded = await base64plus.decodeBase64Plus(base64PlusData);
      
      // Render with bounding boxes
      const outputPath = path.join(__dirname, 'visualization.png');
      await base64plus.renderWithBoundingBoxes(decoded, outputPath);
      console.log('✓ Successfully rendered image with bounding boxes');
      
      // Check that the file exists
      assert(fs.existsSync(outputPath), "Visualization file was not created");
      console.log('✓ Visualization file was created');
      
      // Clean up the visualization file
      fs.unlinkSync(outputPath);
      console.log('✓ Cleaned up visualization file');
      
      console.log('✓ Test 3 passed');
    } catch (error) {
      console.error('✗ Test 3 failed:', error.message);
      throw error;
    }
    
    console.log('\n✅ All tests passed!');
  } catch (error) {
    console.error('\n❌ Tests failed:', error);
    process.exitCode = 1;
  } finally {
    // Clean up
    cleanup();
  }
}

// Run the tests
runTests();