import hashlib

# Supported hash algorithms as defined in the description
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported.
    """
    if not isinstance(algorithm_name, str):
        raise TypeError("algorithm_name must be a string")
    if not isinstance(raw_password, str):
        raise TypeError("raw_password must be a string")

    algo = algorithm_name.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Convert password to bytes; use UTF-8 encoding
    pwd_bytes = raw_password.encode('utf-8')

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)

    return hasher.hexdigest()