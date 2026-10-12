import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes the given password using the specified hash algorithm.

    Args:
        hash_name: The name of the hash algorithm to use.
        password:  The plaintext password.

    Returns:
        The hexadecimal representation of the hash value.

    Raises:
        ValueError: If the requested algorithm is not available.
    """
    # Normalize the algorithm name to match hashlib's expectations
    hash_name = hash_name.lower()

    # Verify that the algorithm is supported by this Python installation
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(hash_name)
    hasher.update(password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()