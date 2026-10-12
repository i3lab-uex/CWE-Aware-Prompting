import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'blake2b', etc.).
    password : str
        The plain‑text password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    try:
        # Create the hash object for the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not available") from exc

    # Encode the password as UTF‑8 before hashing
    hasher.update(password.encode("utf-8"))
    return hasher.digest()