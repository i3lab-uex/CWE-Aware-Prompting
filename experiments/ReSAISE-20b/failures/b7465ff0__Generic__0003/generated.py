import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes the given password using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash function to use (e.g. 'sha256', 'blake2b').
    key : bytes
        The password to hash. It should be provided as a byte string.

    Returns
    -------
    str
        The hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.") from exc

    hasher.update(key)
    return hasher.hexdigest()