import hashlib

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    hash_type : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    pass_input : str
        The password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If ``hash_type`` is not a supported hash algorithm.
    """
    # Ensure the input password is encoded to bytes
    password_bytes = pass_input.encode('utf-8')

    try:
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        # Provide a clear error message indicating the unsupported algorithm
        raise ValueError(f"Unsupported hash type '{hash_type}'. "
                         f"Supported algorithms: {', '.join(hashlib.algorithms_available)}") from exc

    hasher.update(password_bytes)
    return hasher.hexdigest()