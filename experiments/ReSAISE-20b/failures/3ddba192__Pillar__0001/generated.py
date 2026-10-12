import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use. Must be supported by hashlib.
    passcode : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `hash_algo` is not available in the current hashlib implementation.
    """
    # Normalise algorithm name to lower case as hashlib uses lowercase names
    algo_name = hash_algo.lower()

    # Verify the algorithm is available in the current environment
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not supported.")

    # Create a new hash object and feed the password (encoded as UTF-8)
    hasher = hashlib.new(algo_name)
    hasher.update(passcode.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()