import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (case‑insensitive).
    data : bytes
        Data to be hashed.

    Returns
    -------
    bytes
        The raw hash digest of the data.

    Raises
    ------
    ValueError
        If `hash_name` is not supported by the underlying hashlib implementation.
    """
    # Normalise algorithm name to lower case for consistency
    alg = hash_name.lower()

    # Verify that the requested algorithm is available
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Compute the digest
    try:
        hasher = hashlib.new(alg)
        hasher.update(data)
        return hasher.digest()
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError to avoid leaking internal details
        raise ValueError(f"Failed to compute hash with algorithm '{hash_name}': {exc}") from exc