import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (must be supported by hashlib).
    key : bytes
        The password or data to hash.

    Returns
    -------
    str
        Hexadecimal representation of the computed hash.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalize the algorithm name to lower case for consistency
    algo_name = algo_name.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Create a new hash object and update it with the key
    hasher = hashlib.new(algo_name)
    hasher.update(key)

    return hasher.hexdigest()