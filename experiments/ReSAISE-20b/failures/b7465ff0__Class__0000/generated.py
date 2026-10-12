import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes the given password using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    key : bytes
        The password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalize algorithm name to match hashlib's case sensitivity
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Create the hash object and update it with the key
    hasher = hashlib.new(algo_name)
    hasher.update(key)

    # Return the hexadecimal digest
    return hasher.hexdigest()