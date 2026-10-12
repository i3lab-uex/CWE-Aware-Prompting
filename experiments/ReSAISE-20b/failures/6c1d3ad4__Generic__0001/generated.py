import hashlib

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting digest of the password.

    Raises
    ------
    ValueError
        If the specified algorithm is not available in hashlib.
    """
    # Normalise the algorithm name (hashlib accepts lower‑case names)
    algo = algo_hash.lower()

    # Check if the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_hash}' is not available.")

    # Create the hash object, feed it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd_input.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()