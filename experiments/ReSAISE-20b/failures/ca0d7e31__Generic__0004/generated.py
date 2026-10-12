import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g. 'sha256', 'md5', etc.).
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The digest of the data.

    Raises
    ------
    ValueError
        If `hash_name` is not a supported algorithm.
    """
    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not available") from exc

    # Update the hasher with the data and return the digest
    hasher.update(data)
    return hasher.digest()