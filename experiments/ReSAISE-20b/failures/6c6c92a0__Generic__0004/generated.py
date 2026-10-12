import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python environment.
    """
    # Ensure algorithm name is case‑insensitive
    algo = algo_name.lower()

    # Verify that the algorithm is available on this system.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and update it with the password bytes.
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes.
    return hasher.digest()