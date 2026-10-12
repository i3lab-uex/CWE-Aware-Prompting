import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256').
    pass_key : str
        Password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python installation.
    """
    # Normalise algorithm name to lower case for consistency
    algo = algorithm.lower()

    # Verify that the algorithm is available on this system
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm}' is not supported on this system.")

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo)
    # Encode using UTF-8 to ensure consistent byte representation
    hasher.update(pass_key.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()