import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes the given password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g. 'sha256', 'md5').
    password : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the password is encoded as UTF‑8 bytes
    pwd_bytes = password.encode("utf-8")

    try:
        # Create a new hash object using the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Raise a more informative error
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Update the hash with the password bytes and return the digest
    hasher.update(pwd_bytes)
    return hasher.digest()