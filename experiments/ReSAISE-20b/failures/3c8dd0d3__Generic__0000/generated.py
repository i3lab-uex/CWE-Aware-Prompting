import hashlib

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha512', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Ensure we are using a supported algorithm
    if algorithm_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(algorithm_name)

    # Encode the password to bytes and update the hash
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()