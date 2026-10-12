import hashlib

def secure_hashing(algorithm: str, pass_key: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Args:
        algorithm: Name of the hash algorithm (e.g., 'sha256', 'sha512').
        pass_key: The password string to hash.

    Returns:
        bytes: The binary digest of the hashed password.

    Raises:
        ValueError: If the requested algorithm is not supported on this system.
    """
    # Ensure algorithm name is case‑insensitive
    algo = algorithm.lower()

    # Verify that the requested algorithm exists in hashlib.algorithms_available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Encode the password using UTF‑8 before hashing
    hasher.update(pass_key.encode('utf-8'))

    # Return the binary digest (bytes)
    return hasher.digest()