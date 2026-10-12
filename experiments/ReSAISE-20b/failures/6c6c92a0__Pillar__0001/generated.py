import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Args:
        algo_name: Name of the hash algorithm (e.g., 'sha256').
        pwd: Password string to be hashed.

    Returns:
        bytes: The hash digest of the password.

    Raises:
        ValueError: If the requested algorithm is not supported by the system.
    """
    # Normalize algorithm name to lowercase for comparison
    algo = algo_name.lower()

    # Ensure the algorithm is available in this Python environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password as UTF-8 and update the hash
    hasher.update(pwd.encode('utf-8'))

    # Return the digest bytes
    return hasher.digest()