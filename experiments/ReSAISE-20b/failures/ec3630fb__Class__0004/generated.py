import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `hash_type` is not a supported hash algorithm.
    """
    # Ensure the requested algorithm is available
    if hash_type.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_type}' is not available.")

    # Create a new hash object and feed the password bytes
    h = hashlib.new(hash_type.lower())
    h.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return h.hexdigest()