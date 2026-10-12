import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'blake2b', etc.).
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    try:
        # Create a new hash object for the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported.") from exc

    # Encode the password as UTF-8 and feed it into the hasher
    hasher.update(password.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()