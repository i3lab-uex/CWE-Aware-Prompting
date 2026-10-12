import hashlib

# Supported hash algorithms (as defined in the task description)
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns the
    hexadecimal representation of the hash.

    Parameters:
        algorithm_name (str): Name of the hash algorithm to use.
        raw_password (str): The password string to hash.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If an unsupported hash algorithm is requested.
    """
    # Normalise the algorithm name to handle case variations
    algo = algorithm_name.lower()

    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            "Supported algorithms are: " + ", ".join(sorted(_SUPPORTED_ALGORITHMS))
        )

    # Create a new hash object
    hasher = hashlib.new(algo)

    # Update the hash with the password bytes (UTF-8 encoding)
    hasher.update(raw_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()