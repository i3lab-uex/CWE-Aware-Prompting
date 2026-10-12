import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use. Must be one of the algorithms supported by hashlib.
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is lowercase (hashlib accepts case-sensitive names)
    method = encryption_method.lower()

    # Verify that the requested algorithm is supported
    if method not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: '{encryption_method}'. "
                         f"Supported algorithms are: {sorted(hashlib.algorithms_available)}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(method)
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()