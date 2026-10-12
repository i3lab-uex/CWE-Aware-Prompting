import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes the provided password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use.
    password : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        The hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Provide a clear error message for unsupported algorithms
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Encode the password to bytes (UTF‑8) before hashing
    hasher.update(password.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()