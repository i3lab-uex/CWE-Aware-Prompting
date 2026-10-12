import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2b', etc.).
    user_pass : bytes
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hash function.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalise the algorithm name to lower case for consistency
    alg = algorithm_name.lower()

    # Retrieve the set of algorithms guaranteed to be available.
    # If an environment lacks a particular algorithm, it will not appear here,
    # which helps avoid attempting to use an unsupported or broken one.
    available = hashlib.algorithms_guaranteed

    if alg not in available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create a new hash object and compute the digest
    hasher = hashlib.new(alg)
    hasher.update(user_pass)
    return hasher.digest()