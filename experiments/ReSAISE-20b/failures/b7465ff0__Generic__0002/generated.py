import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b', etc.).
    key : bytes
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available.
    """
    # Ensure that the algorithm name is supported
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Create a new hash object and update it with the key
    hasher = hashlib.new(algo_name.lower())
    hasher.update(key)

    # Return the digest as a hexadecimal string
    return hasher.hexdigest()