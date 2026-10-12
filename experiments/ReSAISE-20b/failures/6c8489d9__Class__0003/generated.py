import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'blake2b').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the computed hash value.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure the algorithm exists in the current Python environment
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available in this environment.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(hash_name)
    hasher.update(password.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()