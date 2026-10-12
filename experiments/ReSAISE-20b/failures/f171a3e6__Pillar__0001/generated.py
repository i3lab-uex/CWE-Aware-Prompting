import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the hash name is a valid, built‑in algorithm
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create the hash object
    hasher = hashlib.new(hash_name)

    # Encode password to bytes (UTF‑8 is standard for text)
    hasher.update(password.encode("utf-8"))

    # Return the digest as bytes
    return hasher.digest()