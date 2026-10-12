import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    user_password : bytes
        Password to hash.

    Returns
    -------
    bytes
        The computed digest of the password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the current Python environment.
    """
    # Normalize algorithm name (hashlib expects lowercase names)
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()