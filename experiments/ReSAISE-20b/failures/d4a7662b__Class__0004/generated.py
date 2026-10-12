import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hash algorithm (e.g. 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the current Python
        installation or if it is not considered secure (e.g. MD5, SHA‑1).
    """
    # Normalise the algorithm name
    algo = hash_algorithm.lower()

    # Ensure the algorithm is available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported on this system.")

    # Reject known weak algorithms
    weak_algos = {"md5", "sha1"}
    if algo in weak_algos:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is considered insecure and cannot be used.")

    # Create a new hash object and update it with the password bytes
    h = hashlib.new(algo)
    h.update(pwd.encode("utf-8"))

    # Return the digest as bytes
    return h.digest()