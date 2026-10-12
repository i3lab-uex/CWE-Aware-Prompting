import hashlib

# Set of supported hash algorithm names in hashlib
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
    Hashes the provided password using the specified hash algorithm.

    Parameters
    ----------
    encryption_method : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    user_password : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Normalise the method name to lower case for comparison
    algorithm = encryption_method.lower()

    if algorithm not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: " + ", ".join(sorted(_SUPPORTED_ALGORITHMS))
        )

    # Create a new hash object using the chosen algorithm
    hasher = hashlib.new(algorithm)

    # Encode the password to bytes (UTF-8 is a safe default)
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()