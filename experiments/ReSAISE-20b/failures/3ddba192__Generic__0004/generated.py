import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns the
    hexadecimal digest.

    Parameters:
        hash_algo (str): Name of the hash function to use.
        passcode (str): The password string to be hashed.

    Returns:
        str: Hexadecimal representation of the hash digest.

    Raises:
        ValueError: If the requested hash algorithm is not supported.
    """
    # Ensure the requested algorithm is available
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(hash_algo.lower())
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()