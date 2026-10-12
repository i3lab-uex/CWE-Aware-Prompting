import hashlib

# List of algorithms explicitly mentioned in the description.
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384',
    'shake_128', 'sha256', 'blake2b', 'md5-sha1',
    'shake_256', 'ripemd160', 'md5', 'sha3_256',
    'blake2s', 'sha3_512', 'sha3_224'
}

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the cryptographic hash algorithm to use.
    user_pass : bytes
        The password in binary form that should be hashed.

    Returns
    -------
    bytes
        The resulting hash value.

    Raises
    ------
    ValueError
        If the supplied algorithm is not supported.
    """
    if algorithm_name.lower() not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    try:
        hasher = hashlib.new(algorithm_name)
    except (ValueError, TypeError) as exc:
        # hashlib will raise ValueError if the algorithm is unknown
        raise ValueError(f"Hash algorithm '{algorithm_name}' not available.") from exc

    hasher.update(user_pass)
    return hasher.digest()