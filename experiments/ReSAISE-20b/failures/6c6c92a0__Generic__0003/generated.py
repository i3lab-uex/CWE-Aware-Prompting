import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm (e.g., 'sha256').
    pwd : str
        The password to be hashed.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the selected hash algorithm is not supported by the system.
    """
    # Ensure algorithm name is lower case to match hashlib's naming
    algo = algo_name.lower()

    # Check if the algorithm is available on this system
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()