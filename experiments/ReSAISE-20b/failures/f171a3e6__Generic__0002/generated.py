import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hashes a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g. 'sha256', 'blake2b').
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
    # Ensure we have a string password; encode to UTF-8 for hashing
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    try:
        # Create a new hash object
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{hash_name}' is not available") from exc

    # Update the hash with the password bytes
    hasher.update(password.encode("utf-8"))

    # Return the raw digest bytes
    return hasher.digest()