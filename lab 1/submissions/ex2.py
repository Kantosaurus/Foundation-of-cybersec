#!/usr/bin/env python3
import argparse
import os
import sys
import glob

def validate_key(key):
    """Validate that the key is within the acceptable range (0-255)."""
    if not (0 <= key <= 255):
        print(f"Error: Key must be between 0 and 255 (8-bit integer)")
        sys.exit(1)

def check_files(input_name, output_name=None, mode=None):
    """Check if input file exists and handle output files."""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Split the input name into base name and extension (if provided)
    base_name, ext = os.path.splitext(input_name)
    
    if ext:  # If extension was provided
        # Check for exact file match first
        exact_file = os.path.join(script_dir, input_name)
        if os.path.exists(exact_file):
            selected_input = exact_file
        else:
            print(f"Error: '{input_name}' is not in the folder, please put the file in the same folder as the script!")
            sys.exit(1)
    else:
        # If no extension provided or exact file not found, search for files with the base name
        matching_files = glob.glob(os.path.join(script_dir, f"{base_name}.*"))
        
        if not matching_files:
            print(f"Error: '{base_name}' is not in the folder, please put the file in the same folder as the script!")
            sys.exit(1)
        
        if len(matching_files) == 1:
            selected_input = matching_files[0]
        else:
            print(f"\nMultiple files found with name '{base_name}':")
            for i, file in enumerate(matching_files, 1):
                print(f"{i}. {os.path.basename(file)}")
            
            while True:
                try:
                    choice = int(input("\nPlease choose a file number: "))
                    if 1 <= choice <= len(matching_files):
                        selected_input = matching_files[choice - 1]
                        break
                    else:
                        print("Invalid choice. Please select a valid number.")
                except ValueError:
                    print("Please enter a valid number.")

    # Handle output files
    input_base = os.path.splitext(os.path.basename(selected_input))[0]
    input_ext = os.path.splitext(selected_input)[1]
    operation = "encrypted" if mode == 'e' else "decrypted"

    if output_name is None:
        # Generate default names for both output files
        output_original = f"{input_base}_{operation}{input_ext}"
        output_txt = f"{input_base}_{operation}_hex.txt"
    else:
        # Use provided name but ensure proper extensions
        output_base = os.path.splitext(output_name)[0]
        output_original = f"{output_base}{input_ext}"
        output_txt = f"{output_base}_hex.txt"

    output_original_path = os.path.join(script_dir, output_original)
    output_txt_path = os.path.join(script_dir, output_txt)

    # If input is already a .txt file, we'll only output one .txt file
    if input_ext.lower() == '.txt':
        return selected_input, output_original_path, None

    # Check if output files exist
    for output_path, output_name in [(output_original_path, output_original), (output_txt_path, output_txt)]:
        if os.path.exists(output_path):
            while True:
                response = input(f"Output file '{output_name}' already exists. Do you want to overwrite it? (y/n): ").lower()
                if response == 'y':
                    break
                elif response == 'n':
                    print("Operation cancelled.")
                    sys.exit(0)
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
    
    return selected_input, output_original_path, output_txt_path

def bytes_to_hex_string(data):
    """Convert bytes to a formatted hex string with ASCII representation."""
    result = []
    hex_lines = []
    ascii_lines = []
    
    for i in range(0, len(data), 16):
        # Get current 16 bytes
        chunk = data[i:i+16]
        
        # Create hex representation
        hex_line = ' '.join(f'{b:02x}' for b in chunk)
        hex_line = f'{hex_line:<48}'  # Pad with spaces to align ASCII
        
        # Create ASCII representation
        ascii_line = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        
        # Add offset
        line = f'{i:08x}  {hex_line}  |{ascii_line}|'
        result.append(line)
    
    return 'Offset    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  |ASCII|\n' + \
           '-' * 75 + '\n' + \
           '\n'.join(result)

def encrypt(data, key):
    """Encrypt the bytes using the given key."""
    result = bytearray()
    for byte in data:
        # Add key and wrap around using modulo 256 (for 8-bit arithmetic)
        encrypted_byte = (byte + key) % 256
        result.append(encrypted_byte)
    return bytes(result)

def decrypt(data, key):
    """Decrypt the bytes using the given key."""
    result = bytearray()
    for byte in data:
        # Subtract key and wrap around using modulo 256 (for 8-bit arithmetic)
        decrypted_byte = (byte - key) % 256
        result.append(decrypted_byte)
    return bytes(result)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using byte-level Caesar cipher')
    parser.add_argument('-i', '--input', required=True, help='Input filename (with or without extension)')
    parser.add_argument('-o', '--output', required=False, help='Output filename (optional, will default to inputname_encrypted/decrypted)')
    parser.add_argument('-k', '--key', required=True, type=int, help='Encryption/decryption key (0-255)')
    parser.add_argument('-m', '--mode', required=True, help='Mode: e for encryption, d for decryption')

    # Parse arguments
    args = parser.parse_args()

    # Validate key
    validate_key(args.key)

    # Validate mode
    mode = args.mode.lower()
    if mode not in ['e', 'd']:
        print("Error: Mode must be either 'e' (encryption) or 'd' (decryption)")
        print("Available options: e, d")
        sys.exit(1)

    try:
        # Check files before processing and get the selected input file
        input_file, output_file, output_txt_file = check_files(args.input, args.output, mode)

        # Read input file in binary mode
        with open(input_file, 'rb') as f:
            data = f.read()

        # Process the data
        if mode == 'e':
            result = encrypt(data, args.key)
            print(f"Encryption example for first byte:")
            if len(data) > 0:
                print(f"Original byte: 0x{data[0]:02x}")
                print(f"Key: 0x{args.key:02x}")
                print(f"Encrypted byte: 0x{result[0]:02x}")
        else:  # mode == 'd'
            result = decrypt(data, args.key)
            print(f"Decryption example for first byte:")
            if len(data) > 0:
                print(f"Encrypted byte: 0x{data[0]:02x}")
                print(f"Key: 0x{args.key:02x}")
                print(f"Decrypted byte: 0x{result[0]:02x}")

        # Write output file in binary mode
        with open(output_file, 'wb') as f:
            f.write(result)

        # Write hex representation to txt file if needed
        if output_txt_file:
            with open(output_txt_file, 'w') as f:
                f.write(bytes_to_hex_string(result))

        print(f"\nSuccessfully {'encrypted' if mode == 'e' else 'decrypted'} the file.")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        if output_txt_file:
            print(f"Hex output file: {output_txt_file}")

    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 