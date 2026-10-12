import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'blake2b').
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in the current
        Python environment.
    """
    # Ensure the algorithm name is case‑insensitive and trimmed
    algo = hash_name.strip().lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(password.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()