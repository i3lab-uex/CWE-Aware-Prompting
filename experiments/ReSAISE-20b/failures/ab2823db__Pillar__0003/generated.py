import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    secret : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalise algorithm name to lower case for consistency
    algo_name = algo_name.lower()

    # Check if the algorithm is supported by this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'. "
            "Supported algorithms include: "
            f"{sorted(hashlib.algorithms_available)}"
        )

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()