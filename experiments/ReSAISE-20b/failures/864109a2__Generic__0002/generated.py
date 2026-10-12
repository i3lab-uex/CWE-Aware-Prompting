import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    plain_text_pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_algorithm)
    except ValueError as exc:
        # The algorithm is not available in the current OpenSSL/cryptography
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Please choose from the supported algorithms."
        ) from exc

    # Encode the plaintext password to bytes (UTF-8 is a common choice)
    pwd_bytes = plain_text_pwd.encode("utf-8")
    hasher.update(pwd_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()