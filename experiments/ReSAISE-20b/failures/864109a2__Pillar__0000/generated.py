import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters:
        hash_algorithm (str): Name of the hash algorithm to use.
        plain_text_pwd (str): The plaintext password.

    Returns:
        str: Hexadecimal string of the hashed password.

    Raises:
        ValueError: If the provided algorithm is not supported or unavailable.
    """
    # Validate that the algorithm exists in hashlib
    if hash_algorithm not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Available algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(hash_algorithm)
    # Encode plaintext to UTF-8 before hashing
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()