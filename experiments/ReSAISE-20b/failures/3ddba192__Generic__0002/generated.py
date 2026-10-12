import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns
    the result as a hexadecimal string.

    Parameters:
        hash_algo (str): Name of the hash algorithm to use.
        passcode (str): The password string to hash.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If the requested hash algorithm is not supported.
    """
    # Validate that the algorithm exists in hashlib.algorithms_available
    if hash_algo.lower() not in (name.lower() for name in hashlib.algorithms_available):
        raise ValueError(f"Hash algorithm '{hash_algo}' is not supported.")

    # Create a new hash object using the specified algorithm
    hasher = hashlib.new(hash_algo)

    # Encode the password to bytes (UTF-8 is standard)
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()