import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5', etc.).
    pwd : str
        Plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Ensure algorithm name is case-insensitive
    algo_name = hash_algo.lower()

    # Check if the algorithm exists in hashlib's available algorithms
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algo}'")

    # Create a new hash object
    try:
        hasher = hashlib.new(algo_name)
    except Exception as exc:
        raise ValueError(f"Failed to create hash object for algorithm '{hash_algo}': {exc}") from exc

    # Encode the password to bytes (UTF-8) and update the hash
    hasher.update(pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()