import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes the provided password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash function to be used.
    key : bytes
        The password that has to be hashed.

    Returns
    -------
    str
        A hexadecimal string representing the hashed password.

    Raises
    ------
    ValueError
        If the provided hash function is not available in hashlib.
    """
    # Normalize algorithm name to lowercase as used by hashlib
    algo_name = algo_name.lower()

    # Ensure the requested algorithm is supported
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Create a new hash object and feed the key
    hasher = hashlib.new(algo_name)
    hasher.update(key)

    # Return the hexadecimal digest
    return hasher.hexdigest()