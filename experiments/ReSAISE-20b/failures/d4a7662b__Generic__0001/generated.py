import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the current Python
        installation.
    """
    # Normalise algorithm name to lowercase for comparison
    algo_name = hash_algorithm.lower()

    # Retrieve the set of supported algorithms from hashlib
    available_algorithms = {name.lower() for name in hashlib.algorithms_available}

    if algo_name not in available_algorithms:
        raise ValueError(f"Unsupported hash algorithm: '{hash_algorithm}'. "
                         f"Supported algorithms are: {sorted(available_algorithms)}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()