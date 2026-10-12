import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its hexadecimal digest.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5', etc.).
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
    # Ensure the requested algorithm is available
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(hash_name)
    hasher.update(password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()