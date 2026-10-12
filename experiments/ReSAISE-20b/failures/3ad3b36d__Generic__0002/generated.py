import hashlib

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    raw_password : str
        The password string to be hashed.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported.
    """
    # Supported algorithms (case‑insensitive)
    SUPPORTED_ALGORITHMS = {
        'sha512_256', 'sha224', 'sha384', 'sha512_224',
        'sha512', 'sm3', 'sha1', 'sha3_384',
        'shake_128', 'sha256', 'blake2b', 'md5-sha1',
        'shake_256', 'ripemd160', 'md5', 'sha3_256',
        'blake2s', 'sha3_512', 'sha3_224'
    }

    algo = algorithm_name.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: '{algorithm_name}'. "
                         f"Supported algorithms are: {', '.join(sorted(SUPPORTED_ALGORITHMS))}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(raw_password.encode('utf-8'))

    return hasher.hexdigest()