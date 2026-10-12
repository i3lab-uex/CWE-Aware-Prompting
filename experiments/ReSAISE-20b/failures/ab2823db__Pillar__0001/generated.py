import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    secret : str
        Plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    try:
        # Create a new hash object using the requested algorithm
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # Provide a clear error message if the algorithm is not available
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algo_name}") from exc

    # Encode the secret as UTF-8 before hashing
    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()