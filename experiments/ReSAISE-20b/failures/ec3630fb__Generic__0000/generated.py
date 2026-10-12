import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hash a password using the specified hash algorithm and return its hexadecimal representation.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2b', etc.).
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal string of the computed hash.

    Raises
    ------
    ValueError
        If `hash_type` is not supported by the current hashlib implementation.
    """
    # Normalize algorithm name (hashlib is case‑insensitive but may contain hyphens)
    algo = hash_type.lower().replace('-', '')

    # Verify that the algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_type}' is not available in this Python environment.")

    # Create a new hash object and feed it the password bytes
    h = hashlib.new(algo)
    h.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return h.hexdigest()