import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return
    its hexadecimal representation.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use. Must be one of the algorithms
        supported by hashlib.new().
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_algo`` is not supported or unavailable.
    """
    if not isinstance(hash_algo, str) or not isinstance(pwd, str):
        raise ValueError("Both hash_algo and pwd must be strings")

    try:
        # Create a new hash object
        hasher = hashlib.new(hash_algo)
    except ValueError as exc:
        # Raised when the algorithm is unknown or unsupported
        raise ValueError(
            f"Unsupported hash algorithm '{hash_algo}'. "
            "Available algorithms: " + ", ".join(hashlib.algorithms_available)
        ) from exc

    # Encode the password to bytes (UTF-8 is standard for hashing)
    hasher.update(pwd.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()