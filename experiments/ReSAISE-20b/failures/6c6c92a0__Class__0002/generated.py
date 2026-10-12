import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'sha512').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the password using the selected algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the underlying hashlib implementation.
    """
    # Normalize algorithm name to lower case, as hashlib expects
    algo_name = algo_name.lower()

    # Check if the algorithm is available on this system
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    # Encode password as UTF-8; this is the standard practice for hashing text
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest bytes
    return hasher.digest()