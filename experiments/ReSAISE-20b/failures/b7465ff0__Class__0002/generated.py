import hashlib

# List of weak algorithms that are generally discouraged for password hashing.
_WEAK_ALGORITHMS = {"md5", "md5-sha1", "sha1"}

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Compute a secure hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use. Must be supported by hashlib.
    key : bytes
        The password (or any secret) to hash.

    Returns
    -------
    str
        Hexadecimal representation of the computed digest.

    Raises
    ------
    ValueError
        If ``algo_name`` is not a valid hash algorithm name in hashlib.
    """
    # Ensure the algorithm exists
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.")

    # Warn about weak algorithms – they are still supported but discouraged.
    if algo_name.lower() in _WEAK_ALGORITHMS:
        # In a real application you might log this warning or raise an exception.
        pass

    # Create the hash object and update it with the key
    hasher = hashlib.new(algo_name)
    hasher.update(key)

    # Return the digest as a hex string
    return hasher.hexdigest()