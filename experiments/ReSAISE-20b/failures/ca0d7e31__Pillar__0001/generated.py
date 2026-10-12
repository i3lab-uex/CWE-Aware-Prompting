import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use.
    data : bytes
        Data to be hashed.

    Returns
    -------
    bytes
        The digest of the data.

    Raises
    ------
    ValueError
        If `hash_name` is not a supported algorithm in the current Python
        installation.
    """
    # Normalise the hash name (hashlib is case‑insensitive)
    algorithm = hash_name.lower()

    # Verify that the algorithm exists in the current environment
    if algorithm not in hashlib.algorithms_available:
        available = sorted(hashlib.algorithms_available)
        raise ValueError(
            f"Unsupported hash algorithm '{hash_name}'. "
            f"Available algorithms: {', '.join(available)}"
        )

    # Create a new hash object and update it with the data
    hasher = hashlib.new(algorithm)
    hasher.update(data)

    # Return the raw digest bytes
    return hasher.digest()