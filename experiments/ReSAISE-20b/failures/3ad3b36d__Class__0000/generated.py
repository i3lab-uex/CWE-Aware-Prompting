import hashlib

# Set of algorithms that are considered insecure (for reference)
_INSECURE_ALGORITHMS = {"md5", "sha1", "md4", "md2"}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal digest.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the algorithms supported by hashlib.
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Validate that the algorithm exists in hashlib
    if algorithm_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {sorted(hashlib.algorithms_available)}"
        )

    # Optional: warn about weak algorithms
    if algorithm_name.lower() in _INSECURE_ALGORITHMS:
        # In production code you might log a warning instead of raising.
        pass  # For this exercise we simply proceed.

    # Create the hash object and compute digest
    hasher = hashlib.new(algorithm_name)
    hasher.update(raw_password.encode("utf-8"))
    return hasher.hexdigest()