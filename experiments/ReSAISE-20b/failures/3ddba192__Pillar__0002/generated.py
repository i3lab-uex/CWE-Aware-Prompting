import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Securely hash the provided password using the specified algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    passcode : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal string of the computed hash.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the algorithm exists
    if hash_algo.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create a new hash object
    hasher = hashlib.new(hash_algo)

    # Encode the passcode to bytes and update the hash
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()