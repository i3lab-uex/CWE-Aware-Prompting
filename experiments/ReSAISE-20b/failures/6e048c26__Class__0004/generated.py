import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the cryptographic hash algorithm to use (e.g. 'sha256', 'blake2b').
    user_pass : bytes
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash value.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Ensure the algorithm name is supported
    if algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algorithm_name.lower())
    hasher.update(user_pass)

    # Return the digest as bytes
    return hasher.digest()