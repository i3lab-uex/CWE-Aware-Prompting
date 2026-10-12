import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256').
    pass_key : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python runtime.
    """
    # Normalize algorithm name to lower case for consistency
    algo = algorithm.lower()

    # Check if the algorithm is available on this system.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the hasher and feed it the password bytes.
    hasher = hashlib.new(algo)
    hasher.update(pass_key.encode('utf-8'))

    return hasher.digest()