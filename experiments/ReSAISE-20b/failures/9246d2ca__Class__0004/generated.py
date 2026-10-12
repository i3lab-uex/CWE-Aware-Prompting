import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pass_key : bytes
        The password to hash.

    Returns
    -------
    bytes
        The computed hash value.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Ensure that the requested algorithm is available
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and feed the password
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)

    # Return the digest as bytes
    return hasher.digest()