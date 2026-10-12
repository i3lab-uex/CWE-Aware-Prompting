import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes the given password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use.
    password : str
        The plaintext password.

    Returns
    -------
    bytes
        The hash digest of the password.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Validate that the hash name is available
    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(
            f"Hash algorithm '{hash_name}' is not available in this Python "
            "installation."
        ) from exc

    # Encode the password to bytes and update the hasher
    hasher.update(password.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()