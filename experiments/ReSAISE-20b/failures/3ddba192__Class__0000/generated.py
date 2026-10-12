import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_algo : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
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
    # Normalize algorithm name to lowercase for comparison
    algo_name = hash_algo.lower()

    # Verify the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create the hash object
    hasher = hashlib.new(algo_name)

    # Encode the password to bytes (UTF-8 is a common choice)
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()