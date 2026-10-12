import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters:
        hash_algo (str): The name of the hash algorithm to use.
        pwd      (str): The plaintext password.

    Returns:
        str: Hexadecimal string of the hashed password.

    Raises:
        ValueError: If the requested algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lower case as hashlib uses lower‑case names
    algo = hash_algo.lower()

    # Check if the algorithm is available in this Python environment.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_algo}")

    # Create a new hash object and feed the password bytes
    h = hashlib.new(algo)
    h.update(pwd.encode("utf-8"))

    # Return the hexadecimal digest
    return h.hexdigest()