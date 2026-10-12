import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of *data* using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm.  Must be one of the algorithms supported by
        :mod:`hashlib`.  The name is case‑sensitive and should match the names
        returned by :func:`hashlib.algorithms_available`.
    data : bytes
        Data to hash.

    Returns
    -------
    bytes
        The binary digest of the data.

    Raises
    ------
    ValueError
        If *hash_name* is not a supported algorithm.
    """
    # Validate the algorithm name
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_name!r}")

    # Create the hash object and feed it the data
    hasher = hashlib.new(hash_name)
    hasher.update(data)

    # Return the binary digest
    return hasher.digest()