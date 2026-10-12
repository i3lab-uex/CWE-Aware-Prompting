import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha512', 'blake2b').
    user_password : bytes
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lowercase (hashlib accepts case‑insensitive names)
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()