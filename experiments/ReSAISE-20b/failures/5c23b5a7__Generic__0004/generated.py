import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (case‑insensitive).
    user_password : bytes
        The password data to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the current Python installation.
    """
    # Normalise algorithm name to lower case for lookup
    algo = algorithm_name.lower()

    # Verify that the algorithm is available in this environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()