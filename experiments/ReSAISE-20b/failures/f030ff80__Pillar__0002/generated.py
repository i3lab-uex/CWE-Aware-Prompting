import hashlib

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its
    hexadecimal representation.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use. Supported values are those
        provided by hashlib.algorithms_available.
    pass_input : str
        The password string to hash.

    Returns
    -------
    str
        The hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Convert password to bytes once for all algorithms
    password_bytes = pass_input.encode("utf-8")

    # Normalize hash type to lowercase to avoid case sensitivity issues
    algorithm = hash_type.lower()

    # Verify that the requested algorithm is supported by hashlib
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash function '{hash_type}'. "
            f"Supported algorithms: {sorted(hashlib.algorithms_available)}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algorithm)
    hasher.update(password_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()