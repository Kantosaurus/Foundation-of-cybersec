def decrypt(text, key):
    """
    Decrypts the given text using a simple Caesar cipher with the provided key.
    
    :param text: The text to decrypt.
    :param key: The number of positions to reverse shift each character.
    :return: The decrypted text.
    """
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shift = key % 26
            if char.islower():
                decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text 