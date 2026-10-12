import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes a password using the specified algorithm and returns the hex digest.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use. Must be one of the names
        supported by :mod:`hashlib`.  The check is case‑sensitive.
    key : bytes
        The password (or any byte sequence) to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hash value.

    Raises
    ------
    ValueError
        If *algo_name* is not a supported hash algorithm.
    """
    # Ensure the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported.")

    # Compute the hash
    hasher = hashlib.new(algo_name)
    hasher.update(key)
    return hasher.hexdigest()