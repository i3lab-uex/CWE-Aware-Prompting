import hashlib

# A curated set of secure hash algorithms (excluding known weak ones)
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s',
    # Add other algorithms you consider secure for your use case
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest of the password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available or deemed insecure.
    """
    # Normalize name for comparison
    algo = algorithm_name.lower()

    # Ensure the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not supported by hashlib.")

    # Reject algorithms that are explicitly considered insecure
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is considered insecure for password hashing.")

    # Create the hash object and compute digest
    try:
        hasher = hashlib.new(algo)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Failed to create hash object for algorithm '{algorithm_name}': {exc}")

    hasher.update(pwd.encode('utf-8'))
    return hasher.digest()