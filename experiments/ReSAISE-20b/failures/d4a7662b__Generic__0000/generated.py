import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of a supported hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If `hash_algorithm` is not supported on the current system.
    """
    # Ensure the algorithm name is in lower case for consistency
    algo_name = hash_algorithm.lower()

    # Check if the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported on this system.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()