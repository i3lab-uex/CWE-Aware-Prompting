import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Args:
        algorithm_name: Name of a supported hash algorithm.
        user_password: Password to be hashed, as bytes.

    Returns:
        The raw digest of the hash algorithm applied to `user_password`.

    Raises:
        ValueError: If `algorithm_name` is not a supported hash algorithm.
    """
    # Normalize algorithm name to lower case as hashlib uses lowercase names
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available and supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()