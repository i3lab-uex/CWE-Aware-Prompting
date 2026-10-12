import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use.
    password : str
        The plaintext password to be hashed.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is in a canonical form
    hash_name = hash_name.lower()

    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(hash_name)

    # Encode the password to bytes (UTF-8 is standard)
    hasher.update(password.encode('utf-8'))

    # Return the binary digest
    return hasher.digest()