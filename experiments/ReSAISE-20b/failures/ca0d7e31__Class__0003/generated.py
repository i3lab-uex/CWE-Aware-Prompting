import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of ``data`` using the algorithm specified by
    ``hash_name``.

    Parameters
    ----------
    hash_name : str
        Name of the desired hash algorithm (e.g. 'sha256', 'md5').
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If ``hash_name`` is not a supported algorithm.
    """
    # Normalise the name to lower case as hashlib expects
    algo = hash_name.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    try:
        h = hashlib.new(algo)
    except (TypeError, ValueError) as exc:
        # This should not happen if the algorithm is in algorithms_available,
        # but we guard against it anyway.
        raise ValueError(f"Failed to create hash object for '{hash_name}': {exc}") from exc

    h.update(data)

    # For SHAKE algorithms we need to specify a digest size.
    if algo.startswith("shake"):
        # Default to 64 bytes (512 bits) which is a common choice.
        return h.digest(64)
    else:
        return h.digest()