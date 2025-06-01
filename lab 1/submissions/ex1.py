import argparse
import string
import sys
import os
import glob

def validate_key(key):
    """Validate that the key is within the acceptable range."""
    if not (1 <= key <= len(string.printable) - 1):
        print(f"Error: Key must be between 1 and {len(string.printable)-1}")
        sys.exit(1)

def is_printable_file(filepath):
    """Check if file contains only printable characters."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            return all(char in string.printable for char in content)
    except UnicodeDecodeError:
        return False

def check_files(input_name, output_name=None, mode=None):
    """Check if input file exists and handle output file overwrite."""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Split the input name into base name and extension (if provided)
    base_name, ext = os.path.splitext(input_name)
    
    if ext:  # If extension was provided
        # Check for exact file match first
        exact_file = os.path.join(script_dir, input_name)
        if os.path.exists(exact_file):
            if not is_printable_file(exact_file):
                print(f"Error: The file '{input_name}' cannot be encrypted or decrypted due to not having a printable input.")
                sys.exit(1)
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
        
        # Check if the selected file contains printable input
        if not is_printable_file(selected_input):
            print(f"Error: The file '{os.path.basename(selected_input)}' cannot be encrypted or decrypted due to not having a printable input.")
            sys.exit(1)

    # Handle output file
    if output_name is None:
        # If no output name provided, use input base name with appropriate suffix
        input_base = os.path.splitext(os.path.basename(selected_input))[0]
        suffix = "_encrypted.txt" if mode == 'e' else "_decrypted.txt"
        output_name = f"{input_base}{suffix}"
    else:
        # Ensure output has .txt extension
        output_base, output_ext = os.path.splitext(output_name)
        if output_ext and output_ext != '.txt':
            print(f"Warning: The script can only output .txt files. Changing extension from '{output_ext}' to '.txt'")
        output_name = f"{output_base}.txt"

    output_file = os.path.join(script_dir, output_name)
    
    # Check if output file exists
    if os.path.exists(output_file):
        while True:
            response = input(f"Output file '{output_name}' already exists. Do you want to overwrite it? (y/n): ").lower()
            if response == 'y':
                return selected_input, output_file
            elif response == 'n':
                print("Operation cancelled.")
                sys.exit(0)
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    return selected_input, output_file

def encrypt(text, key):
    """Encrypt the text using the given key."""
    result = ""
    for char in text:
        if char in string.printable:
            # Get the position in printable characters
            pos = string.printable.index(char)
            # Apply encryption formula and wrap around using modulo
            new_pos = (pos + key) % len(string.printable)
            # Get the new character
            result += string.printable[new_pos]
        else:
            result += char
    return result

def decrypt(text, key):
    """Decrypt the text using the given key."""
    result = ""
    for char in text:
        if char in string.printable:
            # Get the position in printable characters
            pos = string.printable.index(char)
            # Apply decryption formula and wrap around using modulo
            new_pos = (pos - key) % len(string.printable)
            # Get the new character
            result += string.printable[new_pos]
        else:
            result += char
    return result

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using Caesar cipher')
    parser.add_argument('-i', '--input', required=True, help='Input filename (with or without extension)')
    parser.add_argument('-o', '--output', required=False, help='Output filename (optional, will default to inputname_encrypted.txt or inputname_decrypted.txt)')
    parser.add_argument('-k', '--key', required=True, type=int, help='Encryption/decryption key')
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
        input_file, output_file = check_files(args.input, args.output, mode)

        # Read input file
        with open(input_file, 'r') as f:
            text = f.read()

        # Process the text
        if mode == 'e':
            result = encrypt(text, args.key)
        else:  # mode == 'd'
            result = decrypt(text, args.key)

        # Write output file
        with open(output_file, 'w') as f:
            f.write(result)

        print(f"\nSuccessfully {'encrypted' if mode == 'e' else 'decrypted'} the file.")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")

    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
