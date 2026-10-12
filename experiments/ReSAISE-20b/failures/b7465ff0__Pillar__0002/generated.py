import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hashes the given password using the specified hash algorithm and returns
    the hexadecimal representation of the digest.

    Parameters:
        algo_name (str): Name of the hash function to use.
        key (bytes): The password bytes to be hashed.

    Returns:
        str: Hexadecimal string of the hash digest.

    Raises:
        ValueError: If the requested algorithm is not available in hashlib.
    """
    # Check that the algorithm exists in hashlib
    try:
        hash_obj = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported.") from exc

    # Update the hash object with the key
    hash_obj.update(key)

    # Return the digest as a hexadecimal string
    return hash_obj.hexdigest()