import hashlib

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use (case-insensitive).
    pass_input : str
        The password string to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash value.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Normalise hash name to lower case for consistency
    algo_name = hash_type.lower()

    # Ensure the algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            "Supported algorithms: "
            + ", ".join(sorted(hashlib.algorithms_available))
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pass_input.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()