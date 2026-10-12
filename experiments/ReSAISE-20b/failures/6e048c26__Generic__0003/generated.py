import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    user_pass : bytes
        The password to hash. It must be a byte string.

    Returns
    -------
    bytes
        The binary digest produced by the hash function.

    Raises
    ------
    ValueError
        If `algorithm_name` is not a supported algorithm.
    """
    # Normalise the algorithm name to lower case
    algo = algorithm_name.lower()

    # Validate that the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and feed the password
    hasher = hashlib.new(algo)
    hasher.update(user_pass)

    # Return the digest as bytes
    return hasher.digest()