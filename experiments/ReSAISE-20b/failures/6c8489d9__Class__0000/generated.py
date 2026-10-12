import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (case‑sensitive, as accepted by hashlib).
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python environment.
    """
    try:
        # Create a new hash object with the requested algorithm
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # hashlib raises a ValueError if the algorithm is unknown
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Encode the password to bytes (UTF‑8) and feed it into the hasher
    hasher.update(password.encode('utf-8'))

    # Return the hexadecimal digest string
    return hasher.hexdigest()