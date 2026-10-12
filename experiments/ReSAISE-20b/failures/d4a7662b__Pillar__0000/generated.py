import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hash algorithm (e.g. 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        Binary digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python
        installation or the underlying OpenSSL library.
    """
    # Normalise algorithm name (hashlib is case‑insensitive)
    algo_name = hash_algorithm.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm!r}")

    # Create a new hash object and update it with the password bytes
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:          # pragma: no cover
        # Some algorithms may be available in the name set but not actually
        # implemented due to platform restrictions.
        raise ValueError(f"Failed to initialise hash algorithm {hash_algorithm!r}") from exc

    hasher.update(pwd.encode('utf-8'))
    return hasher.digest()