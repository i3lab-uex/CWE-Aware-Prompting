import hashlib

# Supported hash algorithms according to the description
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    raw_password : str
        The plaintext password.

    Returns
    -------
    str
        Hexadecimal hash of the password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported.
    """
    if algorithm_name.lower() not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Encode the password as UTF-8 before hashing
    pwd_bytes = raw_password.encode('utf-8')

    # Create a new hash object with the specified algorithm
    try:
        hasher = hashlib.new(algorithm_name.lower())
    except ValueError as exc:
        # This should not happen because we validated earlier,
        # but keep for safety
        raise ValueError(f"Failed to create hash object: {exc}") from exc

    hasher.update(pwd_bytes)
    return hasher.hexdigest()