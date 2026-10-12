import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    secret : str
        Plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Verify that the algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{algo_name}'")

    # Create a new hash object and update it with the secret bytes
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        # This should not happen because we checked algorithms_available,
        # but guard against race conditions or environment changes.
        raise ValueError(f"Failed to initialize hash algorithm '{algo_name}': {exc}") from exc

    # Encode the secret as UTF-8 bytes before hashing
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest string
    return hasher.hexdigest()