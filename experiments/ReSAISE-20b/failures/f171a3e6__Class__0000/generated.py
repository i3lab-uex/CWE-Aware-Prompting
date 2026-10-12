import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2s', etc.).
    password : str
        Plain‑text password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Ensure the password is encoded to bytes; use UTF‑8 which is a common default.
    pwd_bytes = password.encode('utf-8')

    # Verify that the requested algorithm is supported by hashlib.
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and update it with the password.
    hasher = hashlib.new(hash_name)
    hasher.update(pwd_bytes)

    # Return the digest as bytes.
    return hasher.digest()