import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Securely hash a password using the specified algorithm and return the
    resulting hexadecimal string.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
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
    if not isinstance(hash_algo, str):
        raise TypeError("hash_algo must be a string")
    if not isinstance(passcode, str):
        raise TypeError("passcode must be a string")

    # Ensure the algorithm is available
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(hash_algo.lower())
    hasher.update(passcode.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()