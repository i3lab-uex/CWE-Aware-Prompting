import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (must be supported by hashlib).
    passcode : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Validate that the algorithm exists
    try:
        hasher = hashlib.new(hash_algo)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}") from exc

    # Encode the password to bytes (UTF-8 is a safe, standard choice)
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()