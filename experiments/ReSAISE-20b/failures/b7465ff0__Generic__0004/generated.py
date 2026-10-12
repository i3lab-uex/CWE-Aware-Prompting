import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    key : bytes
        The password to hash. Must be in bytes.

    Returns
    -------
    str
        The hexadecimal digest of the hash.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    if not isinstance(key, bytes):
        raise TypeError("Password key must be of type 'bytes'.")

    try:
        hash_obj = hashlib.new(algo_name, key)
    except ValueError as exc:
        # Provide a clear message about unsupported algorithms
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.") from exc

    return hash_obj.hexdigest()