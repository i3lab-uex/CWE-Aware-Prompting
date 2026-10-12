import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm (e.g. 'sha256', 'blake2b', etc.).
    pass_key : bytes
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    TypeError
        If `pass_key` is not of type `bytes`.
    """
    if not isinstance(pass_key, bytes):
        raise TypeError("pass_key must be of type 'bytes'")

    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # Provide a clear error message with supported algorithms
        supported = ', '.join(sorted(hashlib.algorithms_available))
        raise ValueError(
            f"Unsupported hash algorithm '{algo_name}'. "
            f"Supported algorithms: {supported}"
        ) from exc

    hasher.update(pass_key)
    return hasher.digest()