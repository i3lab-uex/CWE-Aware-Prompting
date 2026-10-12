import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes the provided password using the specified algorithm and returns a
    hexadecimal digest string.

    Parameters
    ----------
    hash_algo : str
        Name of the hashing algorithm (e.g., 'sha256', 'blake2b', etc.).
    passcode : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalise algorithm name to lower case
    algo_name = hash_algo.lower()

    # Verify that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create the hash object
    hasher = hashlib.new(algo_name)

    # Encode the passcode to bytes (UTF-8) and update the hash
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()