import hashlib

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    raw_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalise the algorithm name to lowercase for consistency
    algo = algorithm_name.lower()

    # Check if the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            "Supported algorithms are: "
            + ", ".join(sorted(hashlib.algorithms_available))
        )

    # Encode the password to bytes (UTF-8 is a safe default)
    pwd_bytes = raw_password.encode("utf-8")

    # Create the hash object and compute the digest
    hash_obj = hashlib.new(algo)
    hash_obj.update(pwd_bytes)

    # Return the hexadecimal representation
    return hash_obj.hexdigest()