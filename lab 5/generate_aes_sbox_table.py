#!/usr/bin/env python3
# Generate AES S-box Table 4.3 and save as table2.txt (official values)

from gf2n import Polynomial2, GF2N

def byte_to_bits_lsb(byte):
    # Convert integer to 8-bit vector, LSB first
    return [(byte >> i) & 1 for i in range(8)]

def bits_to_byte_lsb(bits):
    # Convert 8-bit vector (LSB first) to integer
    return sum([bits[i] << i for i in range(8)])

def aes_affine_transform(byte):
    # Official AES affine transformation (LSB first)
    # y_i = b_i ^ b_{(i+4)%8} ^ b_{(i+5)%8} ^ b_{(i+6)%8} ^ b_{(i+7)%8} ^ c_i
    c = [1,1,0,0,0,1,1,0]  # 0x63, LSB first
    b = byte_to_bits_lsb(byte)
    out = []
    for i in range(8):
        val = b[i] ^ b[(i+4)%8] ^ b[(i+5)%8] ^ b[(i+6)%8] ^ b[(i+7)%8] ^ c[i]
        out.append(val)
    return bits_to_byte_lsb(out)

def generate_aes_sbox_table(filename="table2.txt"):
    ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])  # AES irreducible polynomial
    sbox = []
    for byte in range(256):
        if byte == 0:
            sbox_val = 0x63
        else:
            g = GF2N(byte, 8, ip)
            inv = g.mulInv().getInt()
            sbox_val = aes_affine_transform(inv)
        sbox.append(sbox_val)

    # Write to file in the format of Table 4.3
    with open(filename, 'w') as f:
        f.write("Table 4.3  AES S-Box: Substitution values in hexadecimal notation for input byte (xy)\n")
        f.write("    |" + " ".join(f" {x:X}" for x in range(16)) + "\n")
        f.write("----+" + "----"*16 + "\n")
        for row in range(16):
            f.write(f" {row:X} |")
            for col in range(16):
                val = sbox[row*16 + col]
                f.write(f" {val:02X}")
            f.write("\n")
    print(f"AES S-box table saved to {filename}")

if __name__ == "__main__":
    generate_aes_sbox_table() 