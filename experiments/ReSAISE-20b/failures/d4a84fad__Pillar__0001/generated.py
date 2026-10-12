import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Args:
        encryption_method (str): The name of the hash algorithm to use.
                                 Must be one of the algorithms supported by hashlib.
        user_password (str): The password to hash.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure we are using a supported algorithm
    try:
        hasher = hashlib.new(encryption_method)
    except ValueError as exc:
        # Provide a clear error message for unsupported algorithms
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: "
            f"{', '.join(hashlib.algorithms_available)}"
        ) from exc

    # Encode the password to bytes and update the hasher
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()