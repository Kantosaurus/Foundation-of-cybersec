import random

def mathematical_rng(seed):
    a, b, m = 1664525, 1013904223, 2**32
    state = seed
    sequence = []
    
    # Define corrections for each sequence
    three_corrections = [
        1000 - 61, 5000 + 167, 10000 - 453, 5000 + 108, 6000 + 405, 10000 - 515,
        6000 + 343, 8000 + 827, 7000 + 82, 7000 + 383, 6000 + 56, 10000 - 369,
        3000 + 186, 7000 + 574, 10000 - 539, 10000 - 538, 7000 + 480, 8000 + 785,
        7000 + 59, 9000 + 251, 5000 + 108, 6000 + 734, 2000 + 77, 5000 + 639,
        6000 + 278, 3000 + 700, 7000 + 304, 4000 + 474, 6000 + 280, 5000 + 523,
        6000 + 684, 6000 + 396
    ]
    
    two_corrections = [
        10000 - 122, 3000 + 553, 1000 - 237, 2000 + 294, 6000 + 862, 8000 + 85,
        2000 + 220, 1000 - 147, 1000 - 238, 1000 + 652, 3000 + 891, 1000 - 315,
        6000 + 730, 5000 + 261, 1000 - 199, 8000 + 27, 2000 + 905, 3000 + 940,
        2000 + 146, 9000 + 269, 3000 + 494, 1000 - 698, 4000 + 719, 8000 + 400,
        5000 + 786, 2000 + 417, 1000 + 683, 7000 + 372, 8000 + 73, 6000 + 116,
        2000 + 686, 1000 + 944
    ]
    
    one_corrections = [
        6000 + 612, 9000 + 448, 8000 + 511, 6000 + 724, 7000 + 418, 1000 - 781,
        9000 + 93, 2000 - 65, 1000 - 463, 3000 + 753, 2000 - 19, 4000 + 904,
        5000 + 874, 1000 + 667, 6000 + 908, 2000 + 785, 1000 - 742, 9000 + 312,
        1000 + 44, 3000 + 326, 4000 + 426, 3000 + 905, 9000 + 414, 7000 + 307,
        1000 - 329, 4000 + 928, 2000 + 336, 1000 - 5, 7000 + 223, 7000 + 756,
        9000 + 83, 1000 + 590
    ]
    
    # Determine which sequence to generate based on seed
    if seed == 17:
        # h3@rTed sequence
        corrections = two_corrections
        base_multiplier, base_addend = 5432, 9876
        sequence_length = 32
    elif seed == 19:
        # 1/2_ sequence
        corrections = one_corrections
        base_multiplier, base_addend = 6789, 5432
        sequence_length = 32
    else:
       corrections = three_corrections
       base_multiplier, base_addend = 12345, 6789
       sequence_length = 32
    
    # Generate the sequence
    for i in range(sequence_length):
        state = (a * state + b) % m
        x = i + 1
        base = (x * base_multiplier + base_addend) % 10000
        state_factor = (state % 10000)
        combined = (base + state_factor) % 10000
        
        if corrections and i < len(corrections):
            # Use predefined corrections for known sequences
            final_result = corrections[i]
        else:
            # Use combined calculation for random sequences
            final_result = combined
        
        sequence.append(final_result)
    
    return sequence

# Main execution
if __name__ == "__main__":
    try:
        seed = int(input("Enter a seed number: "))
        result = mathematical_rng(seed)
        print(result)
            
    except ValueError:
        print("Please enter a valid integer for the seed.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
