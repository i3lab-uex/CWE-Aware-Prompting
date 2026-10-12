import hashlib

# Supported hash algorithms (as returned by hashlib.algorithms_available)
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}


def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of *data* using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'md5').
    data : bytes
        The binary data to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If *hash_name* is not a supported hash algorithm.
    """
    if not isinstance(hash_name, str):
        raise TypeError("hash_name must be a string")
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    # Normalise the algorithm name (hashlib is case‑sensitive)
    algo = hash_name.lower()
    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available")

    # Create a new hash object and update it with the data
    hasher = hashlib.new(algo)
    hasher.update(data)

    # Return the digest as bytes
    return hasher.digest()