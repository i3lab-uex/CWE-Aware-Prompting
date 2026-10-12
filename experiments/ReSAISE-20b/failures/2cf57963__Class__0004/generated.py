import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algorithm : str
        Name of a hash algorithm supported by the local OpenSSL installation.
    pass_key : str
        The password to be hashed.

    Returns
    -------
    bytes
        Raw digest of the hash function applied to ``pass_key``.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system or if it is a known weak algorithm.
    """
    # List of algorithms that are considered insecure for password hashing
    _WEAK_ALGORITHMS = {"md5", "md5-sha1", "sha1"}

    # Ensure the algorithm name is case‑insensitive
    algo = algorithm.lower()

    # Check if the algorithm exists in this environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm}' is not supported on this system.")

    # Reject algorithms known to be weak for password hashing
    if algo in _WEAK_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{algorithm}' is considered insecure for password hashing.")

    # Compute the digest
    hasher = hashlib.new(algo)
    hasher.update(pass_key.encode("utf-8"))
    return hasher.digest()