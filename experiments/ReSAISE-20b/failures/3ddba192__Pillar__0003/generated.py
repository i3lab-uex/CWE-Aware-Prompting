import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hash a password using the specified hash algorithm and return the hexadecimal digest.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    passcode : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the algorithm name matches a callable in hashlib
    try:
        hash_func = getattr(hashlib, hash_algo)
    except AttributeError:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available in hashlib.") from None

    # Compute the hash
    digest = hash_func(passcode.encode('utf-8')).hexdigest()
    return digest