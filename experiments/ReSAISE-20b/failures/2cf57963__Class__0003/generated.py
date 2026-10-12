import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    pass_key : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python
        environment or if it is considered insecure (e.g. md5, sha1).
    """
    # Normalize algorithm name
    algo_name = algorithm.lower()

    # List of algorithms known to be weak or broken; disallow them
    insecure_algorithms = {
        'md5',
        'sha1',
        'md4',
        'ripemd160',  # considered weak in some contexts
    }

    if algo_name in insecure_algorithms:
        raise ValueError(f"The algorithm '{algorithm}' is considered insecure and cannot be used.")

    # Verify that the algorithm exists in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm}' is not supported on this system.")

    # Create the hash object and compute digest
    hasher = hashlib.new(algo_name)
    # Encode the password to bytes (UTF-8 is standard for hashing text)
    hasher.update(pass_key.encode('utf-8'))
    return hasher.digest()