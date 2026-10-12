import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system.
    """
    # Normalise algorithm name to lowercase (hashlib expects lower‑case names)
    algo = hash_algorithm.lower()

    # Check that the algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported on this system.")

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()