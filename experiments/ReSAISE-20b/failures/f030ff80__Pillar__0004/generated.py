import hashlib

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes the provided password using the specified hash algorithm and returns
    the hexadecimal representation of the digest.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    pass_input : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise the algorithm name (hashlib expects lower‑case)
    algo = hash_type.lower()

    # Check that the algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: '{hash_type}'. "
                         f"Supported algorithms include: {sorted(hashlib.algorithms_available)}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pass_input.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()