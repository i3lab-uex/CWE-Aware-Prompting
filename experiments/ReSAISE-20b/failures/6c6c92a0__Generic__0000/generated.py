import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of a hash algorithm supported by the current Python installation.
        Examples: 'sha256', 'blake2b', etc.

    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If `algo_name` is not supported by the underlying hashlib implementation.
    """
    # Ensure the algorithm name is lower‑case to match hashlib's naming
    algo_name = algo_name.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name!r}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as raw bytes
    return hasher.digest()