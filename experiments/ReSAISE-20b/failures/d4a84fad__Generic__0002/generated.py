import hashlib

# Set of supported hash algorithm names (lowercase for case-insensitive matching)
_SUPPORTED_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',
    'sha1',
    'sha3_384',
    'shake_128',
    'sha256',
    'blake2b',
    'md5-sha1',
    'shake_256',
    'ripemd160',
    'md5',
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224',
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported.
    """
    # Normalise algorithm name to lower case
    algo = encryption_method.lower()

    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm '{encryption_method}'. "
                         f"Supported algorithms are: {', '.join(sorted(_SUPPORTED_ALGORITHMS))}")

    # Encode password to bytes (UTF-8 is a common, safe choice)
    password_bytes = user_password.encode('utf-8')

    # Create a new hash object using the chosen algorithm
    hasher = hashlib.new(algo)
    hasher.update(password_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()