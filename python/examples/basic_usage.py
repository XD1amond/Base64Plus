"""
Basic usage example for Base64Plus Python library.
"""

import os
import json
from base64plus import encode_base64plus, decode_base64plus

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if sample image exists, otherwise provide instructions
    sample_image = os.path.join(current_dir, 'sample_image.jpg')
    if not os.path.exists(sample_image):
        print(f"Please place a sample image at {sample_image}")
        print("You can use any image with text in it.")
        return
    
    print(f"Processing image: {sample_image}")
    
    # Encode the image to Base64Plus format
    try:
        # Try with EasyOCR first, fall back to Tesseract if needed
        base64plus_data = encode_base64plus(
            sample_image,
            ocr_engine='auto',
            include_confidence=True
        )
        
        # Save the Base64Plus data to a file
        output_file = os.path.join(current_dir, 'output.b64p')
        with open(output_file, 'w') as f:
            f.write(base64plus_data)
        
        print(f"Base64Plus data saved to: {output_file}")
        
        # Parse and display some information about the encoded data
        data = json.loads(base64plus_data)
        print(f"Image format: {data.get('format', 'unknown')}")
        print(f"Number of text elements detected: {len(data['text_data'])}")
        
        # Print the first few text elements
        print("\nDetected text elements:")
        for i, item in enumerate(data['text_data'][:5]):  # Show first 5 elements
            print(f"{i+1}. Text: {item['text']}")
            print(f"   Position: x={item['x']}, y={item['y']}, width={item['width']}, height={item['height']}")
            if 'confidence' in item:
                print(f"   Confidence: {item['confidence']:.2f}")
        
        if len(data['text_data']) > 5:
            print(f"... and {len(data['text_data']) - 5} more elements")
        
        # Decode the Base64Plus data
        print("\nDecoding the Base64Plus data...")
        image, text_data = decode_base64plus(base64plus_data)
        
        # Save the decoded image
        decoded_image_path = os.path.join(current_dir, 'decoded_image.png')
        image.save(decoded_image_path)
        print(f"Decoded image saved to: {decoded_image_path}")
        
        print("\nBase64Plus encoding and decoding completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have installed the required dependencies:")
        print("   - For EasyOCR: pip install base64plus[easyocr]")
        print("   - For Tesseract: pip install base64plus[tesseract] and install Tesseract executable")
        print("2. Check that your image contains readable text")
        print("3. Try with a different OCR engine: encode_base64plus(image_path, ocr_engine='tesseract')")

if __name__ == "__main__":
    main()