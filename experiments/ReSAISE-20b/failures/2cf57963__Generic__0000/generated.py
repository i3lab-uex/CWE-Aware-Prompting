import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of a hash algorithm supported by hashlib (e.g. 'sha256', 'blake2b').
    pass_key : str
        Password string to be hashed.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported by the underlying hashlib implementation.
    """
    try:
        # Create a new hash object for the chosen algorithm
        hasher = hashlib.new(algorithm)
    except ValueError as exc:
        # hashlib raises a ValueError if the algorithm is unknown
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from exc

    # Encode the password as UTF-8 and update the hash object
    hasher.update(pass_key.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()