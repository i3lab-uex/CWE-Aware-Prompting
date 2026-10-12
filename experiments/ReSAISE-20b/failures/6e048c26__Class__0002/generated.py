import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha512', 'blake2b', etc.).
    user_pass : bytes
        The password to hash. It must be a byte string.

    Returns
    -------
    bytes
        The raw digest of the hash operation.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python environment.
    """
    # Normalise the algorithm name to lower case as hashlib expects
    alg = algorithm_name.lower()

    # Verify that the algorithm is supported
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the hash object and compute the digest
    hasher = hashlib.new(alg)
    hasher.update(user_pass)
    return hasher.digest()