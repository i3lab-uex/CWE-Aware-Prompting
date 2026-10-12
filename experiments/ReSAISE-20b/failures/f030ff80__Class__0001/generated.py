import hashlib

# List of supported hash algorithms provided by hashlib
SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    hash_type : str
        Name of the hash algorithm to use. Must be one of the supported algorithms.
    pass_input : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If an unsupported hash algorithm is requested.
    """
    if hash_type not in SUPPORTED_HASHES:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_HASHES))}"
        )

    # Use hashlib.new to create a hash object for the specified algorithm
    hasher = hashlib.new(hash_type)
    # Encode the password to bytes using UTF-8 before hashing
    hasher.update(pass_input.encode('utf-8'))
    return hasher.hexdigest()