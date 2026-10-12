import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to apply.
    secret : str
        Plain‑text password.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If an unsupported or unavailable hash algorithm is provided.
    """
    # Normalise the algorithm name to match hashlib's expectations
    algo_name = algo_name.lower()

    # Verify that the requested algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'. "
            "Check hashlib.algorithms_available for supported names."
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(secret.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()