import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    pass_key : bytes
        The password (or any byte sequence) to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalize the algorithm name (hashlib expects lower‑case)
    algo_name = algo_name.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name!r}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)

    # Return the digest as bytes
    return hasher.digest()