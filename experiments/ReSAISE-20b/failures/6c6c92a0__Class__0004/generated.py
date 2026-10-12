import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Args:
        algo_name (str): Name of the hash algorithm to use (e.g., 'sha256').
        pwd (str): Password string to be hashed.

    Returns:
        bytes: The binary hash digest of the password.

    Raises:
        ValueError: If the requested algorithm is not supported by the system.
    """
    # Normalize algorithm name to lowercase for consistency
    algo_name = algo_name.lower()

    # Check if the requested algorithm is available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()