import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5', etc.).
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_algo`` is not a supported or available hash algorithm.
    """
    # Normalize the algorithm name to lower case
    algo = hash_algo.lower()

    # Verify that the requested algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            "Supported algorithms are: "
            f"{sorted(hashlib.algorithms_available)}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()