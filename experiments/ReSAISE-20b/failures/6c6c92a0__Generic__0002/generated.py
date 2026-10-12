import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm (e.g., 'sha256', 'sha512_224').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Ensure the algorithm name is valid
    if algo_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo_name.lower())
    hasher.update(pwd.encode('utf-8'))
    return hasher.digest()