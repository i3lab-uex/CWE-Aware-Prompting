import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    pass_key : bytes
        The password to hash. Must be a bytes-like object.

    Returns
    -------
    bytes
        The binary digest produced by the hash algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    TypeError
        If `pass_key` is not a bytes-like object.

    Notes
    -----
    The function uses :func:`hashlib.new` to create a hash object.  It does
    not perform any additional key stretching (e.g., PBKDF2) because the
    specification only requests a simple hash.  For real-world password
    storage, consider using a dedicated key‑derivation function such as
    :func:`hashlib.pbkdf2_hmac` or a library like ``passlib``.
    """
    if not isinstance(pass_key, (bytes, bytearray)):
        raise TypeError("pass_key must be a bytes-like object")

    # Normalize algorithm name to lower case for consistency
    algo_name = algo_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create the hash object and compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)
    return hasher.digest()