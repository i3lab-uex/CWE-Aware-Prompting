import hashlib

# List of hash algorithms that are considered weak or deprecated.
_WEAK_ALGORITHMS = {
    "md5",
    "md5-sha1",
    "sha1",
}

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns
    its hexadecimal representation.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'blake2s').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib,
        or if it is considered weak/deprecated.
    """
    # Normalise the algorithm name to match hashlib's expectations
    algo = hash_name.lower()

    if algo in _WEAK_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_name}' is considered weak or deprecated.")

    # Verify that the algorithm exists in hashlib
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Encode the password as UTF‑8 bytes before hashing
    hash_func.update(password.encode("utf-8"))
    return hash_func.hexdigest()