#!/usr/bin/env python3
import argparse
import os

def validate_inputs(args):
    # Validate key
    try:
        key = int(args.key)
        if key < 0 or key > 255:
            print(f"Error: Key must be between 0 and 255.")
            return False
    except ValueError:
        print("Error: Key must be an integer.")
        return False
    
    # Validate mode
    if args.mode.lower() not in ['e', 'd']:
        print("Error: Mode must be 'e' (encryption) or 'd' (decryption).")
        return False
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return False
    
    return True

def encrypt(data, key):
    # Create a new bytearray for the encrypted data
    result = bytearray(len(data))
    
    # Encrypt each byte by adding the key and applying modulo 256
    for i in range(len(data)):
        result[i] = (data[i] + key) % 256
    
    return result

def decrypt(data, key):
    # Create a new bytearray for the decrypted data
    result = bytearray(len(data))
    
    # Decrypt each byte by subtracting the key and applying modulo 256
    for i in range(len(data)):
        result[i] = (data[i] - key) % 256
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using byte-level Caesar cipher.')
    parser.add_argument('-i', '--input', required=True, help='Input filename')
    parser.add_argument('-o', '--output', required=True, help='Output filename')
    parser.add_argument('-k', '--key', required=True, help='Key for encryption/decryption (0-255)')
    parser.add_argument('-m', '--mode', required=True, help="Mode: 'e' for encryption, 'd' for decryption")
    
    args = parser.parse_args()
    
    if not validate_inputs(args):
        return
    
    key = int(args.key)
    mode = args.mode.lower()
    
    try:
        # Read input file in binary mode
        with open(args.input, 'rb') as infile:
            data = bytearray(infile.read())
        
        # Process the data
        if mode == 'e':
            result = encrypt(data, key)
        else:  # mode == 'd'
            result = decrypt(data, key)
        
        # Write to output file in binary mode
        with open(args.output, 'wb') as outfile:
            outfile.write(result)
        
        print(f"File processed successfully. Output written to '{args.output}'.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 