import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    user_password : bytes
        The password to hash.

    Returns
    -------
    bytes
        The computed digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalize algorithm name to lowercase for consistency
    algo = algorithm_name.lower()

    # Verify that the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hash_obj = hashlib.new(algo)
    hash_obj.update(user_password)

    # Return the digest as bytes
    return hash_obj.digest()