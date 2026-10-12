import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'sha512_256').
    pwd : str
        Password string to be hashed.

    Returns
    -------
    bytes
        The resulting hash digest as raw bytes.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported on this system.
    """
    # Ensure algorithm name is case‑insensitive
    algo_name = algo_name.lower()

    # Verify that the algorithm exists in hashlib's available algorithms
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and feed it the password encoded as UTF‑8
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()