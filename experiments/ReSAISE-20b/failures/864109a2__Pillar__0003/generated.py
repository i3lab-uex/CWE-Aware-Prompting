import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hashes a plaintext password using the specified hash algorithm and returns
    its hexadecimal representation.

    Parameters:
        hash_algorithm (str): Name of the hash algorithm to use.
        plain_text_pwd (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the algorithm is unsupported or unavailable.
    """
    if not isinstance(hash_algorithm, str):
        raise ValueError("hash_algorithm must be a string")
    if not isinstance(plain_text_pwd, str):
        raise ValueError("plain_text_pwd must be a string")

    # Normalize algorithm name to lower case
    algo = hash_algorithm.lower()

    try:
        # hashlib.new accepts algorithm names from the set of available algorithms
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # Provide a clear error message
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_algorithm}") from exc

    # Encode the password to bytes (UTF-8 is a common, safe choice)
    pwd_bytes = plain_text_pwd.encode('utf-8')
    hasher.update(pwd_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()