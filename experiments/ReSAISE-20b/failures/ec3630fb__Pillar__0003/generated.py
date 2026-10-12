import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    secret : str
        The password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available.
    """
    if not isinstance(hash_type, str):
        raise ValueError("hash_type must be a string")

    if not isinstance(secret, str):
        raise ValueError("secret must be a string")

    # Verify that the hash algorithm is supported
    try:
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            "Available algorithms are: "
            f"{', '.join(hashlib.algorithms_available)}"
        ) from exc

    # Encode the secret to bytes (UTF-8) before hashing
    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()