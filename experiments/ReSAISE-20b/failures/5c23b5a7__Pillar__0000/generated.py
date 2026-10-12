import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha512', 'sha256').
    user_password : bytes
        Password to be hashed. Must be a byte string.

    Returns
    -------
    bytes
        The raw hash digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalize algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    # Check if the requested algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()