import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    plain_text_pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_algorithm`` is not supported by the current Python
        installation or if it is unavailable on the system.
    """
    # Normalise algorithm name to lowercase for consistency
    algo = hash_algorithm.lower()

    try:
        # hashlib.new will raise a ValueError if the algorithm is unknown
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # Provide a clear error message
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Please choose from the supported algorithms."
        ) from exc

    # Encode password to bytes and update the hasher
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()