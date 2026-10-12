import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes the provided password using the specified hash algorithm and returns
    its hexadecimal representation.

    Parameters:
        hash_name (str): The name of the hash algorithm to use.
                         Must be supported by hashlib.new().
        password (str): The plaintext password to hash.

    Returns:
        str: The hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the requested hash algorithm is not available.
    """
    # Ensure the algorithm name is valid and supported by hashlib
    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Encode the password to bytes (UTF-8) and update the hasher
    hasher.update(password.encode('utf-8'))

    # Return the hexadecimal digest of the hash
    return hasher.hexdigest()