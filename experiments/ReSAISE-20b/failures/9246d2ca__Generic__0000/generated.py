import hashlib

# List of supported algorithms as per the provided description
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    pass_key : bytes
        Password to be hashed.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported.
    """
    if algo_name.lower() not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and compute the digest
    hash_obj = hashlib.new(algo_name)
    hash_obj.update(pass_key)
    return hash_obj.digest()