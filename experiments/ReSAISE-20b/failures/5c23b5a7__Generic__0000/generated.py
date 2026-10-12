import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha512', 'blake2b', etc.).
    user_password : bytes
        The password to hash. Must be provided as a byte string.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python
        installation.
    """
    # Ensure the algorithm name is valid. hashlib.new will raise a ValueError
    # if the algorithm is unknown.
    try:
        hash_obj = hashlib.new(algorithm_name)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported hash algorithm: {algorithm_name!r}. "
            "Supported algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        ) from exc

    # Feed the password into the hash object and return the digest.
    hash_obj.update(user_password)
    return hash_obj.digest()