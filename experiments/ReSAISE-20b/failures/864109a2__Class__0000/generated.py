import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hashes a plaintext password using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    plain_text_pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Ensure the algorithm name is case‑insensitive
    algo = hash_algorithm.lower()

    # Check if the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Please choose a supported algorithm from hashlib.algorithms_available."
        )

    # Create the hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()