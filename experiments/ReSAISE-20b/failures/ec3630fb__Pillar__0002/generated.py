import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    secret : str
        The password string to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Ensure the hash type exists in hashlib
    if hash_type.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Unsupported hash algorithm: {hash_type}")

    # Create a new hash object
    try:
        hasher = hashlib.new(hash_type)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to create hash object for {hash_type}") from exc

    # Update the hasher with the secret encoded in UTF-8
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()