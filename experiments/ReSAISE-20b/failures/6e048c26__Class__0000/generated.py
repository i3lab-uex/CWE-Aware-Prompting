import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the cryptographic hash algorithm (e.g. 'sha512', 'blake2b').
    user_pass : bytes
        Password to hash.

    Returns
    -------
    bytes
        The computed digest of the password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not a supported algorithm.
    """
    # Ensure the algorithm name exists in hashlib's available algorithms
    if algorithm_name.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create a new hash object for the chosen algorithm
    hasher = hashlib.new(algorithm_name)

    # Feed the password into the hash function
    hasher.update(user_pass)

    # Return the raw digest bytes
    return hasher.digest()