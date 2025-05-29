import argparse
import os
from key_checker import validate_key

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
    parser.add_argument('input_file', help='Path to the encrypted file')
    parser.add_argument('key', type=int, help='Decryption key (0-255)')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Validate the key
    is_valid, message = validate_key(args.key, key_type='byte')
    if not is_valid:
        print(f"Error: {message}")
        return
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        return
    
    # Generate output filename if not provided
    if args.output:
        output_file = args.output
    else:
        base, ext = os.path.splitext(args.input_file)
        output_file = f"{base}_decrypted{ext}"
    
    try:
        # Decrypt the file
        decrypted_data = decrypt_file(args.input_file, args.key)
        
        # Save the decrypted file
        save_file(decrypted_data, output_file)
        print(f"Successfully decrypted file to: {output_file}")
        
    except Exception as e:
        print(f"Error during decryption: {str(e)}")

if __name__ == '__main__':
    main() 