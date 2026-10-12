import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    plain_text_pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lower case for consistency
    algo = hash_algorithm.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Supported algorithms include: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(algo)
    # Encode plaintext using UTF-8; adjust encoding if needed
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()