import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm (e.g., 'sha512', 'sha256', etc.).
    user_pass : bytes
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
    # Normalize algorithm name to lower case for consistency
    algo = algorithm_name.lower()

    # Ensure the requested algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_pass)

    # Return the digest as bytes
    return hasher.digest()