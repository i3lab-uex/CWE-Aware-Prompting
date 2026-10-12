import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha512', 'blake2b').
    user_pass : bytes
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the underlying hashlib implementation.
    """
    # Normalise algorithm name to lower case as required by hashlib
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create a new hash object and update it with the password.
    hasher = hashlib.new(algo)
    hasher.update(user_pass)

    # Return the digest as bytes.
    return hasher.digest()