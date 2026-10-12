import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hashes the given plaintext password using the specified hash algorithm
    and returns its hexadecimal representation.

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
        If the requested algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lower case (hashlib uses lower-case names)
    algo_name = hash_algo.lower()

    # Check if the algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            "Please choose a valid algorithm from hashlib.algorithms_available."
        )

    # Encode the password to bytes; UTF-8 is a common choice
    pwd_bytes = pwd.encode("utf-8")

    # Create the hash object and compute the digest
    try:
        hasher = hashlib.new(algo_name)
        hasher.update(pwd_bytes)
        return hasher.hexdigest()
    except Exception as exc:
        # This should not normally happen, but we guard against unexpected errors
        raise ValueError(
            f"Failed to hash password using algorithm '{hash_algo}': {exc}"
        ) from exc