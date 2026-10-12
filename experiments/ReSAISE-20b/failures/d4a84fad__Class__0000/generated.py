import hashlib

# Set of supported hash algorithms (as defined by the problem statement)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512', 'sha3_224'
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its hexadecimal representation.

    Args:
        encryption_method (str): The name of the hash algorithm to use.
        user_password (str): The plaintext password.

    Returns:
        str: The hexadecimal digest of the hashed password.

    Raises:
        ValueError: If an unsupported hash algorithm is requested.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = encryption_method.lower()

    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            f"Supported algorithms are: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Create a new hash object
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # This should not happen because we checked the list,
        # but guard against unexpected changes in hashlib
        raise ValueError(f"Hash algorithm '{encryption_method}' is not available.") from exc

    # Encode the password to bytes (UTF-8) and update the hasher
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()