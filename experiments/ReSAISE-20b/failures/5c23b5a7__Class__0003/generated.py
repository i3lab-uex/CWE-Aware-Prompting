import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (e.g., 'sha512', 'blake2b').
    user_password : bytes
        The password to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If *algorithm_name* is not a supported hash algorithm in the current
        Python installation.

    Notes
    -----
    - The function accepts any algorithm available via ``hashlib.algorithms_available``.
      It does **not** automatically reject weak algorithms such as MD5 or SHA‑1,
      but callers should avoid them for production use.
    - The digest is returned as a byte string.  For storage or comparison,
      encode it with ``hex()`` or ``b64encode()`` as appropriate.
    """
    # Normalise the algorithm name to lower case for lookup
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the raw digest
    return hasher.digest()