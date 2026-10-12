import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm (e.g., 'sha256').
    pass_key : str
        The password to be hashed.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on the current system.
    """
    # Normalize algorithm name to lowercase for consistency
    algo_name = algorithm.lower()

    # Verify that the requested algorithm is available on this platform.
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Convert the password to bytes using UTF-8 encoding.
    data = pass_key.encode('utf-8')

    # Create a new hash object and update it with the data.
    hasher = hashlib.new(algo_name)
    hasher.update(data)

    # Return the digest as bytes.
    return hasher.digest()