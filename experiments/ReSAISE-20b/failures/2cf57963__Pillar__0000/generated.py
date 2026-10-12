import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256').
    pass_key : str
        The password string to be hashed.

    Returns
    -------
    bytes
        The binary digest produced by the hash function.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Normalise algorithm name (hashlib accepts lower‑case)
    algo_name = algorithm.lower()

    # Verify that the algorithm is available on this platform
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm}' is not supported on this system.")

    # Create a new hash object and feed it the password bytes
    hash_obj = hashlib.new(algo_name)
    # Encode the password using UTF-8 to avoid encoding issues
    hash_obj.update(pass_key.encode('utf-8'))

    # Return the raw digest bytes
    return hash_obj.digest()