import hashlib
import random
import string

def read_passwords(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []

def generate_salt():
    # Generate a random lowercase letter as salt
    return random.choice(string.ascii_lowercase)

def create_salted_hash(password, salt):
    # Concatenate password with salt and create MD5 hash
    salted_password = password + salt
    return hashlib.md5(salted_password.encode()).hexdigest()

def main():
    # Read the original hashes
    passwords = read_passwords('ex2_hash.txt')
    
    if not passwords:
        return
    
    salted_hashes = []
    salted_plains = []
    
    # Process each password
    for password in passwords:
        # Generate a random salt
        salt = generate_salt()
        
        # Create the salted hash
        salted_hash = create_salted_hash(password, salt)
        
        # Store the results
        salted_hashes.append(f"{salted_hash}:{salt}")
        salted_plains.append(f"{password}{salt}")
    
    # Save the salted hashes
    with open('salted6.txt', 'w') as file:
        for hash_salt in salted_hashes:
            file.write(hash_salt + '\n')
    
    # Save the plain salted passwords
    with open('plain6.txt', 'w') as file:
        for plain in salted_plains:
            file.write(plain + '\n')

if __name__ == "__main__":
    main()
