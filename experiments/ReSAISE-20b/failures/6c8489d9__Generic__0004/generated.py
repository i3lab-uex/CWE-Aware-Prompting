import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes the given password using the specified hash algorithm and returns
    the hexadecimal digest.

    Parameters:
        hash_name (str): Name of the hash algorithm to use.
        password (str): Password string to be hashed.

    Returns:
        str: Hexadecimal hash value of the password.

    Raises:
        ValueError: If the specified hash algorithm is not supported.
    """
    # Ensure the password is encoded to bytes
    pwd_bytes = password.encode('utf-8')

    try:
        # Create a new hash object for the specified algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported.") from exc

    # Update the hash object with the password bytes and return hex digest
    hasher.update(pwd_bytes)
    return hasher.hexdigest()