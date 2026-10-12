import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of a user's password using the specified algorithm.

    Args:
        algorithm_name (str): Name of the hash algorithm to use.
        user_pass (bytes): The password to be hashed.

    Returns:
        bytes: The computed hash digest.

    Raises:
        ValueError: If the requested algorithm is not supported.
    """
    # Normalize algorithm name to lowercase for consistency
    algo = algorithm_name.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and feed the password
    hasher = hashlib.new(algo)
    hasher.update(user_pass)

    # Return the digest as bytes
    return hasher.digest()