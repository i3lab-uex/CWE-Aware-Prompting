import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use. Must be one of the algorithms supported by
        :mod:`hashlib`. The list includes: {'sha512_256', 'sha224', 'sha384',
        'sha512_224', 'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
        'sha256', 'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
        'md5', 'sha3_256', 'blake2s', 'sha3_512', 'sha3_224'}.
    secret : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the provided algorithm name is not supported or unavailable.
    """
    try:
        # Create a new hash object for the specified algorithm
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # Algorithm not available on this platform
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'."
        ) from exc

    # Encode the secret to bytes (UTF-8) before hashing
    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()