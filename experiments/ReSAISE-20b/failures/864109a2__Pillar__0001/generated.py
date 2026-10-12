import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    plain_text_pwd : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal string of the hash digest.

    Raises
    ------
    ValueError
        If the supplied algorithm is not supported or unavailable.
    """
    # Normalise algorithm name (hashlib expects lowercase)
    alg = hash_algorithm.lower()

    # Verify that the algorithm is available in this Python build
    if alg not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Please choose from the supported algorithms."
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(alg)
    # Encode the plaintext to UTF-8 before hashing
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()