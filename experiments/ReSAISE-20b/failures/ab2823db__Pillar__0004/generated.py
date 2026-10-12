import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    secret : str
        Plaintext password.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `algo_name` is not supported or unavailable in the current environment.
    """
    # Normalize algorithm name to lowercase as hashlib expects
    algo_name = algo_name.lower()

    # Verify the algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'. "
            "Available algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and feed it the password bytes
    try:
        hasher = hashlib.new(algo_name)
    except Exception as exc:  # pragma: no cover
        # This block should never be hit because we already checked availability,
        # but it guards against unexpected failures.
        raise ValueError(
            f"Failed to initialize hash algorithm '{algo_name}': {exc}"
        ) from exc

    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()