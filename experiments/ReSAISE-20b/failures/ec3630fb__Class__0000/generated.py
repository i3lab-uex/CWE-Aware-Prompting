import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Compute a cryptographic hash of the supplied password using the
    specified algorithm and return the result as a hexadecimal string.

    Parameters
    ----------
    hash_type : str
        Name of the hash algorithm to use. Must be one of the algorithms
        supported by :mod:`hashlib`.  Case-insensitive.
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the computed hash.

    Raises
    ------
    ValueError
        If *hash_type* is not supported by :mod:`hashlib`.
    """
    # Normalise the hash name to lower case for consistency
    algo_name = hash_type.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_type!r}")

    # Create the hasher and feed it the secret as bytes
    hasher = hashlib.new(algo_name)
    hasher.update(secret.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()