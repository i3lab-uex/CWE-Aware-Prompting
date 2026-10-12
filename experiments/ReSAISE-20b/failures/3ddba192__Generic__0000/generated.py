import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes the provided password using the specified algorithm and returns
    a hexadecimal digest string.

    Parameters:
        hash_algo (str): Name of the hashing algorithm to use.
        passcode (str): The password string to hash.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If the requested hash algorithm is not supported.
    """
    # Ensure the algorithm name is in lowercase for consistency
    algo = hash_algo.lower()

    try:
        # Create a new hash object using the specified algorithm
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # The algorithm is not available in this environment
        raise ValueError(
            f"Hash algorithm '{hash_algo}' is not supported."
        ) from exc

    # Encode the password to bytes (UTF-8) and feed it into the hasher
    hasher.update(passcode.encode("utf-8"))

    # Return the hexadecimal digest of the hash
    return hasher.hexdigest()