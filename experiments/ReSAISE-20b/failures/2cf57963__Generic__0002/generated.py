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
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Normalize algorithm name to lowercase (hashlib accepts case-insensitive names)
    algo = algorithm.lower()

    # Verify that the requested algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new hash object and feed it the password encoded as UTF-8
    hasher = hashlib.new(algo)
    hasher.update(pass_key.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()