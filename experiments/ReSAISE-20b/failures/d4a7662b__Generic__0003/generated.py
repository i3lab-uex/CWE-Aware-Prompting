import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a supported hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on this system.
    """
    # Verify that the chosen algorithm is available
    if hash_algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported on this system.")

    # Create a new hash object
    hasher = hashlib.new(hash_algorithm)

    # Update the hash with the password encoded as UTF-8
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()