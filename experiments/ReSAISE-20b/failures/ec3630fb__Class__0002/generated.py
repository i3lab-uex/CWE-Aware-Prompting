import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        The name of a hash function supported by hashlib.
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `hash_type` is not supported by hashlib.
    """
    # Ensure the requested algorithm exists
    try:
        hash_obj = hashlib.new(hash_type)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash type '{hash_type}'. "
                         f"Available algorithms: {', '.join(hashlib.algorithms_available)}") from exc

    # Encode the secret to bytes and update the hash object
    hash_obj.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hash_obj.hexdigest()