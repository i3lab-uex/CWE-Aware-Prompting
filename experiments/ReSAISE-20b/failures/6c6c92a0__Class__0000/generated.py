import hashlib

# A small set of algorithms that are generally considered insecure for password hashing.
INSECURE_ALGORITHMS = {
    "md5",
    "md5-sha1",
    "sha1",
}

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    pwd : str
        Plain‑text password to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by this Python installation,
        or if it is in the list of known insecure algorithms.
    """
    # Normalise algorithm name
    algo = algo_name.lower()

    # Check if the algorithm is available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Reject algorithms that are considered weak for password hashing
    if algo in INSECURE_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{algo_name}' is insecure and not allowed.")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password as UTF‑8 before hashing
    hasher.update(pwd.encode("utf-8"))

    # Return the raw digest bytes
    return hasher.digest()