#!/usr/bin/env python3
# Generate addition and multiplication tables for GF(2^4)
# Using irreducible polynomial x^4 + x^3 + 1

from gf2n import Polynomial2, GF2N

def generate_gf24_tables():
    # Define the irreducible polynomial: x^4 + x^3 + 1
    ip = Polynomial2([1, 0, 0, 1, 1])  # x^4 + x^3 + 1
    
    print("Generating GF(2^4) tables with irreducible polynomial:", ip)
    print("=" * 60)
    
    # Create all elements in GF(2^4) - 16 elements from 0 to 15
    elements = []
    for i in range(16):
        g = GF2N(i, 4, ip)
        elements.append(g)
    
    # Generate addition table
    print("\nAddition Table for GF(2^4):")
    print("-" * 60)
    
    # Header row
    header = "   |"
    for i in range(16):
        header += f" {i:2d} |"
    print(header)
    print("-" * 60)
    
    addition_table = []
    for i in range(16):
        row = f" {i:2d} |"
        row_data = []
        for j in range(16):
            result = elements[i].add(elements[j])
            result_int = result.getInt()
            row += f" {result_int:2d} |"
            row_data.append(result_int)
        print(row)
        addition_table.append(row_data)
    
    # Generate multiplication table
    print("\nMultiplication Table for GF(2^4):")
    print("-" * 60)
    
    # Header row
    print(header)
    print("-" * 60)
    
    multiplication_table = []
    for i in range(16):
        row = f" {i:2d} |"
        row_data = []
        for j in range(16):
            result = elements[i].mul(elements[j])
            result_int = result.getInt()
            row += f" {result_int:2d} |"
            row_data.append(result_int)
        print(row)
        multiplication_table.append(row_data)
    
    return addition_table, multiplication_table

def save_tables_to_file(addition_table, multiplication_table, filename="table1.txt"):
    """Save the tables to a text file"""
    with open(filename, 'w') as f:
        f.write("GF(2^4) Tables with irreducible polynomial x^4 + x^3 + 1\n")
        f.write("=" * 60 + "\n\n")
        
        # Save addition table
        f.write("Addition Table:\n")
        f.write("-" * 60 + "\n")
        
        # Header
        header = "   |"
        for i in range(16):
            header += f" {i:2d} |"
        f.write(header + "\n")
        f.write("-" * 60 + "\n")
        
        # Table content
        for i in range(16):
            row = f" {i:2d} |"
            for j in range(16):
                row += f" {addition_table[i][j]:2d} |"
            f.write(row + "\n")
        
        f.write("\n" + "=" * 60 + "\n\n")
        
        # Save multiplication table
        f.write("Multiplication Table:\n")
        f.write("-" * 60 + "\n")
        
        # Header
        f.write(header + "\n")
        f.write("-" * 60 + "\n")
        
        # Table content
        for i in range(16):
            row = f" {i:2d} |"
            for j in range(16):
                row += f" {multiplication_table[i][j]:2d} |"
            f.write(row + "\n")
    
    print(f"\nTables saved to {filename}")

def verify_tables(addition_table, multiplication_table):
    """Verify some properties of the tables"""
    print("\nVerifying table properties:")
    print("-" * 30)
    
    # Check addition properties
    print("Addition properties:")
    
    # Identity element (0)
    for i in range(16):
        if addition_table[0][i] != i or addition_table[i][0] != i:
            print(f"ERROR: 0 is not identity for addition at position {i}")
            return False
    print("✓ 0 is the identity element for addition")
    
    # Commutativity
    for i in range(16):
        for j in range(16):
            if addition_table[i][j] != addition_table[j][i]:
                print(f"ERROR: Addition not commutative at ({i}, {j})")
                return False
    print("✓ Addition is commutative")
    
    # Check multiplication properties
    print("\nMultiplication properties:")
    
    # Identity element (1)
    for i in range(16):
        if multiplication_table[1][i] != i or multiplication_table[i][1] != i:
            print(f"ERROR: 1 is not identity for multiplication at position {i}")
            return False
    print("✓ 1 is the identity element for multiplication")
    
    # Zero multiplication
    for i in range(16):
        if multiplication_table[0][i] != 0 or multiplication_table[i][0] != 0:
            print(f"ERROR: 0 multiplication not working at position {i}")
            return False
    print("✓ 0 * x = x * 0 = 0 for all x")
    
    # Commutativity
    for i in range(16):
        for j in range(16):
            if multiplication_table[i][j] != multiplication_table[j][i]:
                print(f"ERROR: Multiplication not commutative at ({i}, {j})")
                return False
    print("✓ Multiplication is commutative")
    
    print("\nAll table properties verified successfully!")
    return True

def main():
    print("GF(2^4) Table Generator")
    print("Irreducible polynomial: x^4 + x^3 + 1")
    print("=" * 50)
    
    # Generate tables
    addition_table, multiplication_table = generate_gf24_tables()
    
    # Save to file
    save_tables_to_file(addition_table, multiplication_table)
    
    # Verify properties
    verify_tables(addition_table, multiplication_table)
    
    print(f"\nTable generation complete! Check table1.txt for the saved tables.")

if __name__ == "__main__":
    main() 