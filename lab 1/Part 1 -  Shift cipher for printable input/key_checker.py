def validate_key(key):
    """
    Validates if the provided key is valid for the standard Caesar cipher.
    
    :param key: The key to validate (must be an integer between 1 and 25).
    :return: A tuple (is_valid, message) where is_valid is a boolean and message is a string.
    """
    try:
        key_val = int(key)
        if key_val < 1 or key_val > 25:
            return False, "Key must be an integer between 1 and 25 for standard Caesar cipher."
        return True, "Valid key"
    except ValueError:
        return False, "Key must be an integer for standard Caesar cipher." 