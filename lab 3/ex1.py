import hashlib

# Function to compute MD5 hash
def compute_md5(text):
    result = hashlib.md5(text.encode())
    return result.hexdigest()

# Strings of different lengths
strings = [
    "a",                  # 1 character
    "hello",              # 5 characters
    "cybersecurity",      # 13 characters
    "This is a longer string with spaces",  # 35 characters
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget felis euismod."  # 83 characters
]

print("MD5 Hash Demonstration\n")
print("String Length | MD5 Hash")
print("-" * 50)

for s in strings:
    md5_hash = compute_md5(s)
    print(f"'{s}'")
    print(f"Length: {len(s)} characters")
    print(f"MD5 Hash: {md5_hash}")
    print("-" * 50)

# Note: On Windows PowerShell, you can compute MD5 hash using:
# Get-FileHash -Algorithm MD5 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes("your text")))
#
# On Linux/macOS, you can use:
# echo -n "your text" | md5sum
