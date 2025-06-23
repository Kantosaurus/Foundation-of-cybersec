import random
import hashlib

def select_random_words(filename, num_words=300):
    """Randomly select words from a file"""
    words = []
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            # Read all lines and split into words
            all_words = []
            for line in file:
                all_words.extend(line.strip().split())
            
            print(f"Total words found in file: {len(all_words)}")
            
            # Randomly select 300 words
            if len(all_words) >= num_words:
                selected_words = random.sample(all_words, num_words)
            else:
                selected_words = all_words  # If file has fewer than 300 words
            
            print(f"Selected {len(selected_words)} words")
            return selected_words
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def hash_words_md5(words):
    """Hash each word with MD5 and return as a single string"""
    hashed_words = []
    for word in words:
        # Hash the word with MD5
        md5_hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        hashed_words.append(md5_hash)
    
    # Join all hashes into one line
    return ' '.join(hashed_words)

def randomly_break_into_lines(text, min_lines=5, max_lines=20):
    """Randomly break text into a random number of lines"""
    words = text.split()
    num_lines = random.randint(min_lines, max_lines)
    
    # Calculate words per line (approximately)
    words_per_line = len(words) // num_lines
    remainder = len(words) % num_lines
    
    lines = []
    word_index = 0
    
    for i in range(num_lines):
        # Add extra word to first 'remainder' lines to distribute evenly
        current_line_words = words_per_line + (1 if i < remainder else 0)
        line_words = words[word_index:word_index + current_line_words]
        lines.append(' '.join(line_words))
        word_index += current_line_words
    
    return '\n'.join(lines)

# Select 300 random words from rockyou.txt
rockyou_path = "lab 3/rockyou.txt"
selected_words = select_random_words(rockyou_path, 300)

if selected_words:
    # Hash all words with MD5 and put them on one line
    hashed_line = hash_words_md5(selected_words)
    print(f"Hashed line length: {len(hashed_line)}")
    print(f"First 100 characters of hashed line: {hashed_line[:100]}")
    
    # Randomly break into lines
    final_text = randomly_break_into_lines(hashed_line)
    print(f"Final text has {final_text.count(chr(10)) + 1} lines")
    
    # Write to encrypted.txt
    with open("self-challenges/encypted.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(final_text)
    
    print(f"Successfully processed 300 random words from {rockyou_path}")
    print(f"Hashed and formatted text written to self-challenges/encypted.txt")
else:
    print("No words were selected. Please check the rockyou.txt file.") 