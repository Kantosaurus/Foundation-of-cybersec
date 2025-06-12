import argparse
import string
from collections import Counter
import re
import nltk
from nltk.corpus import words
import itertools
from tabulate import tabulate

# Download the word list if not already downloaded
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

def load_text(filename):
    """
    Safely reads the input file without modifying it.
    Returns the content in uppercase for analysis.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().upper()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except PermissionError:
        print(f"Error: Permission denied to read file '{filename}'.")
        exit(1)

def get_letter_frequency(text):   # Count only letters
    letters = re.findall(r'[A-Z]', text)
    return Counter(letters)

def get_english_frequency():
    return {
        'E': 12.70, 'T': 9.10, 'A': 8.20, 'O': 7.50, 'I': 6.97,
        'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
        'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
        'Z': 0.07
    }

def get_english_words():
    return set(word.upper() for word in words.words())

def create_initial_mapping(text_freq, english_freq): # Sort both frequency distributions
    text_letters = sorted(text_freq.items(), key=lambda x: x[1], reverse=True)
    english_letters = sorted(english_freq.items(), key=lambda x: x[1], reverse=True)
    mapping = {}
    for (encrypted, _), (decrypted, _) in zip(text_letters, english_letters):
        mapping[encrypted] = decrypted
    
    return mapping

def decrypt_text(text, mapping):
    result = []
    for char in text:
        if char in string.ascii_uppercase:
            result.append(mapping.get(char, char))
        else:
            result.append(char)
    return ''.join(result)

def get_words(text):   # Split text into words, preserving punctuation
    return re.findall(r'\b[A-Z]+\b', text)

def score_decryption(decrypted_text, english_words):
    words = get_words(decrypted_text)
    if not words:
        return 0   # Count how many words are valid English words
    valid_words = sum(1 for word in words if word in english_words)
    return valid_words / len(words)

def find_best_mapping(text, initial_mapping, english_words, max_iterations=100):
    best_mapping = initial_mapping.copy()
    best_score = score_decryption(decrypt_text(text, best_mapping), english_words)
    
    for _ in range(max_iterations):
        current_mapping = best_mapping.copy()
        improved = False
        for letter1, letter2 in itertools.combinations(string.ascii_uppercase, 2):
            if letter1 in current_mapping and letter2 in current_mapping:
                current_mapping[letter1], current_mapping[letter2] = current_mapping[letter2], current_mapping[letter1]
                current_score = score_decryption(decrypt_text(text, current_mapping), english_words)        
                if current_score > best_score:
                    best_score = current_score
                    best_mapping = current_mapping.copy()
                    improved = True
                else:
                    current_mapping[letter1], current_mapping[letter2] = current_mapping[letter2], current_mapping[letter1]   
        if not improved:
            break
    return best_mapping, best_score

def save_solution(decrypted_text, filename='solution.txt'):
    """
    Saves the decrypted text to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(decrypted_text)
        print(f"\nDecrypted text has been saved to {filename}")
    except PermissionError:
        print(f"Error: Permission denied to write to file '{filename}'.")
    except Exception as e:
        print(f"Error saving solution: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Automatic frequency analysis decryption (read-only)')
    parser.add_argument('-i', '--input', required=True, help='Input file containing encrypted text (will not be modified)')
    args = parser.parse_args()

    # Load and process the text (read-only operation)
    encrypted_text = load_text(args.input)
    text_freq = get_letter_frequency(encrypted_text)
    english_freq = get_english_frequency()
    english_words = get_english_words()

    # Create initial mapping
    initial_mapping = create_initial_mapping(text_freq, english_freq)
    
    # Find best mapping
    best_mapping, best_score = find_best_mapping(encrypted_text, initial_mapping, english_words)
    
    # Decrypt text with best mapping
    decrypted_text = decrypt_text(encrypted_text, best_mapping)

    # Prepare table data
    table_data = []
    for letter in string.ascii_uppercase:
        if letter in text_freq:
            table_data.append([
                letter,  # Encrypted letter
                text_freq[letter],  # Frequency in encrypted text
                f"{text_freq[letter]/sum(text_freq.values())*100:.2f}%",  # Percentage
                best_mapping.get(letter, '-'),  # Mapped to
                f"{english_freq.get(best_mapping.get(letter, 'E'), 0):.2f}%"  # Expected frequency
            ])

    # Print results
    print("\nFrequency Analysis Results:")
    print(tabulate(
        table_data,
        headers=['Letter', 'Count', 'Frequency', 'Maps To', 'Expected %'],
        tablefmt='grid'
    ))
    
    print(f"\nDecryption quality score: {best_score:.2%}")
    print("\nDecrypted text:")
    print(decrypted_text)

    # Save the solution
    save_solution(decrypted_text)

if __name__ == "__main__":
    main()
