import hashlib

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the algorithms supported by
        hashlib (case-sensitive).
    raw_password : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the underlying hashlib implementation.
    """
    # Ensure we are using a valid algorithm name
    if algorithm_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm: {algorithm_name!r}. "
            "Supported algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object using the requested algorithm
    try:
        hasher = hashlib.new(algorithm_name)
    except Exception as exc:  # pragma: no cover
        raise ValueError(
            f"Failed to create hash object for algorithm {algorithm_name!r}"
        ) from exc

    # Encode the raw password to bytes (UTF-8 is a common choice)
    password_bytes = raw_password.encode("utf-8")

    # Update the hash object and get the hexadecimal digest
    hasher.update(password_bytes)
    return hasher.hexdigest()