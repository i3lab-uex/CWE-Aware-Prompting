import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (must be supported by hashlib).
    secret : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the hash type is supported
    if hash_type.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_type}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(hash_type.lower())

    # Update the hash with the password bytes (UTF-8 encoding)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()