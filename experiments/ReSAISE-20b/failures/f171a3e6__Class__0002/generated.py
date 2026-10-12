import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    password : str
        Plain‑text password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm exists in hashlib
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object and update it with the password bytes
    h = hashlib.new(hash_name)
    # Encode the password using UTF-8; this is a common, safe choice for text input
    h.update(password.encode('utf-8'))

    # Return the raw digest bytes (not hex or base64)
    return h.digest()