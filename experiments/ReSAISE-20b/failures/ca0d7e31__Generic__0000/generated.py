import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of ``data`` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'md5', etc.).
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The raw digest of the hash.

    Raises
    ------
    ValueError
        If ``hash_name`` is not a supported algorithm.
    """
    # Normalise the hash name to lower case (hashlib accepts both).
    algorithm = hash_name.lower()

    # Verify that the requested algorithm is available.
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and update it with the data.
    try:
        h = hashlib.new(algorithm)
    except (TypeError, ValueError) as exc:
        # In case the algorithm name is malformed or unsupported.
        raise ValueError(f"Failed to create hash object for '{hash_name}': {exc}") from exc

    h.update(data)
    return h.digest()