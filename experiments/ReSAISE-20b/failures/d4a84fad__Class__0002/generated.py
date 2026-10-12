import hashlib

# Set of supported hash algorithms for this function
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns the
    hexadecimal representation of the hash.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use.
    user_password : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If `encryption_method` is not in the list of supported algorithms.
    """
    # Normalise algorithm name (hashlib expects lowercase)
    method = encryption_method.lower()

    if method not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(method)
    hasher.update(user_password.encode('utf-8'))

    return hasher.hexdigest()