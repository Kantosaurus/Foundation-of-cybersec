def validate_key(key, key_type='standard'):
    """
    Validates if the provided key is valid for the specified cipher type.
    
    :param key: The key to validate, can be string or integer depending on cipher type.
    :param key_type: Type of cipher key ('standard' for Caesar cipher, 'byte' for byte-level encryption).
    :return: A tuple (is_valid, message) where is_valid is a boolean and message is a string.
    """
    if key_type == 'standard':
        try:
            key_val = int(key)
            if key_val < 1 or key_val > 25:
                return False, "Key must be an integer between 1 and 25 for standard Caesar cipher."
            return True, "Valid key"
        except ValueError:
            return False, "Key must be an integer for standard Caesar cipher."
    
    elif key_type == 'byte':
        try:
            key_val = int(key)
            if key_val < 0 or key_val > 255:
                return False, "Key must be an integer between 0 and 255 for byte-level encryption."
            return True, "Valid key"
        except ValueError:
            return False, "Key must be an integer for byte-level encryption."
    
    else:
        return False, "Unsupported key type specified." 