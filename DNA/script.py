import random
import os

def generate_rna_sequence(length=17):
    """
    Generate a random RNA sequence of specified length using A, U, G, C.
    """
    rna_bases = ['A', 'U', 'G', 'C']
    sequence = ''.join(random.choice(rna_bases) for _ in range(length))
    return sequence

def get_unique_filename(base_name="RNA.txt"):
    """
    Generate a unique filename by appending a number if the file already exists.
    """
    if not os.path.exists(base_name):
        return base_name
    
    name, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(f"{name}_{counter}{ext}"):
        counter += 1
    
    return f"{name}_{counter}{ext}"

def reformat_rna_file(filename="RNA.txt"):
    """
    Read RNA.txt and reformat it so all lines are exactly 17 characters.
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return
    
    # Read the file
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Remove any empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    
    # Reformat each line to be exactly 17 characters
    reformatted_lines = []
    for line in lines:
        if len(line) <= 17:
            # Pad with random RNA bases if shorter than 17
            while len(line) < 17:
                line += random.choice(['A', 'U', 'G', 'C'])
            reformatted_lines.append(line)
        else:
            # Split longer lines into chunks of 17 characters
            for i in range(0, len(line), 17):
                chunk = line[i:i+17]
                if len(chunk) < 17:
                    # Pad the last chunk if it's shorter than 17
                    while len(chunk) < 17:
                        chunk += random.choice(['A', 'U', 'G', 'C'])
                reformatted_lines.append(chunk)
    
    # Save the reformatted content
    output_filename = get_unique_filename("RNA_reformatted.txt")
    with open(output_filename, 'w') as f:
        for line in reformatted_lines:
            f.write(line + '\n')
    
    print(f"Reformatted {len(lines)} original lines into {len(reformatted_lines)} lines of 17 characters each.")
    print(f"Saved to: {output_filename}")
    
    # Show a preview
    print("\nPreview of reformatted file:")
    print("-" * 50)
    for i, line in enumerate(reformatted_lines[:10]):  # Show first 10 lines
        print(f"{i+1:3d}. {line} ({len(line)} chars)")
    if len(reformatted_lines) > 10:
        print("...")
        for i, line in enumerate(reformatted_lines[-5:]):  # Show last 5 lines
            print(f"{len(reformatted_lines)-4+i:3d}. {line} ({len(line)} chars)")

def main():
    print("RNA Sequence Generator")
    print("1. Generate new RNA sequences")
    print("2. Reformat existing RNA.txt file")
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "2":
        reformat_rna_file()
        return
    
    # Generate 500 random RNA sequences
    num_sequences = 500
    sequence_length = 17
    
    # The three specific sequences to inject (full sequences)
    special_sequences = [
        "AUGUCGCGAAAAGUAUACAGGCACUCCAACGUGUGCCCAAUUGGCUGUGCGAGAGUUAGACGUUAUUUAA",
        "AUGGAGUGUGGUUUGGAUCCACACAAGCGGAAAACUAGGUCAGCCCCAGUAUUUUUGAUUAUGCCGGUAG", 
        "AUGUUAUCAGGGGUAUAUGACUAAGGUGCUUUAAGUGCCCUGCCGGUGUUCGCCAUCAAAACACGACUGA"
    ]
    
    print(f"Generating {num_sequences} random RNA sequences of length {sequence_length}...")
    print("-" * 50)
    
    # Generate all random sequences
    sequences = []
    for i in range(num_sequences):
        rna_sequence = generate_rna_sequence(sequence_length)
        sequences.append(rna_sequence)
    
    # Randomly inject the special sequences (full length)
    for special_seq in special_sequences:
        # Choose a random position to insert
        insert_position = random.randint(0, len(sequences))
        sequences.insert(insert_position, special_seq)
    
    # Get unique filename
    filename = get_unique_filename()
    
    # Save sequences to file
    with open(filename, 'w') as f:
        for sequence in sequences:
            f.write(sequence + '\n')
    
    # Print all sequences to console as well
    for sequence in sequences:
        print(sequence)
    
    print("-" * 50)
    print(f"Generated {len(sequences)} RNA sequences successfully!")
    print(f"Injected {len(special_sequences)} special sequences at random positions.")
    print(f"Saved to file: {filename}")
    
    # Automatically reformat the generated file
    print("\nAutomatically reformatting file to ensure all lines are 17 characters...")
    reformat_rna_file(filename)

if __name__ == "__main__":
    main() 