import hashlib
import time
import string
import itertools

def main():
    # Start timing
    start_time = time.time()
    
    # Read hash values from file
    with open('hash5.txt', 'r') as f:
        target_hashes = [line.strip() for line in f.readlines()]
    
    # Create a dictionary to store the results
    results = {}
    remaining_hashes = set(target_hashes)
    total_hashes = len(remaining_hashes)
    
    # Define character set: lowercase letters and numbers
    charset = string.ascii_lowercase + string.digits
    
    # Calculate total combinations for progress tracking
    total_combinations = len(charset) ** 5
    print(f"Starting brute force of {total_hashes} hashes...")
    print(f"Total possible combinations: {total_combinations:,}")
    
    # Counter for progress tracking
    counter = 0
    last_update = time.time()
    update_interval = 2  # seconds between progress updates
    
    # Generate all possible 5-character strings and check their hashes
    for combo in itertools.product(charset, repeat=5):
        # Convert tuple to string
        plaintext = ''.join(combo)
        
        # Calculate MD5 hash
        hash_value = hashlib.md5(plaintext.encode()).hexdigest()
        
        # Check if this hash is one of our targets
        if hash_value in remaining_hashes:
            results[hash_value] = plaintext
            remaining_hashes.remove(hash_value)
            print(f"Found: {plaintext} -> {hash_value} ({len(results)}/{total_hashes})")
            
            # If we've found all hashes, we can stop
            if not remaining_hashes:
                break
        
        # Update progress periodically
        counter += 1
        current_time = time.time()
        if current_time - last_update > update_interval:
            elapsed = current_time - start_time
            progress = counter / total_combinations * 100
            combinations_per_sec = counter / elapsed if elapsed > 0 else 0
            print(f"Progress: {progress:.4f}% | Combinations tried: {counter:,} | Speed: {combinations_per_sec:.0f} combinations/sec")
            last_update = current_time
    
    # Calculate total time
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print results
    print(f"\nAll hashes reversed in {total_time:.2f} seconds")
    
    # Save results to file
    with open('ex2_hash.txt', 'w') as f:
        for hash_val, plaintext in sorted(results.items()):
            f.write(f"{plaintext}\n")
    
    print(f"Results saved to ex2_hash.txt")

if __name__ == "__main__":
    main()
