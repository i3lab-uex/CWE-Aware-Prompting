import hashlib

# List of supported hash algorithm names as per the provided set.
_SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384',
    'shake_128', 'sha256', 'blake2b', 'md5-sha1',
    'shake_256', 'ripemd160', 'md5', 'sha3_256',
    'blake2s', 'sha3_512', 'sha3_224'
}

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of *data* using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'md5').
    data : bytes
        Data to hash.

    Returns
    -------
    bytes
        The raw digest of the data.

    Raises
    ------
    ValueError
        If *hash_name* is not supported or unavailable in the current environment.
    """
    # Normalise algorithm name: hashlib uses lowercase names
    alg = hash_name.lower()

    if alg not in _SUPPORTED_HASHES:
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported.")

    try:
        hasher = hashlib.new(alg)
    except (AttributeError, ValueError) as exc:
        # AttributeError for missing module; ValueError for unknown algorithm
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    hasher.update(data)
    return hasher.digest()