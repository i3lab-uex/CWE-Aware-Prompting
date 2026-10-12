import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified algorithm and returns the hash in hexadecimal form.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
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
    # Normalise algorithm name to lower case for consistency
    algo_name = hash_algo.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(algo_name)

    # Encode the password to bytes (UTF-8 is a common, safe choice)
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()