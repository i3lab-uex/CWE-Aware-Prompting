import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hashlib algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the current Python runtime.
    """
    # Ensure algorithm name is case‑insensitive
    algo = hash_algorithm.lower()

    # Verify support for the algorithm
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password as UTF‑8 before hashing
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()