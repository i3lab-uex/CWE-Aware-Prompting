import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    secret : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or unsupported.
    """
    # Ensure we are using a supported, available algorithm
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{algo_name}'")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()