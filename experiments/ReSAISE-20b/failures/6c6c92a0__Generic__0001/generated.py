import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b', etc.).
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on the current system.
    """
    # Ensure the algorithm name is case‑insensitive
    algo_name = algo_name.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Create a new hash object with the requested algorithm
    hasher = hashlib.new(algo_name)

    # Encode the password to bytes (UTF‑8 is a safe default)
    hasher.update(pwd.encode('utf-8'))

    # Return the binary digest
    return hasher.digest()