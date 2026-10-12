import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hash a password using the specified algorithm and return the hexadecimal digest.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of the algorithms
        supported by :mod:`hashlib`.
    key : bytes
        The password (or any binary data) to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If ``algo_name`` is not a supported hash algorithm.
    """
    # Validate that the requested algorithm exists
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name!r}")

    # Create a new hash object
    try:
        hasher = hashlib.new(algo_name)
    except Exception as exc:   # pragma: no cover
        raise ValueError(f"Failed to create hash object for {algo_name!r}") from exc

    # Update the hasher with the key
    hasher.update(key)

    # For shake algorithms we need to specify a digest size; default to 64 bytes
    if algo_name.startswith("shake"):
        return hasher.hexdigest(64)
    else:
        return hasher.hexdigest()