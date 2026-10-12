import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm and return its
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
        If the provided algorithm is not supported or unavailable.
    """
    try:
        # Create a new hash object for the requested algorithm
        hasher = hashlib.new(hash_algorithm)
    except ValueError as exc:
        # Raise a more descriptive error
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Choose from the algorithms supported by hashlib."
        ) from exc

    # Encode the plaintext password to bytes (UTF-8 is standard)
    pwd_bytes = plain_text_pwd.encode("utf-8")

    # Update the hash object with the password bytes
    hasher.update(pwd_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()