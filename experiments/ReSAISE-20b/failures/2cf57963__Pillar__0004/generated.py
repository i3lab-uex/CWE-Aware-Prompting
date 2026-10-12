import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of a hash algorithm supported by the current Python runtime.
        Examples: 'sha256', 'sha512', 'blake2b', etc.

    pass_key : str
        The password or secret to hash.

    Returns
    -------
    bytes
        Raw digest of the hashed value.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Normalise algorithm name to lowercase as hashlib expects
    alg_name = algorithm.lower()

    # Check if the algorithm is available in the current environment
    if alg_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Hash algorithm '{algorithm}' is not supported on this system."
        )

    # Create a new hash object
    try:
        hasher = hashlib.new(alg_name)
    except Exception as exc:  # pragma: no cover
        raise ValueError(
            f"Failed to create hash object for algorithm '{algorithm}': {exc}"
        ) from exc

    # Encode the password to bytes (UTF‑8 is a standard, non‑ambiguous choice)
    data = pass_key.encode("utf-8")
    hasher.update(data)

    # Return the raw digest bytes
    return hasher.digest()