import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes a password using the specified algorithm and returns the hex digest.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (e.g. 'sha256', 'md5', etc.).
    key : bytes
        Password data to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported.") from exc

    hasher.update(key)
    return hasher.hexdigest()