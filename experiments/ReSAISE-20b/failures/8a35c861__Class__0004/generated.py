import hashlib

# List of cryptographic hash algorithms considered secure for password hashing.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_224",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using a
    secure algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use. Must be one of the
        algorithms listed in SECURE_ALGORITHMS.
    pw : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If `algo_name` is not in SECURE_ALGORITHMS or the algorithm
        is not available in the current Python runtime.
    """
    algo_name_lower = algo_name.lower()

    # Ensure the algorithm is in our secure list
    if algo_name_lower not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_name}' is not considered secure for password hashing."
        )

    # Verify the algorithm is available in this environment
    if algo_name_lower not in hashlib.algorithms_available:
        raise ValueError(
            f"Algorithm '{algo_name}' is not available in this Python runtime."
        )

    # Compute the hash
    hasher = hashlib.new(algo_name_lower)
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()