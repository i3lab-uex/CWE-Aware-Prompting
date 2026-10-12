import hashlib

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalise algorithm name (hashlib is case‑insensitive but some names may have dashes)
    algo = algorithm_name.lower()

    # Get the set of algorithms supported by this Python build
    available_algos = {name.lower() for name in hashlib.algorithms_available}

    if algo not in available_algos:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(available_algos))}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(raw_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()