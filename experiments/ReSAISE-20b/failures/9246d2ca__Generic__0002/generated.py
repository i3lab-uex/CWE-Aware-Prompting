import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    pass_key : bytes
        The password to be hashed.

    Returns
    -------
    bytes
        The binary digest produced by the hash algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Ensure we have a supported algorithm name
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and update it with the password
    h = hashlib.new(algo_name)
    h.update(pass_key)

    # Return the digest as bytes
    return h.digest()