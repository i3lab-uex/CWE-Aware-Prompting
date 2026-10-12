import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_type : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash function is not supported.
    """
    # Ensure the algorithm exists in hashlib
    try:
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported hash type '{hash_type}'. "
            "Supported types: "
            + ", ".join(hashlib.algorithms_available)
        ) from exc

    # Encode the secret to bytes; UTF-8 is a common safe choice
    hasher.update(secret.encode('utf-8'))

    return hasher.hexdigest()