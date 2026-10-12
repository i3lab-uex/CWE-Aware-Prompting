import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use.
    plain_text_pwd : str
        The plaintext password.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the provided algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lower case as hashlib expects
    algo_name = hash_algorithm.lower()

    # Verify that the algorithm is available in the current environment
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Supported algorithms include: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Encode the plaintext password to bytes (UTF-8 is a common choice)
    pwd_bytes = plain_text_pwd.encode('utf-8')

    # Create the hash object and compute the digest
    try:
        hasher = hashlib.new(algo_name)
    except (ValueError, TypeError) as exc:
        # This should not happen due to the earlier check but guard anyway
        raise ValueError(
            f"Failed to create hash object for algorithm '{hash_algorithm}': {exc}"
        ) from exc

    hasher.update(pwd_bytes)
    return hasher.hexdigest()