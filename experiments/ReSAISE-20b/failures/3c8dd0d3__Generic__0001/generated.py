import hashlib

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    pwd : str
        Plain‑text password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the current Python build.
    """
    # Normalise the algorithm name to lower case
    algo = algorithm_name.lower()

    # Check that the requested algorithm is available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create the hash object and feed it the password bytes
    hasher = hashlib.new(algo, pwd.encode("utf-8"))
    return hasher.digest()