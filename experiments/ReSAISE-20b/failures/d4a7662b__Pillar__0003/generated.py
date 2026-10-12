import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hashlib algorithm (e.g. 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If `hash_algorithm` is not available on the current system.
    """
    # Normalize algorithm name (case‑insensitive)
    algo_name = hash_algorithm.lower()

    # Check if the requested algorithm is supported
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm!r}")

    # Create a new hash object
    hasher = hashlib.new(algo_name)

    # Encode the password to bytes and feed it into the hasher
    hasher.update(pwd.encode("utf-8"))

    # Return the digest as bytes
    return hasher.digest()