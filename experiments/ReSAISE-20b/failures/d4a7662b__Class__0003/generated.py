import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the cryptographic hash algorithm (e.g. 'sha256').
    pwd : str
        The password to be hashed.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by the system.
    """
    # Ensure password is encoded to bytes
    pwd_bytes = pwd.encode('utf-8')

    try:
        # Create a new hash object using the requested algorithm
        hasher = hashlib.new(hash_algorithm)
    except ValueError as exc:
        # Raise a clear error if the algorithm is unsupported
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}") from exc

    # Update the hasher with the password bytes and return the digest
    hasher.update(pwd_bytes)
    return hasher.digest()