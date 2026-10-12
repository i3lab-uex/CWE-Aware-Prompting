import hashlib

# Set of supported hash algorithm names (as accepted by hashlib.new)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the supported algorithms.
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If an unsupported hash algorithm is specified.
    """
    if algorithm_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Convert password to bytes; UTF-8 is a common, safe encoding for passwords
    password_bytes = raw_password.encode('utf-8')

    # Create a new hash object using the chosen algorithm
    hasher = hashlib.new(algorithm_name)
    hasher.update(password_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()