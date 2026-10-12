import hashlib

# A set of algorithms that are considered insecure for password hashing.
INSECURE_ALGORITHMS = {
    "md5",
    "md5-sha1",
    "sha1",
}

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system or if it is
        considered insecure for password hashing.
    """
    # Normalise algorithm name to lowercase (hashlib expects case‑insensitive names)
    algo_name = algo_name.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Reject algorithms that are known to be insecure for password hashing
    if algo_name in INSECURE_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{algo_name}' is considered insecure for password hashing.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode("utf-8"))

    # Return the digest as bytes
    return hasher.digest()