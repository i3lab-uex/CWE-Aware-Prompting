import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters:
        hash_algo (str): Name of the hash algorithm to use.
        pwd      (str): Plaintext password.

    Returns:
        str: Hexadecimal string of the hashed password.

    Raises:
        ValueError: If the specified algorithm is not supported or unavailable.
    """
    # Normalise the algorithm name to lowercase as hashlib uses lowercase names
    algo = hash_algo.lower()

    # Verify that the algorithm is available in this Python environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            "Available algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()