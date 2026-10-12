import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'md5').
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalize the algorithm name to match hashlib's convention
    algo = hash_name.strip().lower()

    # Verify the algorithm is available in this Python environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and feed the UTF‑8 encoded password
    h = hashlib.new(algo)
    h.update(password.encode('utf-8'))

    # Return the digest as bytes
    return h.digest()