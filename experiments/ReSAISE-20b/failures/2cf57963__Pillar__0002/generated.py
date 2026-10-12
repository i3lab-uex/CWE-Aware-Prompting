import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm (e.g., 'sha256').
    pass_key : str
        The password to be hashed.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported by the current Python installation.
    """
    # Ensure the algorithm name is in a consistent case
    algo = algorithm.lower()

    # Determine supported algorithms (both guaranteed and available)
    supported_algorithms = hashlib.algorithms_available
    if algo not in supported_algorithms:
        raise ValueError(
            f"Hash algorithm '{algorithm}' is not supported on this system."
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo)
    # Encode using UTF-8 to ensure consistent byte representation
    hasher.update(pass_key.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()