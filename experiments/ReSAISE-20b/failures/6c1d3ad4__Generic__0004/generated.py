import hashlib

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the cryptographic hash algorithm to use.
    pwd_input : str
        The password string to be hashed.

    Returns
    -------
    bytes
        The resulting hash value as a byte string.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python environment.
    """
    # Normalise the algorithm name (hashlib is case‑insensitive but the set may use
    # a specific case; we convert to lower‑case for comparison).
    algo_name = algo_hash.lower()

    # Get the set of available algorithms (case‑insensitive).
    available = {name.lower() for name in hashlib.algorithms_available}

    if algo_name not in available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available.")

    # Create the hash object and feed it the password bytes.
    hasher = hashlib.new(algo_name)
    hasher.update(pwd_input.encode('utf-8'))

    # Return the raw digest bytes.
    return hasher.digest()