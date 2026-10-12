import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters:
        hash_algorithm (str): Name of the hash function to use.
        plain_text_pwd (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the specified algorithm is not supported or unavailable.
    """
    try:
        # hashlib.new will raise a ValueError if the algorithm is not known
        hash_obj = hashlib.new(hash_algorithm)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'"
        ) from exc

    # Encode the password to bytes (UTF-8 is a common choice)
    hash_obj.update(plain_text_pwd.encode("utf-8"))
    return hash_obj.hexdigest()