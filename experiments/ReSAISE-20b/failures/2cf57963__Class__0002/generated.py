import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm (e.g., 'sha256', 'sha512').
    pass_key : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current system.
    """
    # Normalize algorithm name (hashlib accepts lower‑case names)
    algo_name = algorithm.lower()

    # Verify that the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo_name)
    # Encode the password using UTF-8 to ensure consistent byte representation
    hasher.update(pass_key.encode('utf-8'))

    # Return the raw digest bytes (not hex or base64)
    return hasher.digest()