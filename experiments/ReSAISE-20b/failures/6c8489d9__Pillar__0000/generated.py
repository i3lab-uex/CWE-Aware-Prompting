import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal digest.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'md5').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hash value.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the chosen algorithm exists
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Encode the password as UTF‑8 bytes (consistent, secure encoding)
    pwd_bytes = password.encode('utf-8')

    # Compute the hash
    hasher = hashlib.new(hash_name.lower())
    hasher.update(pwd_bytes)
    return hasher.hexdigest()