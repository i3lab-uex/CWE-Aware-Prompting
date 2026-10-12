import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hash algorithm (e.g. 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python environment.
    """
    # Normalize algorithm name (case-insensitive)
    algo = hash_algorithm.lower()

    # Verify that the requested algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()