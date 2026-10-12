import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hash a password using the specified hash algorithm and return
    the result as a hexadecimal string.

    Parameters:
        hash_type (str): Name of the hash function to use.
        secret (str): Password string to be hashed.

    Returns:
        str: Hexadecimal representation of the hash digest.

    Raises:
        ValueError: If the requested hash algorithm is not available.
    """
    # Ensure secret is encoded to bytes (UTF-8 by default)
    data = secret.encode('utf-8')

    try:
        # hashlib.new will raise a ValueError if the algorithm is unknown
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_type}' is not supported.") from exc

    hasher.update(data)
    return hasher.hexdigest()