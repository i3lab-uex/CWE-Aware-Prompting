import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes a password using the specified algorithm.

    Args:
        hash_name (str): The name of the hash algorithm to use.
        password (str): The plaintext password.

    Returns:
        bytes: The hash digest of the password.

    Raises:
        ValueError: If the requested algorithm is not supported by hashlib.
    """
    # Ensure we have a bytes representation of the password
    pwd_bytes = password.encode('utf-8')

    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Update the hash object with the password and return the digest
    hasher.update(pwd_bytes)
    return hasher.digest()