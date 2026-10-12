import hashlib

# List of algorithms considered secure for password hashing purposes.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_224',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    # Additional algorithms that are still considered secure
    'sm3',          # Chinese SM3 hash
    'shake_128',
    'shake_256',
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of SECURE_ALGORITHMS.
    pw : str
        Password string to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If algo_name is not in SECURE_ALGORITHMS or the algorithm is not supported by hashlib.
    """
    algo_name = algo_name.lower()
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is not allowed or recognized as secure.")

    try:
        # Use hashlib.new to support all algorithms in a uniform way.
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # hashlib does not support the requested algorithm.
        raise ValueError(f"Algorithm '{algo_name}' is not available in this Python build.") from exc

    # Ensure the password is encoded to bytes (UTF-8 is a common choice).
    hasher.update(pw.encode('utf-8'))
    return hasher.digest()