import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pass_key : bytes
        The password to hash. Must be a byte string.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Ensure that we are working with a bytes object
    if not isinstance(pass_key, (bytes, bytearray)):
        raise TypeError("pass_key must be a bytes-like object")

    # Validate algorithm name against the set of available algorithms
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)
    return hasher.digest()