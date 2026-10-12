import hashlib

# List of algorithms considered insecure for hashing passwords.
INSECURE_ALGORITHMS = {
    'md5',
    'sha1',
    'md5-sha1',  # combination of MD5 and SHA-1
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use (must be supported by hashlib).
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python installation.
    RuntimeWarning
        If the chosen algorithm is known to be insecure (MD5, SHA‑1, etc.).
    """
    # Ensure the algorithm name is case‑insensitive
    algo = algo_hash.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_hash}' is not available in this environment.")

    if algo in INSECURE_ALGORITHMS:
        # Emit a warning but still allow the operation
        import warnings
        warnings.warn(
            f"Using insecure hash algorithm '{algo_hash}'. "
            "Consider using a stronger algorithm such as SHA-256 or SHA-512.",
            RuntimeWarning
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd_input.encode('utf-8'))

    return hasher.digest()