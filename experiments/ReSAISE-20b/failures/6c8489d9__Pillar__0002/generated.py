import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes the given password using the specified hash algorithm and returns
    the hexadecimal digest.

    Args:
        hash_name: Name of a supported hashlib algorithm.
        password: The plaintext password to hash.

    Returns:
        A hex string representing the hash of the password.

    Raises:
        ValueError: If the requested algorithm is not supported by hashlib.
    """
    if not isinstance(hash_name, str) or not hash_name:
        raise ValueError("hash_name must be a non‑empty string")

    if not isinstance(password, str):
        raise ValueError("password must be a string")

    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Provide a clear error message for unsupported algorithms
        raise ValueError(f"Hash algorithm '{hash_name}' is not available") from exc

    # Encode the password as UTF‑8 before hashing
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()