import hashlib

# Set of supported hash algorithm names as provided by the context
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes the given password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters:
        encryption_method (str): The name of the hash algorithm to use.
        user_password (str): The password to be hashed.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If `encryption_method` is not supported.
    """
    # Normalize the algorithm name to match the keys in SUPPORTED_ALGORITHMS
    algo_name = encryption_method.strip().lower()

    if algo_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash function '{encryption_method}'. "
            f"Supported algorithms are: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Create a new hash object and feed it the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()