import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to apply (e.g., 'sha256', 'md5').
    secret : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Normalise the algorithm name to lowercase for consistency
    algo_name = algo_name.lower()

    # Check if the algorithm is available in the current environment
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'. "
            "Supported algorithms include: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and update it with the secret encoded as UTF-8
    hasher = hashlib.new(algo_name)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()