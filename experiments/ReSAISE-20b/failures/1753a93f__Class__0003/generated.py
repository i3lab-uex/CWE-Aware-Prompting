import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to apply (e.g., 'sha256', 'md5').
    pwd : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the provided hash algorithm is not supported or unavailable.
    """
    # Ensure the algorithm name is valid and available
    if hash_algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algo}'")

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(hash_algo)
    hasher.update(pwd.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()