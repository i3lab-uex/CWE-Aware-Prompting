import hashlib

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of a hash algorithm supported by the hashlib module.
    user_password : bytes
        The password to be hashed.

    Returns
    -------
    bytes
        The digest of the hash function applied to ``user_password``.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Normalise the algorithm name to lower case (hashlib expects lower‑case names)
    algo = algorithm_name.lower()

    # Check if the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(user_password)

    # Return the digest as bytes
    return hasher.digest()