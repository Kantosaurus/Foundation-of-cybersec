import argparse
import os
from key_checker import validate_key

def has_png_chunks(data):
    """
    Check if the data contains valid PNG chunks
    """
    # Look for common PNG chunks like IHDR, IDAT, IEND
    png_chunks = [b'IHDR', b'IDAT', b'IEND', b'PLTE', b'tRNS']
    return any(chunk in data for chunk in png_chunks)

def detect_file_type(data):
    """
    Detect the file type from decrypted data using signatures and content analysis
    
    :param data: Bytes of the decrypted data
    :return: String describing the detected file type, or None if unknown
    """
    # First check for exact signatures at the start
    signatures = {
        b'%PDF': 'PDF document',
        b'\x89PNG\r\n\x1a\n': 'PNG image',
        b'\xff\xd8\xff': 'JPEG image',
        b'PK\x03\x04': 'ZIP archive',
        b'GIF87a': 'GIF image',
        b'GIF89a': 'GIF image',
        b'\x1f\x8b\x08': 'GZIP archive',
        b'#!/': 'Shell script',
        b'<?xml': 'XML document',
        b'<!DOCTYPE': 'HTML document',
        b'-----BEGIN': 'PEM certificate/key',
    }
    
    # Check for known file signatures
    for signature, file_type in signatures.items():
        if data.startswith(signature):
            return file_type
    
    # Secondary checks for file types that might not have perfect signatures
    # Check for PNG chunks anywhere in the file
    if has_png_chunks(data):
        return 'PNG image (detected from chunks)'
    
    # Check for JPEG markers
    jpeg_markers = [b'\xff\xd8', b'\xff\xe0', b'\xff\xe1', b'\xff\xdb', b'\xff\xc0']
    if any(marker in data[:20] for marker in jpeg_markers):
        return 'JPEG image'
    
    # Check if it might be a text file
    try:
        text_sample = data[:100].decode('utf-8')
        # Check if the text contains mostly printable ASCII characters
        printable = sum(32 <= ord(c) <= 126 or c in '\n\r\t' for c in text_sample)
        if printable > len(text_sample) * 0.8:  # If 80% of characters are printable
            return 'Text file'
    except:
        pass
    
    # Additional binary analysis
    # Check for high entropy (typical in compressed/encrypted data)
    byte_counts = {}
    for byte in data[:1024]:  # Check first 1KB
        byte_counts[byte] = byte_counts.get(byte, 0) + 1
    
    unique_bytes = len(byte_counts)
    if unique_bytes > 200:  # High entropy might indicate compressed/encrypted data
        return 'Binary data (possibly compressed/encrypted)'
    
    return 'Unknown file type'

def decrypt_file(input_file, key):
    """
    Decrypt a file using the given key.
    
    :param input_file: Path to the file to decrypt
    :param key: Decryption key (0-255)
    :return: Decrypted bytes
    """
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Decrypt each byte
    decrypted = bytearray()
    for byte in data:
        decrypted_byte = (byte - key) % 256
        decrypted.append(decrypted_byte)
    
    return bytes(decrypted)

def save_file(data, output_file):
    """
    Save the decrypted data to a file.
    
    :param data: Bytes to save
    :param output_file: Path to save the file to
    """
    with open(output_file, 'wb') as f:
        f.write(data)

def main():
    parser = argparse.ArgumentParser(description='Decrypt a file using a shift cipher')
    parser.add_argument('-i', '--input', dest='input_file', help='Path to the encrypted file', required=True)
    parser.add_argument('-k', '--key', type=int, help='Decryption key (0-255)', default=None)
    parser.add_argument('-o', '--output', dest='output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        return

    # If key is provided, only try that key
    if args.key is not None:
        # Validate the key
        is_valid, message = validate_key(args.key, key_type='byte')
        if not is_valid:
            print(f"Error: {message}")
            return
        
        keys_to_try = [args.key]
    else:
        # Try all possible keys
        print("No key provided. Trying all possible keys (0-255)...")
        keys_to_try = range(256)

    # Try each key
    for key in keys_to_try:
        try:
            decrypted_data = decrypt_file(args.input_file, key)
            
            # Detect file type
            file_type = detect_file_type(decrypted_data)
            
            print(f"\nKey {key}:")
            print(f"Detected file type: {file_type}")
            
            # For PNG images, print additional confirmation
            if 'PNG' in file_type:
                print("PNG chunks found:", [chunk.decode('ascii', errors='ignore') 
                                          for chunk in [b'IHDR', b'IDAT', b'IEND', b'PLTE', b'tRNS'] 
                                          if chunk in decrypted_data])
            
            # If it's a text file, show a preview
            if file_type == 'Text file':
                try:
                    decoded_text = decrypted_data[:100].decode('utf-8')
                    print(f"Preview: {decoded_text}")
                except:
                    pass
            
            # If output file is specified and we're using a specific key
            if args.output and args.key is not None:
                save_file(decrypted_data, args.output)
                print(f"Successfully saved decrypted file to: {args.output}")
            
        except Exception as e:
            print(f"Error during decryption with key {key}: {str(e)}")

if __name__ == '__main__':
    main() 