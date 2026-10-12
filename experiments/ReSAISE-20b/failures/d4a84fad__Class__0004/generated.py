import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its
    hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    user_password : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Ensure algorithm name is in a canonical form
    algo_name = encryption_method.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: "
            f"{sorted(hashlib.algorithms_available)}"
        )

    # Create a new hash object for the chosen algorithm
    hasher = hashlib.new(algo_name)

    # Encode password to bytes and update the hash
    hasher.update(user_password.encode('utf-8'))

    # Return hexadecimal digest
    return hasher.hexdigest()