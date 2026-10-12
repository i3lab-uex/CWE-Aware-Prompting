import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    user_pass : bytes
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the password using the requested algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is valid
    if algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algorithm_name.lower())
    hasher.update(user_pass)

    # Return the raw digest bytes
    return hasher.digest()