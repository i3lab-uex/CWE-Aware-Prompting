import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm.

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
        If `algo_name` is not supported or unavailable in the current environment.
    """
    # Ensure algorithm name is lower‑case for consistency
    algo_name = algo_name.lower()

    try:
        hasher = hashlib.new(algo_name)
    except (ValueError, TypeError):
        # ValueError is raised by hashlib.new if the algorithm is unknown
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{algo_name}'")

    # Encode the password to bytes (UTF‑8 is a safe default)
    hasher.update(secret.encode('utf-8'))

    return hasher.hexdigest()