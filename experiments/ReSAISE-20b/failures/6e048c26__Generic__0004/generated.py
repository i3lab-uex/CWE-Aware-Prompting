import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha512', 'blake2b', etc.).
    user_pass : bytes
        The password to hash. Must be a byte string.

    Returns
    -------
    bytes
        The binary digest produced by the chosen hash algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    TypeError
        If `user_pass` is not of type `bytes`.
    """
    if not isinstance(user_pass, bytes):
        raise TypeError("user_pass must be a bytes object")

    # Use the algorithm names as provided by hashlib; they are case-sensitive.
    if algorithm_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    hasher = hashlib.new(algorithm_name)
    hasher.update(user_pass)
    return hasher.digest()