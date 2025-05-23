import argparse
import string
import os

def validate_inputs(args):
    # Validate key
    try:
        key = int(args.key)
        if key < 1 or key > len(string.printable) - 1:
            print(f"Error: Key must be between 1 and {len(string.printable) - 1}.")
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

def encrypt(text, key):
    result = ""
    for char in text:
        if char in string.printable:
            # Get the index of the character in the printable set
            index = string.printable.index(char)
            # Apply the shift (with wrapping)
            new_index = (index + key) % len(string.printable)
            # Get the new character
            result += string.printable[new_index]
        else:
            # Keep non-printable characters as they are
            result += char
    return result

def decrypt(text, key):
    result = ""
    for char in text:
        if char in string.printable:
            # Get the index of the character in the printable set
            index = string.printable.index(char)
            # Apply the reverse shift (with wrapping)
            new_index = (index - key) % len(string.printable)
            # Get the new character
            result += string.printable[new_index]
        else:
            # Keep non-printable characters as they are
            result += char
    return result

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a text file using Caesar cipher.')
    parser.add_argument('-i', '--input', required=True, help='Input filename')
    parser.add_argument('-o', '--output', required=True, help='Output filename')
    parser.add_argument('-k', '--key', required=True, help='Key for encryption/decryption')
    parser.add_argument('-m', '--mode', required=True, help="Mode: 'e' for encryption, 'd' for decryption")
    
    args = parser.parse_args()
    
    if not validate_inputs(args):
        return
    
    key = int(args.key)
    mode = args.mode.lower()
    
    try:
        # Read input file
        with open(args.input, 'r', encoding='utf-8') as infile:
            text = infile.read()
        
        # Process the text
        if mode == 'e':
            result = encrypt(text, key)
        else:  # mode == 'd'
            result = decrypt(text, key)
        
        # Write to output file
        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(result)
        
        print(f"File processed successfully. Output written to '{args.output}'.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 