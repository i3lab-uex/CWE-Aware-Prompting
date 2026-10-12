import hashlib

# List of supported hash algorithms provided by the problem description
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes the given password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters:
        encryption_method (str): Name of the hash algorithm to use.
        user_password (str): The password string to be hashed.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If an unsupported hash algorithm is requested.
    """
    # Normalize the method name to lower case for comparison
    algo = encryption_method.lower()

    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: '{encryption_method}'. "
                         f"Supported algorithms are: {', '.join(sorted(_SUPPORTED_ALGORITHMS))}")

    # Encode the password to bytes (UTF-8 is a safe default)
    pwd_bytes = user_password.encode('utf-8')

    # Create the hash object
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()