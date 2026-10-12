import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Compute the cryptographic hash of a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g. 'sha256', 'blake2b', etc.).
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest of the hash.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure password is encoded consistently
    pwd_bytes = password.encode('utf-8')

    try:
        # Create a new hash object; this will raise ValueError if unsupported
        hasher = hashlib.new(hash_name)
    except (ValueError, TypeError):
        # Provide a clear error message for the caller
        raise ValueError(f"Hash algorithm '{hash_name}' is not available or unsupported.") from None

    hasher.update(pwd_bytes)
    return hasher.digest()