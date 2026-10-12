import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use. Must be supported by hashlib.
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The digest of the hash operation.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Ensure the algorithm name is case‑insensitive and strip whitespace
    alg = hash_name.strip().lower()

    # Check if the algorithm is available in hashlib.algorithms_available
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Compute the hash
    try:
        hasher = hashlib.new(alg)
    except Exception as exc:  # pragma: no cover
        # In the unlikely event hashlib.new fails for a known algorithm,
        # raise a clear error message.
        raise ValueError(f"Failed to create hash object for '{hash_name}': {exc}") from exc

    hasher.update(data)
    return hasher.digest()