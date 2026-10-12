import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm and returns
    its hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'md5', etc.).
    plain_text_pwd : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Normalise algorithm name (case‑insensitive)
    algo_name = hash_algorithm.lower()

    # Ensure the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'")

    # Create a new hash object
    try:
        hasher = hashlib.new(algo_name)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Failed to create hash object for algorithm '{hash_algorithm}': {exc}") from exc

    # Encode the password as UTF‑8 and update the hasher
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()