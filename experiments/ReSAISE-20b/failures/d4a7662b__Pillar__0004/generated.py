import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Normalize algorithm name to lower case
    algo = hash_algorithm.lower()

    # Verify that the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported on this system.")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password to bytes (UTF‑8 is a safe, Unicode‑compatible encoding)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()