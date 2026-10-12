import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    plain_text_pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or unavailable.
    """
    # Normalize algorithm name (hashlib accepts lower‑case names)
    algo = hash_algorithm.lower()

    # Check if the algorithm is available on this platform
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()