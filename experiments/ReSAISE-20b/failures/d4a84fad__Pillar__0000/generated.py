import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use. Must be one of the algorithms supported by hashlib.
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If `encryption_method` is not a supported hash algorithm.
    """
    # List of algorithms that hashlib can create via `hashlib.new`
    supported_algorithms = {
        'sha512_256', 'sha224', 'sha384', 'sha512_224',
        'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
        'sha256', 'blake2b', 'md5-sha1', 'shake_256',
        'ripemd160', 'md5', 'sha3_256', 'blake2s',
        'sha3_512', 'sha3_224'
    }

    if encryption_method.lower() not in supported_algorithms:
        raise ValueError(f"Unsupported hash algorithm: '{encryption_method}'. "
                         f"Supported algorithms are: {', '.join(sorted(supported_algorithms))}")

    # Encode the password to bytes; UTF-8 is a safe default
    password_bytes = user_password.encode('utf-8')

    # Create the hash object and compute digest
    hasher = hashlib.new(encryption_method.lower())
    hasher.update(password_bytes)
    return hasher.hexdigest()