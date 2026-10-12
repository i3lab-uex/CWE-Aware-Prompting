import hashlib

# List of cryptographic hash algorithms considered secure for password hashing.
# Excludes legacy weak algorithms such as md5 and sha1.
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
    # sm3 is considered secure in some contexts but may not be available on all platforms
    'sm3',
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using a secure algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of the algorithms listed in SECURE_ALGORITHMS.
    pw : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name (hashlib accepts case‑insensitive names)
    algo_name = algo_name.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_name}' is not supported or considered insecure."
        )

    # Ensure the algorithm is available in this Python installation
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(
            f"Algorithm '{algo_name}' is not available in the current hashlib implementation."
        ) from exc

    # Encode the password as UTF‑8 bytes before hashing
    hasher.update(pw.encode('utf-8'))
    return hasher.digest()