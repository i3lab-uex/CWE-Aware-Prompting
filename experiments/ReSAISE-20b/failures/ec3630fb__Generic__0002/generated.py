import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `hash_type` is not supported by the underlying hashlib implementation.
    """
    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        # Provide a clear error message
        raise ValueError(
            f"Hash algorithm '{hash_type}' is not supported. "
            "Supported algorithms include: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        ) from exc

    # Encode the secret to bytes (UTF-8 is a common safe choice)
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()