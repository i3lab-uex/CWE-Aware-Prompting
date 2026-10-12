import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hash a password using the specified algorithm and return the hexadecimal digest.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b', etc.).
    key : bytes
        The password or secret to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure algorithm name is in a case‑insensitive set of available algorithms
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Create a new hash object with the provided key
    hasher = hashlib.new(algo_name, key)
    return hasher.hexdigest()