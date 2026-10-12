import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    pass_key : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest bytes of the hashed password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available on this system.
    """
    # Normalise algorithm name to lower case
    algo = algorithm.lower()

    # Ensure the requested algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pass_key.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()