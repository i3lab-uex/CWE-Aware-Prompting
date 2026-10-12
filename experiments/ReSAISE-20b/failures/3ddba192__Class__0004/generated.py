import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Hashes a password using the specified algorithm and returns the hexadecimal digest.

    Args:
        hash_algo: Name of the hash function to use (must be available in hashlib.algorithms_available).
        passcode: The password string to hash.

    Returns:
        A hexadecimal string representing the hashed password.

    Raises:
        ValueError: If the specified hash algorithm is not supported.
    """
    # Normalize the algorithm name to match hashlib's expected format
    algo = hash_algo.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not available in hashlib.")

    # Create a new hash object and update it with the password bytes
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # This should not happen because we already checked availability,
        # but guard against any edge cases.
        raise ValueError(f"Failed to create hash object for algorithm '{hash_algo}'.") from exc

    # Ensure the password is encoded to bytes; use UTF-8 for consistency
    hasher.update(passcode.encode('utf-8'))

    # Return the hexadecimal digest of the hash
    return hasher.hexdigest()