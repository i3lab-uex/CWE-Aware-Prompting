import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hashes a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g. 'sha256', 'md5').
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `hash_type` is not supported by the hashlib module.
    """
    # Normalise algorithm name to lower case for comparison
    algo_name = hash_type.lower()

    # Verify that the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_type}' is not available.")

    # Create a new hash object and feed the secret bytes
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # This should not happen due to the previous check, but guard anyway
        raise ValueError(f"Hash algorithm '{hash_type}' could not be initialized.") from exc

    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()