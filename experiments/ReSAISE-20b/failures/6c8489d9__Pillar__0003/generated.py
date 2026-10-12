import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its
    hexadecimal digest.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure that the algorithm name is valid and available
    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported.") from exc

    # Encode the password to bytes and update the hasher
    hasher.update(password.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()