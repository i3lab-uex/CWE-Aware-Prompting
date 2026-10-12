import hashlib

def encrypt_password(hash_algorithm: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'sha512').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the underlying hashlib implementation.
    """
    # Ensure algorithm name is lowercase to match hashlib's names
    algo_name = hash_algorithm.lower()

    # Verify that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new hash object
    hasher = hashlib.new(algo_name)

    # Update the hash with the password bytes (UTF-8 encoding)
    hasher.update(pwd.encode('utf-8'))

    # Return the raw digest
    return hasher.digest()