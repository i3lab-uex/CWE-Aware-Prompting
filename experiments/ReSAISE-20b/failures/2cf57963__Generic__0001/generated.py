import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of a hash algorithm supported by the current Python installation.
        Examples: 'sha256', 'sha512_256', 'blake2b', etc.
    pass_key : str
        The password to be hashed.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available on this system.
    """
    # Normalize algorithm name to lowercase as hashlib uses lowercase names
    algo_name = algorithm.lower()

    # Ensure the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the hash object
    hasher = hashlib.new(algo_name)

    # Encode the password to bytes (UTF-8 is standard for text hashing)
    hasher.update(pass_key.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()