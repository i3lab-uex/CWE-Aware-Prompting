import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalize the hash type name
    algo = hash_type.lower()

    # Verify that the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_type}")

    # Create a new hash object and feed the password
    hasher = hashlib.new(algo)
    # Encode using UTF-8 to ensure consistent byte representation
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()