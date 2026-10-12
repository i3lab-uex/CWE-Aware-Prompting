import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `encryption_method` is not a supported hash algorithm.
    """
    # Normalise the algorithm name (hashlib uses lowercase names)
    algo = encryption_method.lower()

    # Verify that the algorithm is supported by the current Python runtime
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: "
            + ", ".join(sorted(hashlib.algorithms_available))
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(user_password.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()