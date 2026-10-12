import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use.
    secret : str
        The plaintext password.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is available
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algo_name}")

    # Create a new hash object and update it with the secret bytes
    hasher = hashlib.new(algo_name.lower())
    hasher.update(secret.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()