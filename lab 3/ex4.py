import hashlib
import csv
from itertools import product
import string
import os

def read_hashes(filename):
    """Read hashes from the file and return them as a list."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    hashes = []
    for line in lines:
        line = line.strip()
        # Skip empty lines and category headers
        if line and not line.startswith('==='):
            hashes.append(line)
    return hashes

def load_rockyou_wordlist(rockyou_path='C:/Users/wooai/OneDrive/Documents/Term 5/FCS/Foundation-of-cybersec/lab 3/rockyou.txt'):
    """
    Load passwords from rockyou.txt wordlist.
    Returns a list of passwords to try.
    """
    passwords = []
    
    if not os.path.exists(rockyou_path):
        print(f"Warning: rockyou.txt not found at {rockyou_path}")
        return []
    
    try:
        print(f"Loading passwords from {rockyou_path}...")
        with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                password = line.strip()
                if password:  # Only skip empty lines
                    passwords.append(password)
        print(f"Loaded {len(passwords)} passwords from rockyou.txt")
        return passwords
    except Exception as e:
        print(f"Error loading rockyou.txt: {e}")
        return []

def try_common_passwords():
    """Return a list of common passwords to try."""
    return [
        'password', '123456', 'admin', 'letmein', 'welcome',
        'monkey', 'dragon', 'football', 'baseball', 'abc123',
        'qwerty', '111111', '123123', 'admin123', 'test123',
        'princess', 'dragon', 'password1', '12345', 'monkey',
        'login', 'princess', 'abc123', 'trustno1', 'shadow',
        'master', '666666', 'qwertyuiop', '123321', 'mustang',
        'michael', '654321', 'pussy', 'superman', '1qaz2wsx',
        'kevin', 'football', 'charlie', 'master', 'password1',
        'ninja', 'azerty', '123', 'solo', 'loveme', 'whatever',
        'donald', 'dragon', 'charles', 'cheese', 'admin',
        'secret', 'passw0rd', 'asdf', 'kopi', 'xkcd',
        # Common variations
        'Password', 'Password1', 'P@ssword', 'p@ssword',
        'admin1', 'admin12', 'root123', 'toor',
    ]

def generate_pattern_passwords():
    """Generate passwords following common patterns."""
    patterns = []
    
    # Common years
    years = [str(year) for year in range(1990, 2024)]
    patterns.extend(years)
    
    # Common number sequences
    for i in range(10000):
        patterns.append(f"{i:04d}")
    
    # Common words with numbers
    words = ['pass', 'pwd', 'admin', 'user', 'test', 'root', 'login',
            'sys', 'system', 'web', 'dev', 'hack', 'secure']
    numbers = ['123', '1234', '12345', '123456', '321', '456', '654',
              '111', '222', '333', '777', '888', '999']
    
    for word in words:
        # Try word variations
        patterns.append(word)
        patterns.append(word.capitalize())
        patterns.append(word.upper())
        # Word + number combinations
        for num in numbers:
            patterns.append(f"{word}{num}")
            patterns.append(f"{num}{word}")
            patterns.append(f"{word.capitalize()}{num}")
            patterns.append(f"{word.upper()}{num}")
    
    # Common character substitutions
    substitutions = {
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$',
        'b': '8', 't': '7', 'g': '9', 'l': '1'
    }
    
    base_words = ['password', 'admin', 'secret', 'secure', 'system']
    for word in base_words:
        # Try all possible single character substitutions
        for i in range(len(word)):
            if word[i] in substitutions:
                new_word = word[:i] + substitutions[word[i]] + word[i+1:]
                patterns.append(new_word)
                patterns.append(new_word + '123')
    
    return patterns

def brute_force_short(max_length=5):
    """Generate all possible combinations up to max_length."""
    # Include uppercase letters for very short attempts
    chars = string.ascii_lowercase + string.digits
    if max_length <= 3:
        chars += string.ascii_uppercase
    
    for length in range(1, max_length + 1):
        for attempt in product(chars, repeat=length):
            yield ''.join(attempt)

def crack_single_hash(target_hash, rockyou_passwords, common_passwords, pattern_passwords):
    """
    Try to crack a single hash using multiple methods.
    Returns the password if found, None otherwise.
    """
    # Dictionary to store MD5 hashes we've already computed
    hash_cache = {}
    
    def try_password(password):
        """Try a password and return True if it matches the target hash."""
        if password in hash_cache:
            md5_hash = hash_cache[password]
        else:
            md5_hash = hashlib.md5(password.encode()).hexdigest()
            hash_cache[password] = md5_hash
            
        return md5_hash == target_hash
    
    # Method 1: Try every entry in rockyou.txt
    print(f"Trying rockyou.txt for hash: {target_hash}")
    for i, password in enumerate(rockyou_passwords):
        if try_password(password):
            print(f"  ✓ Cracked with rockyou.txt: {password}")
            return password
        # Progress update every 50000 attempts
        if i % 50000 == 0 and i > 0:
            print(f"    Processed {i} passwords from rockyou.txt...")
    
    # Method 2: Try common passwords
    print(f"  Trying common passwords for hash: {target_hash}")
    for password in common_passwords:
        if try_password(password):
            print(f"  ✓ Cracked with common passwords: {password}")
            return password
    
    # Method 3: Try pattern-based passwords
    print(f"  Trying pattern-based passwords for hash: {target_hash}")
    for password in pattern_passwords:
        if try_password(password):
            print(f"  ✓ Cracked with pattern-based passwords: {password}")
            return password
    
    # Method 4: Try brute force for short passwords
    print(f"  Trying brute force for hash: {target_hash}")
    for password in brute_force_short(5):
        if try_password(password):
            print(f"  ✓ Cracked with brute force: {password}")
            return password
    
    print(f"  ✗ Could not crack hash: {target_hash}")
    return None

def crack_hashes(hash_list):
    """Try to crack each hash individually using multiple methods."""
    cracked = {}
    
    # Load all password lists
    print("Loading password lists...")
    rockyou_passwords = load_rockyou_wordlist()
    common_passwords = try_common_passwords()
    pattern_passwords = generate_pattern_passwords()
    
    print(f"Starting to crack {len(hash_list)} hashes...")
    
    # Try to crack each hash individually
    for i, target_hash in enumerate(hash_list):
        print(f"\n[{i+1}/{len(hash_list)}] Processing hash: {target_hash}")
        
        password = crack_single_hash(target_hash, rockyou_passwords, common_passwords, pattern_passwords)
        
        if password:
            cracked[target_hash] = password
            print(f"Progress: {len(cracked)}/{len(hash_list)} hashes cracked")
        else:
            print(f"Progress: {len(cracked)}/{len(hash_list)} hashes cracked (this one failed)")
    
    return cracked

def save_results(cracked, output_file):
    """Save the cracked hashes to a CSV file."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['md5_hash', 'plaintext'])  # Header
        for md5_hash, plaintext in sorted(cracked.items()):
            writer.writerow([md5_hash, plaintext])

def main():
    # Read hashes from the file
    hashes = read_hashes('hashes.txt')
    print(f"Loaded {len(hashes)} hashes to crack")
    
    # Try to crack the hashes
    cracked = crack_hashes(hashes)
    
    # Save results
    save_results(cracked, 'ex4.csv')
    
    # Print summary
    print(f"\nSummary:")
    print(f"Total hashes: {len(hashes)}")
    print(f"Cracked hashes: {len(cracked)}")
    print(f"Success rate: {len(cracked)/len(hashes)*100:.1f}%")
    print(f"Results saved to ex4.csv")
    
    # Show uncracked hashes
    uncracked = set(hashes) - set(cracked.keys())
    if uncracked:
        print(f"\nUncracked hashes ({len(uncracked)}):")
        for hash_val in sorted(uncracked):
            print(f"  {hash_val}")

if __name__ == '__main__':
    main()
