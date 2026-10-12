import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'md5', etc.).
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed data.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    try:
        # `hashlib.new` raises a ValueError if the algorithm is unknown
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    hasher.update(data)
    return hasher.digest()