import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha512', 'blake2b', etc.).
    user_password : bytes
        The password to hash. Must be a byte string.

    Returns
    -------
    bytes
        The raw digest of the hash function applied to ``user_password``.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in :mod:`hashlib`.

    Notes
    -----
    - The function uses :func:`hashlib.new` to create the hash object.
    - It checks against ``hashlib.algorithms_available`` for algorithm support,
      which is the canonical list of algorithms supported by the underlying
      OpenSSL installation.
    - The returned value is the raw digest bytes; callers can encode it
      (e.g., hexlify) if a textual representation is required.
    """
    # Ensure the algorithm exists
    if algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create the hash object and feed it the password
    hasher = hashlib.new(algorithm_name)
    hasher.update(user_password)

    # Return the digest bytes
    return hasher.digest()