import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return
    its hexadecimal representation.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use. Must be one of the algorithms
        supported by :mod:`hashlib` on the current platform.
    pwd : str
        Plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Ensure we have a set of available algorithms for quick lookup
    available = hashlib.algorithms_available

    # Normalise algorithm name to match what hashlib expects
    algo_name = hash_algo.lower()

    if algo_name not in available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            "Please choose from the following supported algorithms:\n"
            f"{', '.join(sorted(available))}"
        )

    # Encode the password as UTF-8 before hashing
    pwd_bytes = pwd.encode('utf-8')

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pwd_bytes)

    return hasher.hexdigest()