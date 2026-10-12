import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm and returns
    its hexadecimal representation.

    Parameters:
        hash_algo (str): Name of the hash algorithm to use.
        pwd (str): Plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the algorithm is unsupported or unavailable.
        TypeError: If `pwd` is not a string.
    """
    if not isinstance(pwd, str):
        raise TypeError("Password must be a string")

    # Verify that the algorithm is available
    try:
        hasher = hashlib.new(hash_algo)
    except (ValueError, TypeError) as exc:
        # ValueError: unknown algorithm
        # TypeError: algorithm name not a string or None
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_algo}") from exc

    # Encode the password to bytes (UTF-8) before hashing
    hasher.update(pwd.encode('utf-8'))
    return hasher.hexdigest()