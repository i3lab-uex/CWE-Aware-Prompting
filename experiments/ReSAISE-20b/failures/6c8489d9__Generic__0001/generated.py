import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'md5', etc.).
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hash value.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalise algorithm name to lower case (hashlib uses lower‑case names)
    algo = hash_name.lower()

    # Check if the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object
    h = hashlib.new(algo)

    # Update the hash with the password encoded in UTF‑8
    h.update(password.encode('utf-8'))

    # Return the hexadecimal digest
    return h.hexdigest()