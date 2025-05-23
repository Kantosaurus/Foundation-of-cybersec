# Foundation of Cybersecurity

This repository contains labs and exercises for the Foundation of Cybersecurity course.

## Lab 1: Encryption and Decryption

This lab focuses on implementing and understanding encryption techniques, specifically Caesar ciphers.

### Files:

- **ex1.py**: Command-line tool for text file encryption/decryption using Caesar cipher (text-based)
- **ex2.py**: Command-line tool for binary file encryption/decryption using byte-level Caesar cipher
- **encrypt.py**: Module with functions for text encryption using Caesar cipher
- **decrypt.py**: Module with functions for text decryption using Caesar cipher
- **file_checker.py**: Utility to verify file existence and validity
- **key_checker.py**: Utility to validate encryption/decryption keys
- **flag**: Encrypted file for practice
- **sherlock_short.txt**: Sample text file for encryption/decryption practice

### Usage Examples:

#### Text File Encryption/Decryption (ex1.py)
```
python ex1.py -i input.txt -o output.txt -k 3 -m e  # Encrypt with key 3
python ex1.py -i encrypted.txt -o decrypted.txt -k 3 -m d  # Decrypt with key 3
```

#### Binary File Encryption/Decryption (ex2.py)
```
python ex2.py -i input.bin -o output.bin -k 5 -m e  # Encrypt with key 5
python ex2.py -i encrypted.bin -o decrypted.bin -k 5 -m d  # Decrypt with key 5
```

### Assignment Files:
- **Homework1_2025(1).pdf**: Assignment details and requirements
- **cybersecurity lab 1(2).pdf**: Lab instructions and guide
