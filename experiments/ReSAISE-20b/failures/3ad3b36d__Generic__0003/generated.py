import hashlib

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the algorithms supported by
        :mod:`hashlib`.  Examples include 'sha256', 'md5', 'blake2b', etc.
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If ``algorithm_name`` is not supported by :mod:`hashlib`.

    Notes
    -----
    The function encodes the password using UTF‑8 before hashing.  It does **not**
    automatically add a salt; callers should handle salting separately if
    required for security.  The function validates the algorithm name by attempting
    to create a new hash object; if it fails, a clear error message is raised.
    """
    try:
        # Create a new hash object for the requested algorithm
        hasher = hashlib.new(algorithm_name)
    except ValueError as exc:
        # Provide a helpful error message listing supported algorithms
        supported = sorted(
            name for name in hashlib.algorithms_available if not name.startswith('shake_')
        )
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(supported)}"
        ) from exc

    # Encode the password to bytes and update the hash
    hasher.update(raw_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()