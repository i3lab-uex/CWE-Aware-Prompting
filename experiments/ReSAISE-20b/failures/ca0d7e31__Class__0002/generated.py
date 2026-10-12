import hashlib

# Supported hash algorithms as per the problem statement.
SUPPORTED_HASHES = {
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
        Name of the hash algorithm (must be one of SUPPORTED_HASHES).
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The digest of the input data.

    Raises
    ------
    ValueError
        If *hash_name* is not supported or unavailable on the current platform.
    """
    # Normalise name to lowercase for consistency
    alg = hash_name.lower()

    if alg not in SUPPORTED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}")

    try:
        # Some algorithms may not be available on all platforms
        hasher = hashlib.new(alg)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not available on this system.") from exc

    hasher.update(data)
    return hasher.digest()