import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm (e.g., 'sha256').
    pass_key : str
        The password to be hashed.

    Returns
    -------
    bytes
        The hash digest of the provided password.

    Raises
    ------
    ValueError
        If the selected algorithm is not supported or considered insecure.
    """
    # List of algorithms generally regarded as secure for hashing passwords
    SECURE_ALGORITHMS = {
        'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'blake2b', 'blake2s',
        'sha512_224', 'sha512_256',
    }

    # Normalize algorithm name to lowercase
    alg = algorithm.lower()

    # Check if the algorithm is available on this system
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm}' is not supported on this system.")

    # Ensure the algorithm is considered secure
    if alg not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm}' is considered insecure for password hashing.")

    # Compute the hash
    hasher = hashlib.new(alg)
    hasher.update(pass_key.encode('utf-8'))
    return hasher.digest()