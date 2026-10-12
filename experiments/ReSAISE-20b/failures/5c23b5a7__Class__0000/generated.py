import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be present in hashlib.algorithms_available.
    user_password : bytes
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure algorithm name is case-insensitive and trimmed
    alg = algorithm_name.strip().lower()

    # Check if the algorithm is available in hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object for the chosen algorithm
    try:
        hasher = hashlib.new(alg)
    except (ValueError, TypeError) as exc:
        # This block is defensive; the previous check should prevent it
        raise ValueError(f"Failed to create hash object for algorithm '{algorithm_name}': {exc}") from exc

    # Update the hasher with the password bytes
    hasher.update(user_password)

    # Return the digest as raw bytes
    return hasher.digest()