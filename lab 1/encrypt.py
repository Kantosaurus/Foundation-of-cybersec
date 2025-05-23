def encrypt(text, key):
    """
    Encrypts the given text using a simple Caesar cipher with the provided key.
    
    :param text: The text to encrypt.
    :param key: The number of positions to shift each character.
    :return: The encrypted text.
    """
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift = key % 26
            if char.islower():
                encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text