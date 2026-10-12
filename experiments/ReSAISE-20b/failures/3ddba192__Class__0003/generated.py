import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified algorithm and returns a hexadecimal string.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    passcode : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the requested algorithm is available
    if hash_algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(hash_algo)
    hasher.update(passcode.encode('utf-8'))

    # Return the digest as a hex string
    return hasher.hexdigest()