import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'md5').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Normalise algorithm name to lowercase
    algo = hash_name.lower()

    # Verify that the algorithm is available in this environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:          # pragma: no cover
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported.") from exc

    # Update the hash with the password bytes (UTF‑8 encoded)
    hasher.update(password.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()