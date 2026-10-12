import hashlib

# Set of supported hash algorithms (as reported by hashlib.algorithms_available)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384',
    'shake_128', 'sha256', 'blake2b', 'md5-sha1',
    'shake_256', 'ripemd160', 'md5', 'sha3_256',
    'blake2s', 'sha3_512', 'sha3_224'
}

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        The name of the hash function to use (e.g. 'sha256').
    secret : str
        The password string that will be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If `hash_type` is not supported by hashlib.
    """
    # Normalise the algorithm name to match hashlib's naming conventions
    hash_type_clean = hash_type.lower().replace('-', '_')

    if hash_type_clean not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {hash_type}")

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(hash_type_clean)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()