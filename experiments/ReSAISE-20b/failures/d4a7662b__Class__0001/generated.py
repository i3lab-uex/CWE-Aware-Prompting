import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the
    specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hashlib algorithm (e.g. 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python
        environment.
    """
    # Normalise the algorithm name (hashlib is case‑insensitive)
    algo = hash_algorithm.lower()

    # Verify that the algorithm exists
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm!r}")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password to bytes (UTF‑8 is standard for passwords)
    pwd_bytes = pwd.encode("utf-8")

    # Update the hash object and return the digest
    hasher.update(pwd_bytes)
    return hasher.digest()