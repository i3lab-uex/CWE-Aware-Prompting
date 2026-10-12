import hashlib

# Define a set of algorithms considered secure for password hashing.
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s',
    # Include sm3 if available (not guaranteed on all platforms)
    'sm3',
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use.
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the algorithm is not available or considered insecure.
    """
    # Normalise algorithm name to lower case
    algo = algorithm_name.lower()

    # Check that the algorithm is available in hashlib and considered secure
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available.")

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is considered insecure for password hashing.")

    # Create a new hash object and update it with the UTF-8 encoded password
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    return hasher.digest()