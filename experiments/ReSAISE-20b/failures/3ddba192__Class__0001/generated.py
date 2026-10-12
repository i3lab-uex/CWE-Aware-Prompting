import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    passcode : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the algorithm exists
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(hash_algo.lower())

    # Update the hash with the password bytes
    hasher.update(passcode.encode('utf-8'))

    # Return hexadecimal digest
    return hasher.hexdigest()